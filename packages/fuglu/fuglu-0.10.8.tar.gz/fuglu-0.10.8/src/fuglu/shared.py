# -*- coding: UTF-8 -*-
#   Copyright 2009-2021 Oli Schacher, Fumail Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
import hashlib
import logging
import os
import time
import socket
import uuid
import threading
import email
import re
import configparser
import datetime
import tempfile as tf
import typing as tp
from string import Template
from email.header import Header, decode_header
from email.utils import getaddresses
from collections.abc import Mapping

from fuglu.addrcheck import Addrcheck
from fuglu.stringencode import force_uString, force_bString
from fuglu.mailattach import Mailattachment_mgr
from fuglu.lib.patchedemail import PatchedMessage, PatchedMIMEMultipart
from email.mime.base import MIMEBase
from fuglu.funkyconsole import FunkyConsole
from html.parser import HTMLParser
from .mixins import DefConfigMixin

HAVE_BEAUTIFULSOUP = False
try:
    import bs4 as BeautifulSoup
    HAVE_BEAUTIFULSOUP = True
except ImportError:
    pass

try:
    from domainmagic import extractor, tld
except ImportError:
    extractor = None
    tld = None

# constants

DUNNO = 0  # go on
ACCEPT = 1  # accept message, no further tests
DELETE = 2  # blackhole, no further tests
REJECT = 3  # reject, no further tests
DEFER = 4  # defer, no further tests

ALLCODES = {
    'DUNNO': DUNNO,
    'ACCEPT': ACCEPT,
    'DELETE': DELETE,
    'REJECT': REJECT,
    'DEFER': DEFER,
}


def actioncode_to_string(actioncode):
    """Return the human readable string for this code"""
    for key, val in list(ALLCODES.items()):
        if val == actioncode:
            return key
    if actioncode is None:
        return "NULL ACTION CODE"
    return 'INVALID ACTION CODE %s' % actioncode


def string_to_actioncode(actionstring, config=None):
    """return the code for this action"""
    upper = actionstring.upper().strip()

    # support DISCARD as alias for DELETE
    if upper == 'DISCARD':
        upper = 'DELETE'

    if config is not None:
        if upper == 'DEFAULTHIGHSPAMACTION':
            confval = config.get('spam', 'defaulthighspamaction').upper()
            if confval not in ALLCODES:
                return None
            return ALLCODES[confval]

        if upper == 'DEFAULTLOWSPAMACTION':
            confval = config.get('spam', 'defaultlowspamaction').upper()
            if confval not in ALLCODES:
                return None
            return ALLCODES[confval]

        if upper == 'DEFAULTVIRUSACTION':
            confval = config.get('virus', 'defaultvirusaction').upper()
            if confval not in ALLCODES:
                return None
            return ALLCODES[confval]

    if upper not in ALLCODES:
        return None
    return ALLCODES[upper]

class _SuspectTemplate(Template):
    delimiter = '$'
    idpattern = r'@?[a-z][_a-z0-9.:]*'

class _SuspectDict(Mapping):
    """Dictionary-like object which fetches SuspectFilter values dynamically"""

    def __init__(self, suspect, values, valuesfunction):
        self.values = values
        self.filter = SuspectFilter(filename=None)
        self.valuesfunction = valuesfunction
        self.suspect = suspect

    def _get_raw(self, item):
        if item in self.values: # always try the passed dict first
            return self.values[item]
        # get the value from the filter
        fieldlist = self.filter.get_field(self.suspect, item)
        if len(fieldlist):
            # if there are multiple values , just return the first
            return force_uString(str(fieldlist[0]))
        return None

    def __getitem__(self, item):
        val = self._get_raw(item)
        if self.valuesfunction:
            try:
                # valuesfunction expects a dict (backward compatibility)
                val = self.valuesfunction({item:val})[item]
            except KeyError:
                val = None
        if val is not None:
            self.values[item] = val
            return val
        return ''

    def __iter__(self):
        return iter(self.values.copy())

    def __len__(self):
        return len(self.values)

def apply_template(templatecontent, suspect, values=None, valuesfunction=None):
    """Replace templatecontent variables as defined in https://fumail.gitlab.io/fuglu/plugins-index.html#template-variables
    with actual values from suspect
    the calling function can pass additional values by passing a values dict

    if valuesfunction is not none, it is called with the final dict with all built-in and passed values
    and allows further modifications, like SQL escaping etc
    """
    if values is None:
        values = {}

    default_template_values(suspect, values)
    sdict = _SuspectDict(suspect, values, valuesfunction)
    template = _SuspectTemplate(force_uString(templatecontent))
    message = template.safe_substitute(sdict)
    return message


def default_template_values(suspect, values=None):
    """Return a dict with default template variables applicable for this suspect
    if values is not none, fill the values dict instead of returning a new one"""

    if values is None:
        values = {}

    values['id'] = suspect.id
    values['timestamp'] = suspect.timestamp
    values['from_address'] = suspect.from_address
    values['to_address'] = suspect.to_address
    values['from_domain'] = suspect.from_domain
    values['to_domain'] = suspect.to_domain
    values['subject'] = suspect.get_message_rep()['subject']
    values['date'] = str(datetime.date.today())
    values['time'] = time.strftime('%X')
    return values

HOSTNAME = socket.gethostname()


def yesno(val):
    """returns the string 'yes' for values that evaluate to True, 'no' otherwise"""
    if val:
        return 'yes'
    else:
        return 'no'


class Suspect(object):

    """
    The suspect represents the message to be scanned. Each scannerplugin will be presented
    with a suspect and may modify the tags or even the message content itself.
    """

    def __init__(self, from_address: str, recipients: tp.Union[str, tp.List[str]],
                 tempfile: tp.Optional[str], inbuffer: tp.Optional[bytes] = None,
                 smtp_options: tp.Optional[tp.Set] = None, **kwargs):
        self.source = None
        """holds the message source if set directly"""

        self._msgrep = None
        """holds a copy of the message representation"""

        # it's possible to pass ID to suspect
        id = kwargs.pop('id', None)
        self.id = id if id else Suspect.generate_id()

        # store additional keyword parameters
        self.kwargs = kwargs

        self.logger = logging.getLogger('fuglu.Suspect')

        # tags set by plugins
        self.tags = {
            'virus': {},
            'blocked': {},
            'spam': {},
            'highspam': {},
            'decisions': [],
            'scantimes': []
        }

        # temporary file containing the message source
        self._tempfile = tempfile

        # input message buffer
        self.inbuffer = force_bString(inbuffer)

        # stuff set from smtp transaction
        if tempfile:
            self.size = os.path.getsize(tempfile)
        elif inbuffer:
            self.size = len(self.inbuffer)
        else:
            self.size = None
        self.from_address = force_uString(from_address)

        # backwards compatibility, recipients can be a single address
        if isinstance(recipients, list):
            self.recipients = [force_uString(rec) for rec in recipients]
        else:
            self.recipients = [force_uString(recipients), ]

        # basic email validitiy check - nothing more than necessary for our internal assumptions
        for rec in self.recipients:
            if rec is None:
                self.logger.warning("%s: Recipient address can not be None" % self.id)
                raise ValueError("Recipient address can not be None")
            if not Addrcheck().valid(rec):
                self.logger.warning("%s: Invalid recipient address: %s" % (self.id, rec))
                raise ValueError("Invalid recipient address: %s" % rec)

        # additional basic information
        self.timestamp = time.time()

        # headers which are prepended before re-injecting the message
        self.addheaders = {}

        if self.from_address is None:
            self.from_address = u''

        if self.from_address != u'' and not Addrcheck().valid(self.from_address):
            self.logger.warning("%s: Invalid sender address: %s" % (self.id, self.from_address))
            raise ValueError("invalid sender address: %s" % self.from_address)

        """holds client info tuple: helo, ip, reversedns"""
        self.clientinfo = None

        """Attachment manager"""
        self._att_mgr = None

        # ------------- #
        # modifications #
        # ------------- #
        self.modified_headers = {}
        """To keep track of modified headers"""

        self.added_headers = {}
        """To keep track of already added headers (not in self.addheaders)"""

        # keep track of original sender/receivers
        self.original_from_address = self.from_address
        self.original_recipients = self.recipients

        # ------------ #
        # smtp_otpions #
        # ------------ #
        self.smtp_options = set() if smtp_options is None else smtp_options

        # eventually, size was also given in MAIL-FROM command
        mfsize = self.kwargs.get('mfsize', None)
        if self.size and isinstance(mfsize, int) and self.size < int(mfsize*0.9):
            errmsg = f"Message size received {self.size} is smaller than 90% of " \
                     f"the proposed size in MAILFROM {mfsize}"

            self.logger.error(errmsg)
            raise Exception(errmsg)

        self.logger.info(f"{self.id} "
                         f"from={self.from_address}, "
                         f"nrec={len(self.recipients)}, "
                         f"file={tempfile if tempfile else ''}, "
                         f"buffer={bool(inbuffer)}, "
                         f"size={self.size}, "
                         f"mfsize={self.kwargs.get('mfsize', 'N/A')}"
                         )

        # ------------------------- #
        # Attachment manager limits #
        # ------------------------- #
        # as property directly from kwargs:
        # - self._att_cachelimit
        # - self._att_defaultlimit
        # - self._att_maxlimit
        # - self._att_fdefaultlimit
        # - self._att_fmaxlimit

        # ------------------------ #
        # SASL authentication info #
        # queue id                 #
        # (milter mode only)       #
        # ------------------------ #
        # as property directly from kwargs:
        # - self.sasl_login
        # - self.sasl_sender
        # - self.sasl_method

        # ------------------ #
        # queue id           #
        # (milter mode only) #
        # ------------------ #
        # as property directly from kwargs:
        # self.queue_id

        # ---------- #
        # Assertions #
        # ---------- #
        # note the assertions are at the end because everything below will not be called
        # and variables not set, which is however still required for the HealthCheckSuspect

        # either there is a filename defined or a message buffer given
        # (filename can be /dev/null for an empty suspect)
        assert bool(tempfile) or bool(inbuffer)

        # either filename or buffer, not both...
        assert not (bool(tempfile) and bool(inbuffer))


    @property
    def tmpdir(self):
        return self.kwargs.get('queue_id', '/tmp')

    @property
    def tempfile(self):
        if self._tempfile is None:

            (handle, tempfilename) = tf.mkstemp( prefix='fuglu', dir=self.tmpdir)
            if self.inbuffer:
                self._tempfile = tempfilename
                try:
                    fhandle = os.fdopen(handle, 'w+b')
                    fhandle.write(self.inbuffer)
                    fhandle.close()
                    self.logger.debug(f"{self.id} -> tempfile requested, creating file from buffer")
                except Exception as e:
                    self.logger.error(f"{self.id} -> tempfile requested, error creating file from buffer: {str(e)}", exc_info=e)
                    self._tempfile = None
            else:
                self.logger.error(f"{self.id} -> tempfile requested but there's no filename and no buffer!")

        return self._tempfile

    def tempfilename(self) -> str:
        if self._tempfile:
            return self._tempfile
        else:
            return "(buffer-only)"

    @tempfile.setter
    def tempfile(self, val):
        self._tempfile = val

    @property
    def queue_id(self):
        return self.kwargs.get('queue_id')

    @property
    def _att_cachelimit(self):
        return self.kwargs.get('att_cachelimit')

    @property
    def _att_defaultlimit(self):
        return self.kwargs.get('att_defaultlimit')

    @property
    def _att_maxlimit(self):
        return self.kwargs.get('att_maxlimit')

    @property
    def _att_fdefaultlimit(self):
        return self.kwargs.get('att_fdefaultlimit')

    @property
    def _att_fmaxlimit(self):
        return self.kwargs.get('att_fmaxlimit')

    @property
    def sasl_login(self):
        return self.kwargs.get('sasl_login')

    @property
    def sasl_sender(self):
        return self.kwargs.get('sasl_sender')

    @property
    def sasl_method(self):
        return self.kwargs.get('sasl_method')

    def orig_from_address_changed(self):
        return self.original_from_address != self.from_address

    def orig_recipients_changed(self):
        return self.original_recipients != self.recipients

    @property
    def att_mgr(self):
        if self._att_mgr is None:
            self._att_mgr = Mailattachment_mgr(self.get_message_rep(), self.id,
                                               cachelimit=self._att_cachelimit,
                                               default_filelimit=self._att_defaultlimit,
                                               max_filelimit=self._att_maxlimit,
                                               default_numfilelimit=self._att_fdefaultlimit,
                                               max_numfilelimit=self._att_fmaxlimit
                                               )
        return self._att_mgr

    @property
    def to_address(self):
        """Returns the first recipient address"""
        try:
            return self.recipients[0]
        except IndexError:
            return None

    @to_address.setter
    def to_address(self, recipient):
        """Sets a single recipient for this suspect, removing all others"""
        self.recipients=[recipient,]

    @property
    def to_localpart(self):
        """Returns the local part of the first recipient"""
        # catch empty and None
        if not self.to_address:
            return ''
        try:
            return self.to_address.rsplit('@', 1)[0]
        except Exception:
            logging.getLogger('suspect').error('could not extract localpart from recipient address %s' % self.to_address)
            return None

    @property
    def to_domain(self):
        """Returns the local part of the first recipient"""
        # catch empty and None
        if not self.to_address:
            return ''
        try:
            return self.to_address.rsplit('@', 1)[1]
        except Exception:
            logging.getLogger('suspect').error('could not extract domain from recipient address %s' % self.from_address)
            return None


    @property
    def from_localpart(self):
        # catch empty and None
        if not self.from_address:
            return ''

        else:
            try:
               return self.from_address.rsplit('@', 1)[0]
            except Exception:
                logging.getLogger('suspect').error('could not extract localpart from sender address %s'%self.from_address)
                return None

    @property
    def from_domain(self):
        # catch empty and None
        if not self.from_address:
            return ''

        else:
            try:
                return self.from_address.rsplit('@', 1)[1]
            except Exception:
                logging.getLogger('suspect').error('could not extract domain from sender address %s' % self.from_address)
                return None


    @staticmethod
    def generate_id():
        """
        returns a unique id (a string of 32 hex characters)
        """
        return uuid.uuid4().hex

    def debug(self, message):
        """Add a line to the debug log if debugging is enabled for this message"""
        if not self.get_tag('debug'):
            return
        isotime = datetime.datetime.now().isoformat()
        fp = self.get_tag('debugfile')
        try:
            fp.write('%s %s\n' % (isotime, message))
            fp.flush()
        except Exception as e:
            logging.getLogger('suspect').error(
                'Could not write to logfile: %s' % e)

    def get_tag(self, key, defaultvalue=None):
        """returns the tag value. if the tag is not found, return defaultvalue instead (None if no defaultvalue passed)"""
        if key not in self.tags:
            return defaultvalue
        return self.tags[key]

    def set_tag(self, key, value):
        """Set a new tag"""
        self.tags[key] = value

    def is_highspam(self):
        """Returns True if ANY of the spam engines tagged this suspect as high spam"""
        for key in list(self.tags['highspam'].keys()):
            val = self.tags['highspam'][key]
            if val:
                return True
        return False

    def is_spam(self):
        """Returns True if ANY of the spam engines tagged this suspect as spam"""
        for key in list(self.tags['spam'].keys()):
            val = self.tags['spam'][key]
            if val:
                return True
        return False

    def is_blocked(self):
        """Returns True if ANY plugin tagged this suspect as blocked"""
        for key in list(self.tags['blocked'].keys()):
            val = self.tags['blocked'][key]
            if val:
                return True
        return False

    def is_virus(self):
        """Returns True if ANY of the antivirus engines tagged this suspect as infected"""
        for key in list(self.tags['virus'].keys()):
            val = self.tags['virus'][key]
            if val:
                return True
        return False

    def is_ham(self):
        """Returns True if message is neither considered to be spam, virus or blocked"""
        if self.is_spam() or self.is_virus() or self.is_blocked() or self.is_highspam():
            return False
        return True

    def update_subject(self, subject_cb, **cb_params):
        """
        update/alter the message subject
        :param subject_cb: callback function that alters the subject. must accept a string and return a string
        :param cb_params: additional parameters to be passed to subject_cb
        :return: True if subject was altered, False otherwise
        """
        msgrep = self.get_message_rep()
        oldsubj = msgrep.get("subject",None)

        oldsubj_exists = True

        if oldsubj is None:
            oldsubj = ""
            oldsubj_exists = False

        newsubj = subject_cb(oldsubj, **cb_params)
        if oldsubj != newsubj:
            del msgrep["subject"]
            msgrep["subject"] = newsubj

            # store as modified header
            if oldsubj_exists:
                self.modified_headers["subject"] = newsubj
            else:
                self.added_headers["subject"] = newsubj

            # no need to reset attachment manager because of a header change
            self.set_message_rep(msgrep,att_mgr_reset=False)
            if self.get_tag('origsubj') is None:
                self.set_tag('origsubj', oldsubj)
            return True
        return False


    def set_header(self, key, value):
        """
        Replace existing header or create a new one

        Args:
            key (string): header key
            value (string): header value

        """
        msg = self.get_message_rep()

        # convert inputs if needed
        key = force_uString(key)
        value = force_uString(value)

        oldvalue = msg.get(key,None)
        if oldvalue is not None:
            if force_uString(oldvalue) == value:
                return
            del msg[key]
            self.modified_headers[key] = value
        else:
            self.added_headers[key] = value

        msg[key] = value
        self.set_message_rep(msg,att_mgr_reset=False)

    @staticmethod
    def decode_msg_header(header, decode_errors="replace"):
        """
        Decode message header from email.message into unicode string

        Args:
            header (str, email.header.Header): the header to decode
            decode_errors (str): error handling as in standard bytes.decode -> strict, ignore, replace

        Returns:
            str
        """

        try:
            headerstring = u''.join(
                [force_uString(x[0], encodingGuess=x[1], errors=decode_errors) for x in decode_header(header)]
            )
        except TypeError:
            # if input is bytes (Py3) we end here
            header_unicode = force_uString(header)
            headerstring = u''.join(
                [force_uString(x[0], encodingGuess=x[1], errors=decode_errors) for x in decode_header(header_unicode)]
            )
        except Exception as e:
            headerstring = header
        return force_uString(headerstring)

    @staticmethod
    def prepend_header_to_source(key, value, source):
        """
        Prepend a header to the message

        Args:
            key (str): the header key
            value (str): the header value
            source (bytes): the message source

        Returns:
            bytes: the new message buffer

        """

        b_source = force_bString(source)

        # convert inputs if needed
        u_key = force_uString(key)
        u_value = force_uString(value)

        # is ignore the right thing to do here?
        # (moved from add_header) routine
        b_value = u_value.encode('UTF-8', 'ignore')
        try:
            hdr = Header(u_value, header_name=u_key, continuation_ws=' ')
        except (UnicodeDecodeError, UnicodeEncodeError):
            b_value = force_bString(u_value)
            hdr = Header(b_value, charset='utf-8', header_name=u_key, continuation_ws=' ')

        hdrline = u"%s: %s\r\n" % (u_key, hdr.encode())
        src = force_bString(hdrline) + b_source
        return src

    @staticmethod
    def getlist_space_comma_separated(inputstring):
        """Create list from string, splitting at ',' space"""
        finallist = []
        if inputstring:
            inputstring = inputstring.strip()
            if inputstring:
                # check for comma-separated list
                commaseplist = [tag.strip() for tag in inputstring.split(',') if tag.strip()]
                # also handle space-separated list
                for tag in commaseplist:
                    # take elements, split by spac
                    finallist.extend([t.strip() for t in tag.split(' ') if t.strip()])
        return finallist

    def parse_from_type_header(self, header='From', validate_mail=True, recombine=True):
        """

        Args:
            header (str): name of header to extract, defaults to From
            validate_mail (bool): base checks for valid mail
            recombine (bool): recombine displaypart with mailaddress

        Returns:
            [(displayname,email), ... ]
                - displayname (str) : display name
                - email (str) : email address

        """

        from_headers = self.get_message_rep().get_all(header, [])

        # allow multiple headers
        if len(from_headers) < 1:
            return []

        from_addresses_raw = []
        # replace \r\n by placeholders to allow getaddresses to properly distinguish between mail and display part
        #
        # This seems to be a stable way to overcome issues with encoded and multiline headers, see below
        #
        # Example: encoded display part without quotes
        # =?iso-8859-1?q?alpha=2C_beta?= <alpha.beta@fuglu.org>
        # If decode header:
        # alpha, beta <alpha.beta@fuglu.org>
        # and getaddresses returns
        # [(,alpha), (beta, alpha.beta@fuglu.org)]
        # -> this example works correctly if getaddresses is applied first and then decode_header
        #
        # Example: multiline
        # "=?iso-8859-1?q?alpha=2C?=\r\n =?iso-8859-1?q?beta?=" <alpha.beta@fuglu.org>
        # calling getaddresses returns only the first part
        # [('', '=?iso-8859-1?q?alpha=2C?=')]
        # -> calling decode header and then getaddresses works for this case
        #    (because the display name is surrounded by ", otherwise there's no way
        from_headers = [h.replace('\r', '{{CR}}').replace('\n', '{{LF}}') for h in force_uString(from_headers)]
        for display, mailaddress in getaddresses(from_headers):
            isvalid = True

            # after the split, put back the original CR/LF
            if display:
                display = display.replace('{{CR}}', '\r').replace('{{LF}}', '\n')
            if mailaddress:
                mailaddress = mailaddress.replace('{{CR}}', '\r').replace('{{LF}}', '\n')

            # display name eventually needs decoding
            display = Suspect.decode_msg_header(display)

            # Add if there is a display name or mail address,
            # ignore if both entries are empty
            if display or mailaddress:
                from_addresses_raw.append((display, mailaddress))

        # validate email
        from_addresses_val = []
        for displayname, mailaddress in from_addresses_raw:
            if mailaddress and (not Addrcheck().valid(mailaddress)):
                if displayname:
                    displayname += " "+mailaddress
                else:
                    displayname = mailaddress
                mailaddress = ""
            from_addresses_val.append((displayname, mailaddress))

        # --------- #
        # recombine #
        # --------- #
        #
        # if displaypart and mailaddress are not correctly extracted the might
        # appear in separate tuples, for example:
        # [('Sender', ''), ('', 'sender@fuglu.org')]
        # Recombine tries to merge such entries merging if
        # 1) element has display name but no mail address
        # 2) next consecutive element has not display name but mail address
        if recombine:
            from_addresses_recombined = []
            from collections import deque
            entry_list = deque(from_addresses_val)
            try:
                first = entry_list.popleft()
            except IndexError:
                # empty list
                first = None

            # use a loop counter so we can check for an infinite loop
            loopcounter = 0
            while first:
                # check if we're in an infinite loop
                loopcounter += 1
                if loopcounter > 2000:
                    raise ValueError("More than 2000 loops in parsing from-type header!")
                
                display, mailaddress = first
                if mailaddress:
                    from_addresses_recombined.append((display, mailaddress))
                    first = None
                else:
                    # if there's no mail address, check if the next element
                    # has a mail address
                    try:
                        second = entry_list.popleft()
                    except IndexError:
                        # empty list
                        second = None

                    if second:
                        # combine display parts of the elements
                        display2, mailaddress2 = second
                        if display:
                            newdisplay = "{} {}".format(display, display2)
                        else:
                            newdisplay = display2
                        first = (newdisplay.strip(), mailaddress2)
                    else:
                        # if there's no more element, add the current one to the list..
                        from_addresses_recombined.append((display, mailaddress))
                        # set first to None to stop the loop
                        first = None
                if not first:
                    try:
                        first = entry_list.popleft()
                    except IndexError:
                        # empty list
                        first = None
        else:
            from_addresses_recombined = from_addresses_val

        # again decode display part
        from_addresses_decoded = [(Suspect.decode_msg_header(display), mail)
                                  for display, mail in from_addresses_recombined]

        # validate email
        if validate_mail:
            from_addresses = []
            for displayname, mailaddress in from_addresses_decoded:
                try:
                    isvalid = True
                    if not mailaddress or (not Addrcheck().valid(mailaddress)):
                        isvalid = False
                except Exception as e:
                    isvalid = False
                    self.logger.error("%s: Parsing error %s" % (self.id, str(e)))
                    self.logger.exception(e)

                if isvalid:
                    from_addresses.append((displayname, mailaddress))
                else:
                    self.logger.info("%s, Mail \"%s\" is not valid, display name is \"%s\""
                                     % (self.id, mailaddress, displayname))
        else:
            from_addresses = from_addresses_decoded

        return from_addresses

    def add_header(self, key, value, immediate=False):
        """adds a header to the message. by default, headers will added when re-injecting the message back to postfix
        if you set immediate=True the message source will be replaced immediately. Only set this to true if a header must be
        visible to later plugins (eg. for spamassassin rules), otherwise, leave as False which is faster.
        """

        # convert inputs if needed
        key = force_uString(key)
        value = force_uString(value)

        if immediate:
            # no need to reset the attachment manager when just adding a header
            self.set_source(Suspect.prepend_header_to_source(key, value, self.get_source()), att_mgr_reset=False)
            # keep track of headers already added
            self.added_headers[key] = value
        else:
            self.addheaders[key] = value

    def addheader(self, key, value, immediate=False):
        """old name for add_header"""
        return self.add_header(key, value, immediate)

    def get_current_decision_code(self):
        dectag = self.get_tag('decisions')
        if dectag is None:
            return DUNNO
        try:
            pluginname, code = dectag[-1]
            return code
        except Exception:
            return DUNNO

    def _short_tag_rep(self):
        """return a tag representation suitable for logging, with some tags stripped, some shortened"""
        blacklist = ['decisions', 'scantimes', 'debugfile']
        tagscopy = {}

        for k, v in self.tags.items():
            if k in blacklist:
                continue

            try:
                strrep = str(v)
            except Exception:  # Unicodedecode errors and stuff like that
                continue

            therep = v

            maxtaglen = 100
            if len(strrep) > maxtaglen:
                therep = strrep[:maxtaglen] + "..."

            # specialfixes
            if k == 'SAPlugin.spamscore' and not isinstance(v, str):
                therep = "%.2f" % v

            tagscopy[k] = therep
        return str(tagscopy)

    def log_format(self, template=None):
        addvals = {
            'size': self.size,
            'spam': yesno(self.is_spam()),
            'highspam': yesno(self.is_highspam()),
            'blocked': yesno(self.is_blocked()),
            'virus': yesno(self.is_virus()),
            'modified': yesno(self.is_modified()),
            'decision': actioncode_to_string(self.get_current_decision_code()),
            'tags': self._short_tag_rep(),
            'fulltags': str(self.tags),
        }
        return apply_template(template, self, addvals)

    def __str__(self):
        """representation good for logging"""
        return self.log_format("Suspect ${id}: from=${from_address} to=${to_address} size=${size} spam=${spam} blocked=${blocked} virus=${virus} modified=${modified} decision=${decision} tags=${tags}")

    def get_message_rep(self):
        """returns the python email api representation of this suspect"""
        # do we have a cached instance already?
        if self._msgrep is not None:
            return self._msgrep

        if self.source is not None:
            if isinstance(self.source, str):
                msgrep = email.message_from_string(self.source, _class=PatchedMessage)
            else:
                msgrep = email.message_from_bytes(self.source, _class=PatchedMessage)

            self._msgrep = msgrep
            return msgrep
        else:
            # IMPORTANT: It is possible to use email.message_from_file BUT this will automatically replace
            #            '\r\n' in the message (_payload) by '\n' and the endtoend_test.py will fail!
            tmpSource = self.get_original_source()
            msgrep = email.message_from_bytes(tmpSource, _class=PatchedMessage)
            self._msgrep = msgrep
            return msgrep

    def getMessageRep(self):
        """old name for get_message_rep"""
        return self.get_message_rep()

    def set_message_rep(self, msgrep,att_mgr_reset=True):
        """replace the message content. this must be a standard python email representation
        Warning: setting the source via python email representation seems to break dkim signatures!

        The attachment manager is build based on the python mail representation. If no message
        attachments or content is modified there is no need to recreate the attachment manager.

        Args:
            msgrep (email): standard python email representation

        Keyword Args:
            att_mgr_reset (bool): Reset the attachment manager
        """
        try:
            self.set_source(msgrep.as_bytes(),att_mgr_reset=att_mgr_reset)
        except AttributeError:
            self.set_source(force_bString(msgrep.as_string()),att_mgr_reset=att_mgr_reset)

        # order is important, set_source sets source to None
        self._msgrep = msgrep

    def setMessageRep(self, msgrep):
        """old name for set_message_rep"""
        return self.set_message_rep(msgrep)

    def is_modified(self):
        """returns true if the message source has been modified"""
        return self.source is not None

    def get_source(self, maxbytes=None):
        """returns the current message source, possibly changed by plugins"""
        if self.source is not None:
            return self.source[:maxbytes]
        else:
            return self.get_original_source(maxbytes)

    def getSource(self, maxbytes=None):
        """old name for get_source"""
        return self.get_source(maxbytes)

    def set_source(self, source, encoding='utf-8', att_mgr_reset=True):
        """ Store message source. This might be modified by plugins later on...
        
        Args:
            source (bytes,str,unicode): new message source

        Keyword Args:
            encoding (str): encoding, default is utf-8
            att_mgr_reset (bool): Reset the attachment manager
        """
        self.source = force_bString(source,encoding=encoding)
        self._msgrep = None
        #if att_mgr_reset:
            #self._att_mgr = None
        self._att_mgr = None

    def setSource(self, source):
        """old name for set_source"""
        return self.set_source(source)

    def get_original_source(self, maxbytes=None):
        """returns the original, unmodified message source"""
        readbytes = -1
        if maxbytes is not None:
            readbytes = maxbytes
        try:
            # check internal filename directly (otherwise file gets created from buffer automatically...)
            if self._tempfile:
                with open(self.tempfile, 'rb') as fh:
                    source = fh.read(readbytes)
            else:
                source = bytes(self.inbuffer)[:maxbytes]
        except Exception as e:
            logging.getLogger('fuglu.suspect').error(
                'Cannot retrieve original source from tempfile %s : %s' % (self.tempfilename(), str(e)))
            raise e
        return source

    def getOriginalSource(self, maxbytes=None):
        """old name for get_original_source"""
        return self.get_original_source(maxbytes)

    def get_headers(self):
        """
        Returns the message headers as string

        Returns:
            (unicode str) unicode for Py2, str for Py3
        """
        headers = re.split(
            b'(?:\n\n)|(?:\r\n\r\n)', self.get_source(maxbytes=1048576), 1)[0]
        return force_uString(headers)

    def get_client_info(self, config=None):
        """returns information about the client that submitted this message.
        (helo,ip,reversedns)

        In before-queue mode this info is extracted using the XFORWARD SMTP protocol extension.

        In after-queue mode this information is extracted from the message Received: headers and therefore probably not 100% reliable
        all information is returned as-is, this means for example, that non-fcrdns client will show 'unknown' as reverse dns value.

        if no config object is passed, the first parseable Received header is used. otherwise, the config is used to determine the correct boundary MTA (trustedhostsregex / boundarydistance)
        """
        if self.clientinfo is not None:
            return self.clientinfo

        if config is None:
            self.logger.debug(f"Getting client info with no arguments")
            clientinfo = self.client_info_from_rcvd()

        else:
            # use extra try-except blocks because section environment doesn't have
            # default variables. Separate blocks are required to make sure on missing
            # variable doesn't reset the others
            try:
                trustedhostsregex = config.get('environment', 'trustedhostsregex')
            except (configparser.NoOptionError, configparser.NoSectionError):
                trustedhostsregex = ''

            try:
                boundarydistance = config.getint('environment', 'boundarydistance')
            except (configparser.NoOptionError, configparser.NoSectionError):
                boundarydistance = 0

            try:
                skiponerror = config.getboolean('environment', 'skiponerror')
            except (configparser.NoOptionError, configparser.NoSectionError):
                skiponerror = False

            try:
                trustedreceivedregex = config.get('environment', 'trustedreceivedregex')
            except (configparser.NoOptionError, configparser.NoSectionError):
                trustedreceivedregex = ''

            try:
                skipsamedomain = config.get('environment', 'skipsamedomain')
            except (configparser.NoOptionError, configparser.NoSectionError):
                skipsamedomain = False

            self.logger.debug(f"Getting client info with trustedhostsregex: {trustedhostsregex} and boundarydistance: {boundarydistance}")
            clientinfo = self.client_info_from_rcvd(ignoreregex=trustedhostsregex,
                                                    skip=boundarydistance,
                                                    skiponerror=skiponerror,
                                                    ignorelineregex=trustedreceivedregex,
                                                    skipsamedomain=skipsamedomain
                                                    )
        self.clientinfo = clientinfo
        return clientinfo

    def client_info_from_rcvd(self, ignoreregex=None, skip=0, skiponerror=False, ignorelineregex=None, skipsamedomain=False):
        """returns information about the client that submitted this message.
        (helo,ip,reversedns)

        This information is extracted from the message Received: headers and therefore probably not 100% reliable
        all information is returned as-is, this means for example, that non-fcrdns client will show 'unknown' as reverse dns value.

        if ignoreregex is not None, all results which match this regex in either helo,ip or reversedns will be ignored
        if ignorelineregex is not None, all results which match this regex will be ignored
        if skipsamedomain is True, ignore received lines where from & by domain is in same domain

        By default, this method starts searching at the top Received Header. Set a higher skip value to start searching further down.

        both these arguments can be used to filter received headers from local systems in order to get the information from a boundary MTA

        returns None if the client info can not be found or if all applicable values are filtered by skip/ignoreregex
        """
        ignorere = None
        if ignoreregex is not None and ignoreregex != '':
            ignorere = re.compile(ignoreregex)

        ignorelinere = None
        if ignorelineregex is not None and ignorelineregex != '':
            ignorelinere = re.compile(ignorelineregex)

        unknown = None

        receivedheaders_raw = self.get_message_rep().get_all('Received')
        if receivedheaders_raw is None:
            return unknown
        else:
            # make sure receivedheaders is an array of strings, no Header objects
            receivedheaders = [Suspect.decode_msg_header(h) for h in receivedheaders_raw]
            self.logger.debug(f"{self.id} (client_info_from_rcvd) Got {len(receivedheaders)} received headers")

        for rcvdline in receivedheaders[skip:]:
            h_rev_ip = self._parse_rcvd_header(rcvdline)
            if h_rev_ip is None:
                self.logger.debug(f"{self.id} (client_info_from_rcvd) Could not parse header line... -> rcv line was: {rcvdline} => {'skip' if skiponerror else 'break'}")
                if skiponerror:
                    continue
                else:
                    return unknown

            helo, revdns, ip, by = h_rev_ip
            self.logger.debug(f"{self.id} (client_info_from_rcvd) Parsed: helo={helo}, revdns={revdns}, ip={ip}, by={by}")

            # check if hostname or ip matches the ignore re, try next header if
            # it does
            if ignorere is not None:
                excludematch = ignorere.search(ip)
                if excludematch is not None:
                    self.logger.debug(f"{self.id} (client_info_from_rcvd) -> exclude (ip)")
                    continue

                if revdns:
                        excludematch = ignorere.search(revdns)
                        if excludematch is not None:
                            self.logger.debug(f"{self.id} (client_info_from_rcvd) -> exclude (revdns)")
                            continue

                if helo:
                        excludematch = ignorere.search(helo)
                        if excludematch is not None:
                            self.logger.debug(f"{self.id} (client_info_from_rcvd) -> exclude (helo)")
                            continue

            # check if line matches the ignore re, try next header if it does
            if ignorelinere is not None:
                excludematch = ignorelinere.search(rcvdline)
                if excludematch is not None:
                    self.logger.debug(f"{self.id} (client_info_from_rcvd) -> exclude (line)")
                    continue

            if skipsamedomain:
                tldmagic = tld.TLDMagic()
                try:
                    fqdn = extractor.domain_from_uri(revdns)
                    fromdomain = tldmagic.get_domain(fqdn)
                except Exception:
                    fromdomain = revdns

                try:
                    fqdn = extractor.domain_from_uri(by)
                    bydomain = tldmagic.get_domain(fqdn)
                except Exception:
                    bydomain = by

                try:
                    fqdn = extractor.domain_from_uri(helo)
                    helodomain = tldmagic.get_domain(fqdn)
                except Exception:
                    helodomain = by

                if bydomain \
                    and ((fromdomain and (fromdomain  == bydomain) ) or (helodomain and (helodomain == bydomain))):
                    self.logger.debug(f"{self.id} (client_info_from_rcvd) -> exclude (from/helo-domain == by-domain)")
                    continue

            clientinfo = helo, ip, revdns
            self.logger.info(f"{self.id} (client_info_from_rcvd) => extracted: helo={helo}, ip={ip}, revdns={revdns}")
            return clientinfo
        # we should only land here if we only have received headers in
        # mynetworks
        self.logger.info(f"{self.id} (client_info_from_rcvd) => Could not extract clientinfo")
        return unknown

    def _parse_rcvd_header(self, rcvdline):
        """return tuple HELO,REVERSEDNS,IP from received Header line, or None, if extraction fails"""
        receivedpattern = re.compile(
            r"^from\s(?P<helo>[^\s]+)\s+\((?P<revdns>[^\s]+)?\s?\[(?:IPv6:)?(?P<ip>(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?:[0-9a-f:]{3,40}))\]\)", re.MULTILINE)
        match = receivedpattern.search(rcvdline)
        if match is None:
            return None
        h_rev_ip = match.groups()
        helo, revdns, ip = h_rev_ip

        receivedbypattern = re.compile("\s+(by\s+(?P<by>[^\s]+))")
        match = receivedbypattern.search(rcvdline)
        if match is None:
            by = ""
        else:
            by = match.groups()[0]
        return helo, revdns, ip, by

    def source_stripped_attachments(self, content=None, maxsize=None, with_mime_headers=False):
        """
        strip all attachments from multipart mails except for plaintext and html text parts.
        if message is still too long, truncate.
        
        Args:
            content (string,bytes): message source
            maxsize (integer): maximum message size accepted
            with_mime_headers (boolean): add mime headers from attachments
        
        Returns:
            bytes: stripped and truncated message content
        """
        
        if content is None:
            content = self.get_source()
        
        # Content is str or bytes (Py3), so try both
        try:
            msgrep = email.message_from_string(content, _class=PatchedMessage)
        except TypeError:
            msgrep = email.message_from_bytes(content, _class=PatchedMessage)
        
        if msgrep.is_multipart():
            new_msg = PatchedMIMEMultipart()
            for hdr, val in msgrep.items():
                # convert "val" to "str" since in Py3 it might be of type email.header.Header
                new_msg.add_header(hdr, force_uString(val))
            for part in msgrep.walk():
                # only plaintext and html parts but no text attachments
                if part.get_content_maintype() == 'text' and part.get_filename() is None:
                    new_msg.attach(part)
                elif with_mime_headers:
                    new_part = MIMEBase(part.get_content_maintype(), part.get_content_subtype())
                    for mhdr, mval in part.items():
                        new_part.add_header(mhdr, force_uString(mval))
                        new_part.set_payload("")
                    new_msg.attach(new_part)
            new_src = new_msg.as_bytes()
        else:
            # text only mail - keep full content and truncate later
            new_src = force_bString(content)
        
        if maxsize and len(new_src) > maxsize:
            # truncate to maxsize
            new_src = new_src[:maxsize]
        
        return force_bString(new_src)
    
    
    def write_sa_temp_header(self, header, value, plugin='SAPlugin'):
        """
        Write a temporary pseudo header. This is used by e.g. SAPlugin to pass extra information to external services
        :param header: pseudo header name
        :param value: pseudo header value
        :param plugin: name of destination plugin. defaults to SAPlugin
        :return: None
        """
        hdr = "%s: %s" % (header, value)
        tag = self.get_tag('%s.tempheader' % plugin)
        if isinstance(tag, list):
            tag.append(hdr)
        elif tag is None:
            tag = [hdr, ]
        else:  # str/unicode
            tag = "%s\r\n%s" % (tag, hdr)
        self.set_tag('%s.tempheader' % plugin, tag)
        
        
    def get_sa_temp_headers(self, plugin='SAPlugin'):
        """
        returns temporary pseude headers as a bytes string.
        :param plugin: name of destination plugin. defaults to SAPlugin
        :return: bytes: temp headers
        """
        headers = b''
        tempheader = self.get_tag('%s.tempheader' % plugin)
        if tempheader is not None:
            if isinstance(tempheader, list):
                tempheader = "\r\n".join(tempheader)
            tempheader = tempheader.strip()
            if tempheader != '':
                headers = force_bString(tempheader + '\r\n')
        return headers


def strip_address(address):
    """
    Strip the leading & trailing <> from an address.  Handy for
    getting FROM: addresses.
    """
    start = address.find('<') + 1
    if start < 1:
        start = address.find(':') + 1
    if start < 1:
        return address
    end = address.find('>')
    if end < 0:
        end = len(address)
    retaddr = address[start:end]
    retaddr = retaddr.strip()
    return retaddr



def extract_domain(address, lowercase=True):
    if address is None or address == '':
        return None
    else:
        try:
            user, domain = address.rsplit('@', 1)
            if lowercase:
                domain = domain.lower()
            return domain
        except Exception as e:
            raise ValueError("invalid email address: '%s'" % address)




class BasicPlugin(DefConfigMixin):

    """Base class for all plugins"""

    def __init__(self, config, section=None):
        super().__init__(config)
        if section is None:
            self.section = self.__class__.__name__
        else:
            self.section = section

        self.config = config
        self.requiredvars = {}

    def _logger(self):
        """returns the logger for this plugin"""
        myclass = self.__class__.__name__
        loggername = "fuglu.plugin.%s" % myclass
        return logging.getLogger(loggername)

    def lint(self):
        return self.checkConfig()

    def checkConfig(self):
        """old name for check_config"""
        return self.check_config()

    def check_config(self):
        """Print missing / non-default configuration settings"""
        all_ok = True

        fc = FunkyConsole()
        # old config style
        if isinstance(self.requiredvars, (tuple, list)):
            for configvar in self.requiredvars:
                if isinstance(self.requiredvars, tuple):
                    (section, config) = configvar
                else:
                    config = configvar
                    section = self.section
                try:
                    self.config.get(section, config)
                except configparser.NoOptionError:
                    print(fc.strcolor(f"Missing configuration value without default [{section}] :: {config}", "red"))
                    all_ok = False
                except configparser.NoSectionError:
                    print(fc.strcolor(f"Missing configuration section containing variables without default "
                                      f"value [{section}] :: {config}", "red"))
                    all_ok = False

        # new config style
        if isinstance(self.requiredvars, dict):
            for config, infodic in self.requiredvars.items():
                section = infodic.get("section", self.section)

                try:
                    var = self.config.get(section, config)
                    if 'validator' in infodic:
                        if not infodic["validator"](var):
                            print(fc.strcolor(f"Validation failed for [{section}] :: {config}", "red"))
                            all_ok = False
                except configparser.NoSectionError:
                    print(fc.strcolor(f"Missing configuration section containing variables without default "
                                      f"value [{section}] :: {config}", "red"))
                    all_ok = False
                except configparser.NoOptionError:
                    print(fc.strcolor(f"Missing configuration value without default [{section}] :: {config}", "red"))
                    all_ok = False

        # missing sections -> this is only a warning since section is not required
        # as long as there are no required variables without default values...
        if all_ok:
            missingsections = set()
            for config, infodic in self.requiredvars.items():
                section = infodic.get("section", self.section)
                if section not in missingsections and not self.config.has_section(section):
                    missingsections.add(section)
            for section in missingsections:
                if section is None:
                    print(fc.strcolor(f"Pogramming error: Configuration section is manually None :: "
                                      f"Setup 'section' in requiredvars dict!", "red"))
                    all_ok = False
                else:
                    print(fc.strcolor(f"Missing configuration section [{section}] :: "
                                      f"All variables will use default values", "yellow"))
        return all_ok

    def __str__(self):
        classname = self.__class__.__name__
        if self.section == classname:
            return classname
        else:
            return '%s(%s)' % (classname, self.section)


class ScannerPlugin(BasicPlugin):
    """Scanner Plugin Base Class"""

    def examine(self, suspect: Suspect) -> tp.Optional[tp.Union[int, tp.Tuple[int, str]]]:
        self._logger().warning('Unimplemented examine() method')
        return None


class AVScannerPlugin(ScannerPlugin):
    """AV Scanner Plugin Base Class - Scanner Plugins that communicate with external AV scanners"""
    enginename = 'generic-av'

    def scan_stream(self, content, suspectid='(N/A)'):
        """
        Scans given byte buffer (file content). May raise an exception on errors.
        :param content: file content as string
        :param suspectid: suspect.id of currently processed suspect
        :return: None if no virus is found, else a dict filename -> virusname
        """
        self._logger().warning('Unimplemented scan_stream() method')


    def _check_too_big(self, suspect):
        """
        Checks if a message is too big for the current anti virus engine. Expects a maxsize configuration directive to be present
        :param suspect: the suspect object to be checked
        :return: boolean
        """
        if suspect.size > self.config.getint(self.section, 'maxsize'):
            self._logger().info('%s Not scanning - message too big (message %s bytes > config %s bytes )' %
                                (suspect.id, suspect.size, self.config.getint(self.section, 'maxsize')))
            return True
        return False


    def _virusreport(self, suspect, viruses):
        """
        Parses result of scan, tags suspect and returns action code and postfix reply message
        :param suspect: the suspect object
        :param viruses: the virus list generated by e.g. scan_stream function
        :return: action code, message
        """
        actioncode = DUNNO
        message = None
        if viruses is not None:
            self._logger().info("%s Virus found in message from %s : %s" % (suspect.id, suspect.from_address, viruses))
            suspect.tags['virus'][self.enginename] = True
            suspect.tags['%s.virus' % self.enginename] = viruses
            suspect.tags['%s.virus' % self.__class__.__name__] = viruses # deprecated, keep for compatibility
            suspect.debug('viruses found in message : %s' % viruses)
        else:
            suspect.tags['virus'][self.enginename] = False

        if viruses is not None:
            virusaction = self.config.get(self.section, 'virusaction')
            actioncode = string_to_actioncode(virusaction, self.config)
            firstinfected, firstvirusname = list(viruses.items())[0]
            values = dict(infectedfile=firstinfected, virusname=firstvirusname)
            message = apply_template(self.config.get(self.section, 'rejectmessage'), suspect, values)
        return actioncode, message


    def _problemcode(self):
        """
        safely calculates action code based on problemaction config value
        :return: action code
        """
        retcode = string_to_actioncode(
            self.config.get(self.section, 'problemaction'), self.config)
        if retcode is not None:
            return retcode
        else:
            # in case of invalid problem action
            return DEFER


    def lint_eicar(self, scan_function_name='scan_stream'):
        """
        passes an eicar (generic virus test) to the scanner engine
        :param scan_function_name: name of the scan function to be called
        :return: lint success as boolean
        """
        stream = """Date: Mon, 08 Sep 2008 17:33:54 +0200
To: oli@unittests.fuglu.org
From: oli@unittests.fuglu.org
Subject: test eicar attachment
X-Mailer: swaks v20061116.0 jetmore.org/john/code/#swaks
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="----=_MIME_BOUNDARY_000_12140"

------=_MIME_BOUNDARY_000_12140
Content-Type: text/plain

Eicar test
------=_MIME_BOUNDARY_000_12140
Content-Type: application/octet-stream
Content-Transfer-Encoding: BASE64
Content-Disposition: attachment

UEsDBAoAAAAAAGQ7WyUjS4psRgAAAEYAAAAJAAAAZWljYXIuY29tWDVPIVAlQEFQWzRcUFpYNTQo
UF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCoNClBLAQIU
AAoAAAAAAGQ7WyUjS4psRgAAAEYAAAAJAAAAAAAAAAEAIAD/gQAAAABlaWNhci5jb21QSwUGAAAA
AAEAAQA3AAAAbQAAAAAA

------=_MIME_BOUNDARY_000_12140--"""

        scan_function = getattr(self, scan_function_name)
        result = scan_function(force_bString(stream))
        if result is None:
            print("EICAR Test virus not found!")
            return False
        print("%s found virus %s" % (str(self), result))
        return True

    def _skip_on_previous_virus(self, suspect):
        """
        Configurable skip message scan based on previous virus findings.
        Args:
            suspect (fuglu.shared.Suspect):  the suspect 

        Returns:
            str: empty string means "don't skip", otherwise string contains reason to skip
        """
        skiplist = self.config.get(self.section, 'skip_on_previous_virus')
        if skiplist.lower() == "none":
            # don't skip
            return ""
        elif skiplist.lower() == "all":
            # skip if already marked as virus, no matter which scanner did mark
            isvirus = suspect.is_virus()
            if isvirus:
                return "Message is virus and skiplist is 'all' -> skip!"
            else:
                return ""
        else:
            # skip only if scanner from given list has marked message as virus
            scannerlist = [scanner.strip() for scanner in skiplist.split(',')]

            # dict with scanner as key for scanners that found a virus
            scanner_virustags = suspect.tags['virus']
            for scanner in scannerlist:
                if scanner_virustags.get(scanner, False):
                    return "Scanner %s has already tagged message as virus -> skip" % scanner
        return ""
    
    def lintinfo_skip(self):
        """
        If 'examine' method uses _skip_on_previous_virus to skip scan, this routine can be
        used to print lint info
        """
        skiplist = self.config.get(self.section, 'skip_on_previous_virus')
        if skiplist.lower() == "none":
            print("%s will always scan, even if message is already marked as virus" % self.enginename )
        elif skiplist.lower() == "all":
            print("%s will skip scan if message is already marked as virus" % self.enginename )
        else:
            # skip only if scanner from given list has marked message as virus
            scannerlist = [scanner.strip() for scanner in skiplist.split(',')]
            print("%s will skip scan if message is already marked as virus by: %s" 
                  % (self.enginename, ",".join(scannerlist)))
        return True


class PrependerPlugin(BasicPlugin):

    """Prepender Plugins - Plugins run before the scanners that can influence
    the list of scanners being run for a certain message"""

    def pluginlist(self, suspect, pluginlist):
        """return the modified pluginlist or None for no change"""
        return None

    def appenderlist(self, suspect, appenderlist):
        """return the modified appenderlist or None for no change"""
        return None

class AppenderPlugin(BasicPlugin):

    """Appender Plugins are run after the scan process (and after the re-injection if the message
    was accepted)"""

    def process(self, suspect, decision):
        self._logger().warning('Unimplemented process() method')


class SuspectFilter(object):

    """Allows filtering Suspect based on header/tag/body regexes"""

    def __init__(self, filename):
        self.filename = filename
        self.patterns = []

        self.reloadinterval = 30
        self.lastreload = 0
        self.logger = logging.getLogger('fuglu.suspectfilter')

        if filename is not None:
            self._reloadifnecessary()
        self.stripre = re.compile(r'<[^>]*?>')

    def _reloadifnecessary(self):
        now = time.time()
        # check if reloadinterval has passed
        if now - self.lastreload < self.reloadinterval:
            return
        if self.file_changed():
            self._reload()

    def _load_simplestyle_line(self, line):
        sp = line.split(None, 2)
        if len(sp) < 2:
            raise Exception(
                """"Invalid line '%s' in Rulefile %s. Ignoring.""" % (line, self.filename))

        args = None
        if len(sp) == 3:
            args = sp[2]

        fieldname = sp[0]
        # strip ending : (request AXB)
        if fieldname.endswith(':'):
            fieldname = fieldname[:-1]
        regex = sp[1]
        try:
            pattern = re.compile(regex, re.IGNORECASE | re.DOTALL)
        except Exception as e:
            raise Exception(
                'Could not compile regex %s in file %s (%s)' % (regex, self.filename, e))

        tup = (fieldname, pattern, args)
        return tup

    def _load_perlstyle_line(self, line):
        patt = r"""(?P<fieldname>[a-zA-Z0-9\-\.\_\:]+)[:]?\s+\/(?P<regex>(?:\\.|[^/\\])*)/(?P<flags>[IiMm]+)?((?:\s*$)|(?:\s+(?P<args>.*)))$"""
        m = re.match(patt, line)
        if m is None:
            return None

        groups = m.groupdict()
        regex = groups['regex']
        flags = groups['flags']
        if flags is None:
            flags = []
        args = groups['args']
        if args is not None and args.strip() == '':
            args = None
        fieldname = groups['fieldname']
        if fieldname.endswith(':'):
            fieldname = fieldname[:-1]

        reflags = 0
        for flag in flags:
            flag = flag.lower()
            if flag == 'i':
                reflags |= re.I
            if flag == 'm':
                reflags |= re.M

        try:
            pattern = re.compile(regex, reflags)
        except Exception as e:
            raise Exception(
                'Could not compile regex %s in file %s (%s)' % (regex, self.filename, e))

        tup = (fieldname, pattern, args)
        return tup

    def _reload(self):
        self.logger.info('Reloading Rulefile %s' % self.filename)
        statinfo = os.stat(self.filename)
        ctime = statinfo.st_ctime
        self.lastreload = ctime
        with open(self.filename, 'r') as fp:
            lines = fp.readlines()
        newpatterns = []

        for line in lines:
            line = line.strip()
            if line == "":
                continue
            if line.startswith('#'):
                continue

            # try advanced regex line
            #<headername> /regex/<flags> <arguments>
            try:
                tup = self._load_perlstyle_line(line)
                if tup is not None:
                    newpatterns.append(tup)
                    continue
            except Exception as e:
                self.logger.error(
                    "perl style line failed %s, error: %s" % (line, str(e)))
                continue

            # line shold be "headername    regex    arguments"
            try:
                tup = self._load_simplestyle_line(line)
                newpatterns.append(tup)
                continue
            except Exception as e:
                self.logger.error(str(e))
                continue

        self.patterns = newpatterns

    def strip_text(self, content, remove_tags=None, replace_nbsp=True, use_bfs=True):
        """Strip HTML Tags from content, replace newline with space (like Spamassassin)

        Returns:
            (unicode/str) Unicode string (Py3 'str' is unicode string)
        """

        if remove_tags is None:
            remove_tags = ['script', 'style']
        
        # try to generate string if we receive a header.
        if isinstance(content, Header):
            try:
                content = content.encode()
            except Exception as e:
                self.logger.debug('failed to encode header -> %s' % str(e))

        # make sure inputs are unicode, convert if needed
        content = force_uString(content)
        remove_tags = [force_uString(rtag) for rtag in remove_tags]

        content = content.replace("\n", " ")

        if HAVE_BEAUTIFULSOUP and use_bfs:
            soup = BeautifulSoup.BeautifulSoup(content, "lxml")
            for r in remove_tags:
                [x.extract() for x in soup.findAll(r)]

            
            stripped = soup.get_text()
            if replace_nbsp:
                stripped = stripped.replace(u'\xa0', u' ')
            return force_uString(stripped)

        # no BeautifulSoup available, let's try a modified version of pyzor's
        # html stripper
        stripper = HTMLStripper(strip_tags=remove_tags)

        try:
            # always try to replace nbsp as HTMLStripper would just remove them
            content = content.replace("&nbsp;", " ").replace("&#xa0;", " ").replace("&#160;", " ")
        except Exception:
            pass

        try:
            stripper.feed(content)
            return force_uString(stripper.get_stripped_data())
        except Exception:  # ignore parsing/encoding errors
            pass
        # use regex replace, make sure returned object is unicode string
        return force_uString(re.sub(self.stripre, '', content))

    def get_decoded_textparts(self, suspect, attachment=None, inline=None):
        """
        Get all text parts of suspect as a list. Text parts can be limited by the attachment, inline
        keywords which checks the Content-Disposition header:

        attachment: True/False/None
            None: Ignore
            True: attachment or header not present
            False: no attachment

        inline: True/False/None
            None: Ignore
            True: inline attachment
            False: no inline attachment or header present, so attached textparts are included

        Args:
            suspect (Suspect): Suspect object
            attachment (bool, NoneType): filter for attachments
            inline (bool, NoneType): filter for inline attachments

        The input should be a Suspect. Due to backward compatibility email.message.Message is still supported
        and passed to the deprecated routine which will however NOT handle the additional keyword parameters
        for filtering attachments and inline attachments.

        Returns:
            list: List containing decoded text parts

        """
        if not isinstance(suspect, Suspect):
            self.logger.warning("\"get_decoded_textparts\" called with object other than Suspect which is deprecated "
                                "and will be removed in near future...")
            if attachment is not None or inline is not None:
                raise DeprecationWarning
            return self.get_decoded_textparts_deprecated(suspect)

        textparts = []
        for attObj in suspect.att_mgr.get_objectlist():
            # filter for attachment attribute
            if attachment is not None and attachment != attObj.is_attachment:
                # skip if we ask for attachments but the object is not an attachment
                # skip if we ask for non-attachments but the object is an attachment (or no Content-Disposition header)
                continue

            if inline is not None and inline != attObj.is_inline:
                # skip if we ask for inline but the object is not inline
                # skip if we ask for non-inline but the object is inline (or no Content-Disposition header)
                continue

            if attObj.content_fname_check(maintype="text",ismultipart=False) \
                    or attObj.content_fname_check(maintype='multipart', subtype='mixed'):
                textparts.append(attObj.decoded_buffer_text)
        return textparts

    def get_decoded_textparts_deprecated(self, messagerep):
        """Returns a list of all text contents"""
        textparts = []
        for part in messagerep.walk():
            payload = None
            if part.get_content_maintype() == 'text' and (not part.is_multipart()):
                payload = part.get_payload(None, True)

            #multipart/mixed are text by default as well
            if part.get_content_maintype() == 'multipart' and part.get_content_subtype() == 'mixed':
                payload = part.get_payload(None, True)

            # payload can be None even if it was returned from part.get_payload()
            if payload is not None:
                # Try to decode using the given char set
                charset = part.get_content_charset("utf-8")
                payload = force_uString(payload,encodingGuess=charset)
                textparts.append(payload)
        return textparts

    def get_field(self, suspect, headername):
        """return a list of mail header values or special values. If the value can not be found, an empty list is returned.

        headers:
            just the headername or header:<headername> for standard message headers
            mime:headername for attached mime part headers

        envelope data:
            envelope_from (or from_address)
            envelope_to (or to_address)
            from_domain
            to_domain
            clientip
            clienthostname (fcrdns or 'unknown')
            clienthelo

        tags
            @tagname

        body source:
            body:full -> (full source, encoded)
            body:stripped (or just 'body') : -> returns text/* bodyparts with tags and newlines stripped
            body:raw -> decoded raw message body parts


        """

        # convert inputs to unicode if needed
        headername = force_uString(headername)

        # builtins
        if headername == u'envelope_from' or headername == u'from_address':
            return force_uString([suspect.from_address, ])
        if headername == u'envelope_to' or headername == u'to_address':
            return force_uString(suspect.recipients)
        if headername == u'from_domain':
            return force_uString([suspect.from_domain, ])
        if headername == u'to_domain':
            return force_uString([suspect.to_domain, ])
        if headername == u'body:full':
            return force_uString([suspect.get_original_source()])

        if headername in [u'clientip', u'clienthostname', u'clienthelo']:
            clinfo = suspect.get_client_info()
            if clinfo is None:
                return []
            if headername == u'clienthelo':
                return force_uString([clinfo[0], ])
            if headername == u'clientip':
                return force_uString([clinfo[1], ])
            if headername == u'clienthostname':
                return force_uString([clinfo[2], ])

        # if it starts with a @ we return a tag, not a header
        if headername[0:1] == u'@':
            tagname = headername[1:]
            tagval = suspect.get_tag(tagname)
            if tagval is None:
                return []
            if isinstance(tagval, list):
                return force_uString(tagval)
            return force_uString([tagval])

        messagerep = suspect.get_message_rep()

        # body rules on decoded text parts
        if headername == u'body:raw':
            return force_uString(self.get_decoded_textparts(suspect))

        if headername == u'body' or headername == u'body:stripped':
            return force_uString(list(map(self.strip_text, self.get_decoded_textparts(suspect))))

        if headername.startswith(u'mime:'):
            allvalues = []
            realheadername = headername[5:]
            for part in messagerep.walk():
                hdrslist = self._get_headers(realheadername, part)
                allvalues.extend(hdrslist)
            return force_uString(allvalues)

        # standard header
        # the header:<headername> alias is used in apply_template to distinguish from builtin variables
        if headername.startswith(u'header:'):
            headername=headername[7:]
        return force_uString(self._get_headers(headername, messagerep))

    def _get_headers(self, headername, payload):
        valuelist = []
        if '*' in headername:
            regex = re.escape(headername)
            regex = regex.replace('\*', '.*')
            patt = re.compile(regex, re.IGNORECASE)

            for h in list(payload.keys()):
                if re.match(patt, h) is not None:
                    valuelist.extend(payload.get_all(h,[]))
        else:
            valuelist = payload.get_all(headername,[])

        return valuelist

    def matches(self, suspect, extended=False):
        """returns (True,arg) if any regex matches, (False,None) otherwise

        if extended=True, returns all available info about the match in a tuple:
        True, (fieldname, matchedvalue, arg, regex)
        """
        self._reloadifnecessary()

        for tup in self.patterns:
            (fieldname, pattern, arg) = tup
            vals = self.get_field(suspect, fieldname)
            if vals is None or len(vals) == 0:
                self.logger.debug('No field %s found' % fieldname)
                continue

            for val in vals:
                if val is None:
                    continue
                try:
                    strval = str(val)
                    if pattern.search(strval):
                        self.logger.debug("""MATCH field %s (arg '%s') regex '%s' against value '%s'""" % (
                            fieldname, arg, pattern.pattern, val))
                        suspect.debug("message matches rule in %s: field=%s arg=%s regex=%s content=%s" % (
                            self.filename, fieldname, arg, pattern.pattern, val))
                        if extended:
                            return True, (fieldname, strval, arg, pattern.pattern)
                        else:
                            return True, arg
                    else:
                        self.logger.debug("""NO MATCH field %s (arg '%s') regex '%s' against value '%s'""" % (
                            fieldname, arg, pattern.pattern, val))
                except UnicodeEncodeError:
                    pass

        self.logger.debug('No match found')
        suspect.debug("message does not match any rule in %s" % self.filename)
        return False, None

    def get_args(self, suspect, extended=False):
        """returns all args of matched regexes in a list
        if extended=True:  returns a list of tuples with all available information:
        (fieldname, matchedvalue, arg, regex)
        """
        ret = []
        self._reloadifnecessary()
        for tup in self.patterns:
            (fieldname, pattern, arg) = tup
            vals = self.get_field(suspect, fieldname)
            if vals is None or len(vals) == 0:
                self.logger.debug('No field %s found' % fieldname)
                continue
            for val in vals:
                if val is None:
                    continue
                try:
                    strval = str(val)
                    if pattern.search(strval) is not None:
                        self.logger.debug("""MATCH field %s (arg '%s') regex '%s' against value '%s'""" % (
                            fieldname, arg, pattern.pattern, val))
                        suspect.debug("message matches rule in %s: field=%s arg=%s regex=%s content=%s" % (
                            self.filename, fieldname, arg, pattern.pattern, val))
                        if extended:
                            ret.append((fieldname, strval, arg, pattern.pattern))
                        else:
                            ret.append(arg)
                    else:
                        self.logger.debug("""NO MATCH field %s (arg '%s') regex '%s' against value '%s'""" % (
                            fieldname, arg, pattern.pattern, val))
                except UnicodeEncodeError:
                    pass

        return ret

    def getArgs(self, suspect):
        """old name for get_args"""
        return self.get_args(suspect)

    def file_changed(self):
        """Return True if the file has changed on disks since the last reload"""
        if not os.path.isfile(self.filename):
            return False
        statinfo = os.stat(self.filename)
        ctime = statinfo.st_ctime
        if ctime > self.lastreload:
            return True
        return False

    def lint(self):
        """check file and print warnings to console. returns True if everything is ok, False otherwise"""
        if not os.path.isfile(self.filename):
            print("SuspectFilter file not found: %s" % self.filename)
            return False
        with open(self.filename, 'r') as fp:
            lines = fp.readlines()
        lineno = 0
        for line in lines:
            lineno += 1
            line = line.strip()
            if line == "":
                continue
            if line.startswith('#'):
                continue
            try:
                tup = self._load_perlstyle_line(line)
                if tup is not None:
                    continue
                self._load_simplestyle_line(line)
            except Exception as e:
                print("Error in SuspectFilter file '%s', lineno %s , line '%s' : %s" % (
                    self.filename, lineno, line, str(e)))
                return False
        return True


class HTMLStripper(HTMLParser):

    def __init__(self, strip_tags=None):
        HTMLParser.__init__(self)
        self.strip_tags = strip_tags or ['script', 'style']
        self.reset()
        self.collect = True
        self.stripped_data = []

    def handle_data(self, data):
        if data and self.collect:
            self.stripped_data.append(data)

    def handle_starttag(self, tag, attrs):
        HTMLParser.handle_starttag(self, tag, attrs)
        if tag.lower() in self.strip_tags:
            self.collect = False

    def handle_endtag(self, tag):
        HTMLParser.handle_endtag(self, tag)
        if tag.lower() in self.strip_tags:
            self.collect = True

    def get_stripped_data(self):
        return ''.join(self.stripped_data)


class FileList(object):

    """Map all lines from a textfile into a list. If the file is changed, the list is refreshed automatically
    Each line can be run through a callback filter which can change or remove the content.

    filename: The textfile which should be mapped to a list. This can be changed at runtime. If None, an empty list will be returned.
    strip: remove leading/trailing whitespace from each line. Note that the newline character is always stripped
    skip_empty: skip empty lines (if used in combination with strip: skip all lines with only whitespace)
    skip_comments: skip lines starting with #
    lowercase: lowercase each line
    additional_filters: function or list of functions which will be called for each line on reload.
        Each function accept a single argument and must return a (possibly modified) line or None to skip this line
    minimum_time_between_reloads: number of seconds to cache the list before it will be reloaded if the file changes
    """

    def __init__(self, filename=None, strip=True, skip_empty=True, skip_comments=True, lowercase=False, additional_filters=None, minimum_time_between_reloads=5):
        self._filename = filename
        self.minium_time_between_reloads = minimum_time_between_reloads
        self._lastreload = 0
        self.linefilters = []
        self.content = []
        self.logger = logging.getLogger('%s.filelist' % __package__)
        self.lock = threading.Lock()

        # we always strip newline
        self.linefilters.append(lambda x: x.rstrip('\r\n'))

        if strip:
            self.linefilters.append(lambda x: x.strip())

        if skip_empty:
            self.linefilters.append(lambda x: x if x != '' else None)

        if skip_comments:
            self.linefilters.append(
                lambda x: None if x.strip().startswith('#') else x)

        if lowercase:
            self.linefilters.append(lambda x: x.lower())

        if additional_filters is not None:
            if isinstance(additional_filters, list):
                self.linefilters.extend(additional_filters)
            else:
                self.linefilters.append(additional_filters)

        if filename is not None:
            self._reload_if_necessary()


    @property
    def filename(self):
        return self._filename


    @filename.setter
    def filename(self, value):
        if self._filename != value:
            self._filename = value
            if value is not None:
                self._reload_if_necessary()
            else:
                self.content = []
                self._lastreload = 0


    def _reload_if_necessary(self):
        """Calls _reload if the file has been changed since the last reload"""
        now = time.time()
        # check if reloadinterval has passed
        if now - self._lastreload < self.minium_time_between_reloads:
            return False
        if not self.file_changed():
            return False
        if not self.lock.acquire():
            return False
        try:
            self._reload()
        finally:
            self.lock.release()
        return True


    def _reload(self):
        """Reload the file and build the list"""
        self.logger.info('Reloading file %s' % self.filename)
        statinfo = os.stat(self.filename)
        ctime = statinfo.st_ctime
        self._lastreload = ctime
        with open(self.filename, 'r') as fp:
            lines = fp.readlines()
        newcontent = []

        for line in lines:
            for func in self.linefilters:
                line = func(line)
                if line is None:
                    break

            if line is not None:
                newcontent.append(line)

        self.content = newcontent


    def file_changed(self):
        """Return True if the file has changed on disks since the last reload"""
        if not os.path.isfile(self.filename):
            return False
        statinfo = os.stat(self.filename)
        ctime = statinfo.st_ctime
        if ctime > self._lastreload:
            return True
        return False


    def get_list(self):
        """Returns the current list. If the file has been changed since the last call, it will rebuild the list automatically."""
        if self.filename is not None:
            self._reload_if_necessary()
        return self.content
    
    
    @staticmethod
    def inline_comments_filter(line):
        """
        Convenience function, strips comments from lines (e.g. everything after #)
        Pass to FileList() as additional_filter([FileList.inline_comments_filter])
        :param line: str: input line
        :return:  str or None
        """
        if '#' in line:
            idx = line.index('#')
            line = line[:idx].strip()
            if len(line) == 0:
                line = None
        return line



class Cache(object):
    """
    Simple local cache object.
    cached data will expire after a defined interval
    """

    def __init__(self, cachetime=30, cleanupinterval=300):
        self.cache={}
        self.cachetime=cachetime
        self.cleanupinterval=cleanupinterval
        self.lock=threading.Lock()
        self.logger=logging.getLogger("%s.settingscache" % __package__)

        t = threading.Thread(target=self.clear_cache_thread)
        t.daemon = True
        t.start()


    def put_cache(self,key,obj):
        try:
            gotlock=self.lock.acquire(True)
            if gotlock:
                self.cache[key]=(obj,time.time())
        except Exception as e:
            self.logger.exception(e)
        finally:
            self.lock.release()


    def get_cache(self,key):
        ret=None
        try:
            gotlock=self.lock.acquire(True)
            if not gotlock:
                return None

            if key in self.cache:
                obj,instime=self.cache[key]
                now=time.time()
                if now-instime<self.cachetime:
                    ret=obj
                else:
                    del self.cache[key]

        except Exception as e:
            self.logger.exception(e)
        finally:
            self.lock.release()
        return ret


    def clear_cache_thread(self):
        while True:
            time.sleep(self.cleanupinterval)
            now=time.time()
            cleancount=0
            try:
                gotlock=self.lock.acquire(True)
                if not gotlock:
                    continue

                for key in set(self.cache.keys()):
                    obj,instime=self.cache[key]
                    if now-instime>self.cachetime:
                        del self.cache[key]
                        cleancount+=1
            except Exception as e:
                self.logger.exception(e)
            finally:
                self.lock.release()
            self.logger.debug("Cleaned %s expired entries." % cleancount)



class CacheSingleton(object):
    """
    Process singleton to store a default Cache instance
    Note it is important there is a separate Cache instance for each process
    since otherwise the Threading.Lock will screw up and block the execution.
    """

    instance = None
    procPID = None

    def __init__(self, *args, **kwargs):
        pid =  os.getpid()
        logger = logging.getLogger("%s.CacheSingleton" % __package__)
        if pid == CacheSingleton.procPID and CacheSingleton.instance is not None:
            logger.debug("Return existing Cache Singleton for process with pid: %u"%pid)
        else:
            if CacheSingleton.instance is None:
                logger.info("Create CacheSingleton for process with pid: %u"%pid)
            elif CacheSingleton.procPID != pid:
                logger.warning("Replace CacheSingleton(created by process %u) for process with pid: %u"%(CacheSingleton.procPID,pid))

            CacheSingleton.instance = Cache(*args,**kwargs)
            CacheSingleton.procPID  = pid

    def __getattr__(self, name):
        return getattr(CacheSingleton.instance, name)


def get_default_cache():
    """
    Function to get processor unique Cache Singleton
    """
    return CacheSingleton()


def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    """
    Create hash using a iterator.
    Args:
        bytesiter (iterator): iterator for blocks of bytes, for example created by "file_as_blockiter"
        hasher (): a hasher, for example hashlib.md5
        ashexstr (bool): Creates hex hash if true

    Returns:

    """
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


def file_as_blockiter(afile, blocksize=65536):
    """
    Helper for hasher functions, to be able to iterate over a file
    in blocks of given size

    Args:
        afile (BytesIO): file buffer
        blocksize (int): block size in bytes

    Returns:
        iterator

    """
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def create_filehash(fnamelst, hashtype, ashexstr=False):
    """
    Create list of hashes for all files in list
    Args:
        fnamelst (list): list containing filenames
        fnamelst (hashtype): hashtype
        ashexstr (bool): create hex string if true

    Raises:
        KeyError if hashtype is not implemented

    Returns:
        list[(str,hash)]: List of tuples with filename and hashes
    """
    available_hashers = {"md5": hashlib.md5,
                         "sha1": hashlib.sha1}

    return [(fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')),
                                      available_hashers[hashtype](), ashexstr=ashexstr))
            for fname in fnamelst]
