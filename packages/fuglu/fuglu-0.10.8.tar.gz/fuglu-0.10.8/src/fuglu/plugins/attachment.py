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
from fuglu.shared import ScannerPlugin, DELETE, DUNNO, string_to_actioncode
from fuglu.bounce import Bounce
from fuglu.extensions.sql import SQL_EXTENSION_ENABLED, DBFile, DBConfig
from fuglu.extensions.filearchives import Archivehandle
from fuglu.extensions.filetype import filetype_handler
from fuglu.mailattach import NoExtractInfo
import re
import os
import os.path
import logging
import email
from threading import Lock

FUATT_NAMESCONFENDING = "-filenames.conf"
FUATT_CTYPESCONFENDING = "-filetypes.conf"
FUATT_ARCHIVENAMESCONFENDING = "-archivenames.conf"
FUATT_ARCHIVENAMES_CRYPTO_CONFENDING = "-archivenames-crypto.conf"
FUATT_ARCHIVECTYPESCONFENDING = "-archivefiletypes.conf"

FUATT_DEFAULT = u'default'

FUATT_ACTION_ALLOW = u'allow'
FUATT_ACTION_DENY = u'deny'
FUATT_ACTION_DELETE = u'delete'

FUATT_CHECKTYPE_FN = u'filename'
FUATT_CHECKTYPE_CT = u'contenttype'

FUATT_CHECKTYPE_ARCHIVE_CRYPTO_FN = u'archive-crypto-filename'
FUATT_CHECKTYPE_ARCHIVE_FN = u'archive-filename'
FUATT_CHECKTYPE_ARCHIVE_CT = u'archive-contenttype'

ATTACHMENT_DUNNO = 0
ATTACHMENT_BLOCK = 1
ATTACHMENT_OK = 2
ATTACHMENT_SILENTDELETE = 3

KEY_NAME = u"name"
KEY_CTYPE = u"ctype"
KEY_ARCHIVENAME = u"archive-name"
KEY_ARCHIVECTYPE = u"archive-ctype"
KEY_ENCARCHIVENAME = u"enc-archive-name"  # name rules for files in password protected archives


class RulesCache(object):

    """caches rule files"""

    __shared_state = {}

    def __init__(self, rulesdir, nocache: bool = False):
        """Nocache option can be useful for testing"""
        self.__dict__ = self.__shared_state
        if not hasattr(self, 'rules'):
            self.rules = {}
        if not hasattr(self, 'lock'):
            self.lock = Lock()
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(
                'fuglu.plugin.FiletypePlugin.RulesCache')
        if not hasattr(self, 'lastreload'):
            self.lastreload = 0
        self.rulesdir = rulesdir
        self._nocache = nocache
        self.reloadifnecessary()

    def getRules(self, ruletype, key):
        self.logger.debug('Rule cache request: [%s] [%s]' % (ruletype, key))
        if ruletype not in self.rules:
            self.logger.error('Invalid rule type requested: %s' % ruletype)
            return None
        if key not in self.rules[ruletype]:
            self.logger.debug(
                'Ruleset not found : [%s] [%s]' % (ruletype, key))
            return None
        self.logger.debug('Ruleset found : [%s] [%s] ' % (ruletype, key))

        ret = self.rules[ruletype][key]
        return ret

    def getCTYPERules(self, key):
        return self.getRules(KEY_CTYPE, key)

    def getARCHIVECTYPERules(self, key):
        return self.getRules(KEY_ARCHIVECTYPE, key)

    def getNAMERules(self, key):
        return self.getRules(KEY_NAME, key)

    def getARCHIVENAMERules(self, key):
        return self.getRules(KEY_ARCHIVENAME, key)

    def getEcryptedARCHIVENAMERules(self, key):
        return self.getRules(KEY_ENCARCHIVENAME, key)

    def reloadifnecessary(self):
        """reload rules if file changed"""
        if not self.rulesdirchanged():
            return
        if not self.lock.acquire():
            return
        try:
            self._loadrules()
        finally:
            self.lock.release()

    def rulesdirchanged(self):
        dirchanged = False
        # if _nocache is True never cache (debugging only)
        if self._nocache:
            return True
        try:
            statinfo = os.stat(self.rulesdir)
        except FileNotFoundError:
            pass
        else:
            ctime = statinfo.st_ctime
            if ctime > self.lastreload:
                dirchanged = True
        return dirchanged

    def _loadrules(self):
        """effectively loads the rules, do not call directly, only through reloadifnecessary"""
        self.logger.debug('Reloading attachment rules...')

        # set last timestamp
        statinfo = os.stat(self.rulesdir)
        ctime = statinfo.st_ctime
        self.lastreload = ctime

        filelist = os.listdir(self.rulesdir)

        newruleset = {KEY_NAME: {}, KEY_CTYPE: {},
                      KEY_ARCHIVENAME: {}, KEY_ARCHIVECTYPE: {},
                      KEY_ENCARCHIVENAME: {}}

        rulecounter = 0
        okfilecounter = 0
        ignoredfilecounter = 0

        for filename in filelist:
            endingok = False
            for ending in FUATT_NAMESCONFENDING, FUATT_CTYPESCONFENDING, FUATT_ARCHIVENAMESCONFENDING, FUATT_ARCHIVECTYPESCONFENDING, FUATT_ARCHIVENAMES_CRYPTO_CONFENDING :
                if filename.endswith(ending):
                    endingok = True
                    break

            if endingok:
                okfilecounter += 1
            else:
                ignoredfilecounter += 1
                self.logger.debug('Ignoring file %s' % filename)
                continue

            ruleset = self._loadonefile("%s/%s" % (self.rulesdir, filename))
            if ruleset is None:
                continue
            rulesloaded = len(ruleset)
            self.logger.debug('%s rules loaded from file %s' %
                              (rulesloaded, filename))
            ruletype = KEY_NAME
            key = filename[0:-len(FUATT_NAMESCONFENDING)]
            if filename.endswith(FUATT_CTYPESCONFENDING):
                ruletype = KEY_CTYPE
                key = filename[0:-len(FUATT_CTYPESCONFENDING)]
            elif filename.endswith(FUATT_ARCHIVENAMESCONFENDING):
                ruletype = KEY_ARCHIVENAME
                key = filename[0:-len(FUATT_ARCHIVENAMESCONFENDING)]
            elif filename.endswith(FUATT_ARCHIVENAMES_CRYPTO_CONFENDING):
                ruletype = KEY_ENCARCHIVENAME
                key = filename[0:-len(FUATT_ARCHIVENAMES_CRYPTO_CONFENDING)]
            elif filename.endswith(FUATT_ARCHIVECTYPESCONFENDING):
                ruletype = KEY_ARCHIVECTYPE
                key = filename[0:-len(FUATT_ARCHIVECTYPESCONFENDING)]

            newruleset[ruletype][key] = ruleset
            self.logger.debug('Updating cache: [%s][%s]' % (ruletype, key))
            rulecounter += rulesloaded

        self.rules = newruleset
        self.logger.info('Loaded %s rules from %s files in %s (%s files ignored)' %
                         (rulecounter, okfilecounter,  self.rulesdir, ignoredfilecounter))

    def _loadonefile(self, filename):
        """returns all rules in a file"""
        if not os.path.exists(filename):
            self.logger.error('Rules File %s does not exist' % filename)
            return None
        if not os.path.isfile(filename):
            self.logger.warning('Ignoring file %s - not a file' % filename)
            return None
        with open(filename) as handle:
            rules = self.get_rules_from_config_lines(handle.readlines())
        return rules

    def get_rules_from_config_lines(self, lineslist):
        ret = []
        for line in lineslist:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            tpl = line.split(None, 2)
            if len(tpl) != 3:
                self.logger.debug(
                    'Ignoring invalid line  (length %s): %s' % (len(tpl), line))
                continue
            (action, regex, description) = tpl
            action = action.lower()
            if action not in [FUATT_ACTION_ALLOW, FUATT_ACTION_DENY, FUATT_ACTION_DELETE]:
                self.logger.error('Invalid rule action: %s' % action)
                continue

            tp = (action, regex, description)
            ret.append(tp)
        return ret


class FiletypePlugin(ScannerPlugin):

    """This plugin checks message attachments. You can configure what filetypes or filenames are allowed to pass through fuglu. If a attachment is not allowed, the message is deleted and the sender receives a bounce error message. The plugin uses the '''file''' library to identify attachments, so even if a smart sender renames his executable to .txt, fuglu will detect it.

Attachment rules can be defined globally, per domain or per user.

Actions: This plugin will delete messages if they contain blocked attachments.

Prerequisites: You must have the python ``file`` or ``magic`` module installed. Additionaly, for scanning filenames within rar archives, fuglu needs the python ``rarfile`` module.


The attachment configuration files are in ``/etc/fuglu/rules``. You should have two default files there: ``default-filenames.conf`` which defines what filenames are allowed and ``default-filetypes.conf`` which defines what content types a attachment may have.

For domain rules, create a new file ``<domainname>-filenames.conf`` / ``<domainname>-filetypes.conf`` , eg. ``fuglu.org-filenames.conf`` / ``fuglu.org-filetypes.conf``

For individual user rules, create a new file ``<useremail>-filenames.conf`` / ``<useremail>-filetypes.conf``, eg. ``oli@fuglu.org-filenames.conf`` / ``oli@fuglu.org-filetypes.conf``

To scan filenames or even file contents within archives (zip, rar), use ``<...>-archivefilenames.conf`` and ``<...>-archivefiletypes.conf``.


The format of those files is as follows: Each line should have three parts, seperated by tabs (or any whitespace):
``<action>``    ``<regular expression>``   ``<description or error message>``

``<action>`` can be one of:
 * allow : this file is ok, don't do further checks (you might use it for safe content types like text). Do not blindly create 'allow' rules. It's safer to make no rule at all, if no other rules hit, the file will be accepted
 * deny : delete this message and send the error message/description back to the sender
 * delete : silently delete the message, no error is sent back, and 'blockaction' is ignored


``<regular expression>`` is a standard python regex. in ``x-filenames.conf`` this will be applied to the attachment name . in ``x-filetypes.conf`` this will be applied to the mime type of the file as well as the file type returned by the ``file`` command.

Example of ``default-filetypes.conf`` :

::

    allow    text        -        
    allow    \bscript    -        
    allow    archive        -            
    allow    postscript    -            
    deny    self-extract    No self-extracting archives
    deny    executable    No programs allowed
    deny    ELF        No programs allowed
    deny    Registry    No Windows Registry files allowed



A small extract from ``default-filenames.conf``:

::

    deny    \.ico$            Windows icon file security vulnerability    
    deny    \.ani$            Windows animated cursor file security vulnerability    
    deny    \.cur$            Windows cursor file security vulnerability    
    deny    \.hlp$            Windows help file security vulnerability

    allow    \.jpg$            -    
    allow    \.gif$            -    



Note: The files will be reloaded automatically after a few seconds (you do not need to kill -HUP / restart fuglu)

Per domain/user overrides can also be fetched from a database instead of files (see dbconnectstring / query options).
The query must return the same rule format as a file would. Multiple columns in the resultset will be concatenated.

The default query assumes the following schema:

::

    CREATE TABLE `attachmentrules` (
      `rule_id` int(11) NOT NULL AUTO_INCREMENT,
      `action` varchar(10) NOT NULL,
      `regex` varchar(255) NOT NULL,
      `description` varchar(255) DEFAULT NULL,
      `scope` varchar(255) DEFAULT NULL,
      `checktype` varchar(20) NOT NULL,
      `prio` int(11) NOT NULL,
      PRIMARY KEY (`rule_id`)
    )

*action*: ``allow``, ``deny``, or ``delete``

*regex*: a regular expression

*description*: description/explanation of this rule which is optionally sent back to the sender if bounces are enabled

*scope*: a domain name or a recipient's email address

*checktype*: one of ``filename``,``contenttype``,``archive-filename``,``archive-contenttype``

*prio*: order in which the rules are run

The bounce template (eg ``/etc/fuglu/templates/blockedfile.tmpl`` ) should
start by defining the headers, followed by a blank line, then the message body for your bounce message. Something like this:

::

    To: ${from_address}
    Subject: Blocked attachment

    Your message to ${to_address} contains a blocked attachment and has not been delivered.

    ${blockinfo}



``${blockinfo}`` will be replaced with the text you specified in the third column of the rule that blocked this message.

The other common template variables are available as well.


"""

    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.requiredvars = {
            'template_blockedfile': {
                'default': '/etc/fuglu/templates/blockedfile.tmpl',
                'description': 'Mail template for the bounce to inform sender about blocked attachment',
            },

            'sendbounce': {
                'default': 'True',
                'description': 'inform the sender about blocked attachments.\nIf a previous plugin tagged the message as spam or infected, no bounce will be sent to prevent backscatter',
            },

            'rulesdir': {
                'default': '/etc/fuglu/rules',
                'description': 'directory that contains attachment rules',
            },

            'blockaction': {
                'default': 'DELETE',
                'description': 'what should the plugin do when a blocked attachment is detected\nREJECT : reject the message (recommended in pre-queue mode)\nDELETE : discard messages\nDUNNO  : mark as blocked but continue anyway (eg. if you have a later quarantine plugin)',
            },

            'dbconnectstring': {
                'default': '',
                'description': 'sqlalchemy connectstring to load rules from a database and use files only as fallback. requires SQL extension to be enabled',
                'confidential': True,
            },

            'query': {
                'default': 'SELECT action,regex,description FROM attachmentrules WHERE scope=:scope AND checktype=:checktype ORDER BY prio',
                'description': "sql query to load rules from a db. #:scope will be replaced by the recipient address first, then by the recipient domain\n:check will be replaced 'filename','contenttype','archive-filename' or 'archive-contenttype'",
            },

            'checkarchivenames': {
                'default': 'False',
                'description': "enable scanning of filenames within archives (zip,rar). This does not actually extract the files, it just looks at the filenames found in the archive."
            },

            'checkarchivecontent': {
                'default': 'False',
                'description': 'extract compressed archives(zip,rar) and check file content type with libmagics\nnote that the files will be extracted into memory - tune archivecontentmaxsize  accordingly.\nfuglu does not extract archives within the archive(recursion)',
            },

            'archivecontentmaxsize': {
                'default': '5000000',
                'description': 'only extract and examine files up to this amount of (uncompressed) bytes',
            },

            'archiveextractlevel': {
                'default': '1',
                'description': 'recursive extraction level for archives. Undefined or negative value means extract until it\'s not an archive anymore'
            },

            'enabledarchivetypes': {
                'default': '',
                'description': 'comma separated list of archive extensions. do only process archives of given types.',
            }

        }

        self.logger = self._logger()
        self.rulescache = None
        self.extremeverbosity = False
        self.blockedfiletemplate = ''
        self.sendbounce = True
        self.checkarchivenames = False
        self.checkarchivecontent = False


        # copy dict with available extensions from Archivehandle
        # (deepcopy is not needed here although in general it is a good idea
        # to use it in case a dict contains another dict)
        #
        # key: file ending, value: archive type
        self.active_archive_extensions = dict(Archivehandle.avail_archive_extensions)


    def examine(self, suspect):
        if self.rulescache is None:
            self.rulescache = RulesCache(
                self.config.get(self.section, 'rulesdir'))

        self.blockedfiletemplate = self.config.get(
            self.section, 'template_blockedfile')

        runtimeconfig = DBConfig(self.config, suspect)
        self.checkarchivenames = runtimeconfig.getboolean(self.section, 'checkarchivenames')
        self.checkarchivecontent = runtimeconfig.getboolean(self.section, 'checkarchivecontent')
        self.sendbounce = runtimeconfig.getboolean(self.section, 'sendbounce')

        enabledarchivetypes = runtimeconfig.get(self.section, 'enabledarchivetypes')
        if enabledarchivetypes:
            enabled = [t.strip() for t in enabledarchivetypes.split(',')]
            archtypes = list(self.active_archive_extensions.keys())
            for archtype in archtypes:
                if archtype not in enabled:
                    del self.active_archive_extensions[archtype]

        returnaction = self.walk(suspect)
        return returnaction
    
    
    def asciionly(self, stri):
        """return stri with all non-ascii chars removed"""
        if isinstance(stri, str):
            return stri.encode('ascii', 'ignore').decode()
        elif isinstance(stri, bytes):  # python3
            # A bytes object therefore already ascii, but not a string yet
            return stri.decode('ascii', 'ignore')
        return "".join([x for x in stri if ord(x) < 128])
    
    
    def _tostr(self, stri):
        if isinstance(stri, bytes): # python3 bytes object
            stri = stri.decode('utf-8', 'ignore')
        return stri
    
    
    def matchRules(self, ruleset, obj, suspect, attachmentname=None):
        if attachmentname is None:
            attachmentname = ""
        attachmentname = self.asciionly(attachmentname)

        if obj is None:
            self.logger.warning(
                "%s: message has unknown name or content-type attachment %s" % (suspect.id, attachmentname))
            return ATTACHMENT_DUNNO

        # remove non ascii chars
        asciirep = self.asciionly(obj)

        displayname = attachmentname
        if asciirep == attachmentname:
            displayname = ''

        if ruleset is None:
            return ATTACHMENT_DUNNO

        for action, regex, description in ruleset:
            # database description, displayname and asciirep may be unicode
            description = self._tostr(description)
            displayname = self._tostr(displayname)
            asciirep = self._tostr(asciirep)

            prog = re.compile(regex, re.I)
            if self.extremeverbosity:
                self.logger.debug('%s Attachment %s Rule %s' % (suspect.id, obj, regex))
            if isinstance(obj, bytes):
                obj = obj.decode('UTF-8', 'ignore')
            if prog.search(obj):
                self.logger.debug('%s Rulematch: Attachment=%s Rule=%s Description=%s Action=%s' % (
                    suspect.id, obj, regex, description, action))
                suspect.debug('%s Rulematch: Attachment=%s Rule=%s Description=%s Action=%s' % (
                    suspect.id, obj, regex, description, action))
                if action == 'deny':
                    self.logger.info('%s contains blocked attachment %s %s' % (
                        suspect.id, displayname, asciirep))
                    suspect.tags['blocked']['FiletypePlugin'] = True
                    blockinfo = ("%s %s: %s" % (displayname, asciirep, description)).strip()
                    suspect.tags['FiletypePlugin.errormessage'] = blockinfo
                    if self.sendbounce:
                        if suspect.is_spam() or suspect.is_virus():
                            self.logger.info(f"{suspect.id} backscatter prevention: not sending attachment block "
                                             f"bounce to {suspect.from_address} - the message is tagged spam or virus")
                        elif not suspect.from_address:
                            self.logger.warning(f"{suspect.id}, not sending attachment block bounce to empty recipient")
                        else:
                            # check if another attachment blocker has already sent a bounce
                            queueid = suspect.get_tag('Attachment.bounce.queueid')
                            if queueid:
                                self.logger.info(f'{suspect.id} already sent attachment block bounce '
                                                 f'to {suspect.from_address} with queueid {queueid}')
                            else:
                                self.logger.debug(f"{suspect.id} sending attachment block "
                                                  f"bounce to {suspect.from_address}")
                                bounce = Bounce(self.config)
                                queueid = bounce.send_template_file(suspect.from_address,
                                                                    self.blockedfiletemplate,
                                                                    suspect,
                                                                    dict(blockinfo=blockinfo))
                                self.logger.info(f'{suspect.id} sent attachment block bounce '
                                                 f'to {suspect.from_address} with queueid {queueid}')
                                suspect.set_tag('Attachment.bounce.queueid', queueid)
                    return ATTACHMENT_BLOCK

                if action == 'delete':
                    self.logger.info(
                        '%s contains blocked attachment %s %s -- SILENT DELETE! --' % (suspect.id, displayname, asciirep))
                    return ATTACHMENT_SILENTDELETE

                if action == 'allow':
                    return ATTACHMENT_OK
        return ATTACHMENT_DUNNO
    
    
    def matchMultipleSets(self, setlist, obj, suspect, attachmentname=None):
        """run through multiple sets and return the first action which matches obj"""
        self.logger.debug(
            '%s Checking object %s against attachment rulesets' % (suspect.id, obj))
        for ruleset in setlist:
            res = self.matchRules(ruleset, obj, suspect, attachmentname)
            if res != ATTACHMENT_DUNNO:
                return res
        return ATTACHMENT_DUNNO
    
    
    def walk(self, suspect):
        """walks through a message and checks each attachment according to the rulefile specified in the config"""

        blockaction = self.config.get(self.section, 'blockaction')
        blockactioncode = string_to_actioncode(blockaction)

        # try db rules first
        self.rulescache.reloadifnecessary()
        dbconn = ''
        if self.config.has_option(self.section, 'dbconnectstring'):
            dbconn = self.config.get(self.section, 'dbconnectstring')

        if dbconn.strip() != '':
            self.logger.debug('%s Loading attachment rules from database' % suspect.id)
            query = self.config.get(self.section, 'query')
            dbfile = DBFile(dbconn, query)
            user_names = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_address, 'checktype': FUATT_CHECKTYPE_FN}))
            user_ctypes = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_address, 'checktype': FUATT_CHECKTYPE_CT}))
            user_archive_names = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_address, 'checktype': FUATT_CHECKTYPE_ARCHIVE_FN}))
            user_archive_crypto_names = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_address, 'checktype': FUATT_CHECKTYPE_ARCHIVE_CRYPTO_FN}))
            user_archive_ctypes = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_address, 'checktype': FUATT_CHECKTYPE_ARCHIVE_CT}))
            self.logger.debug('%s Found %s filename rules, %s content-type rules, %s archive filename rules, %s archive content rules for address %s' %
                              (suspect.id, len(user_names), len(user_ctypes), len(user_archive_names), len(user_archive_ctypes), suspect.to_address))

            domain_names = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_domain, 'checktype': FUATT_CHECKTYPE_FN}))
            domain_ctypes = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_domain, 'checktype': FUATT_CHECKTYPE_CT}))
            domain_archive_names = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_domain, 'checktype': FUATT_CHECKTYPE_ARCHIVE_FN}))
            domain_archive_crypto_names = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_domain, 'checktype': FUATT_CHECKTYPE_ARCHIVE_CRYPTO_FN}))
            domain_archive_ctypes = self.rulescache.get_rules_from_config_lines(
                dbfile.getContent({'scope': suspect.to_domain, 'checktype': FUATT_CHECKTYPE_ARCHIVE_CT}))
            self.logger.debug('%s Found %s filename rules, %s content-type rules, %s archive filename rules, %s archive content rules for domain %s' %
                              (suspect.id, len(domain_names), len(domain_ctypes), len(domain_archive_names), len(domain_archive_ctypes), suspect.to_domain))
        else:
            self.logger.debug('%s Loading attachment rules from filesystem dir %s' % (suspect.id, self.config.get(self.section,'rulesdir')))
            user_names = self.rulescache.getNAMERules(suspect.to_address)
            user_ctypes = self.rulescache.getCTYPERules(suspect.to_address)
            user_archive_names = self.rulescache.getARCHIVENAMERules(
                suspect.to_address)
            user_archive_crypto_names = self.rulescache.getEcryptedARCHIVENAMERules(
                suspect.to_address)
            user_archive_ctypes = self.rulescache.getARCHIVECTYPERules(
                suspect.to_address)

            domain_names = self.rulescache.getNAMERules(suspect.to_domain)
            domain_ctypes = self.rulescache.getCTYPERules(suspect.to_domain)
            domain_archive_names = self.rulescache.getARCHIVENAMERules(
                suspect.to_domain)
            domain_archive_crypto_names = self.rulescache.getEcryptedARCHIVENAMERules(
                suspect.to_domain)
            domain_archive_ctypes = self.rulescache.getARCHIVECTYPERules(
                suspect.to_domain)

        # always get defaults from file
        default_names = self.rulescache.getNAMERules(FUATT_DEFAULT)
        default_ctypes = self.rulescache.getCTYPERules(FUATT_DEFAULT)
        default_archive_names = self.rulescache.getARCHIVENAMERules(
            FUATT_DEFAULT)
        default_archive_crypto_names = self.rulescache.getEcryptedARCHIVENAMERules(
            FUATT_DEFAULT)
        default_archive_ctypes = self.rulescache.getARCHIVECTYPERules(
            FUATT_DEFAULT)

        # get mail attachment objects (only directly attached objects)
        for attObj in suspect.att_mgr.get_objectlist():
            contenttype_mime = attObj.contenttype_mime
            att_name = attObj.filename
            
            if attObj.is_inline or attObj.is_attachment or not attObj.filename_generated:
                # process all attachments marked as "inline", "attachment" or parts
                # with filenames that are not auto-generated
                pass
            else:
                self.logger.debug("%s Skip message object: %s (attachment: %s, inline: %s, auto-name: %s)" % (
                    suspect.id, att_name, attObj.is_attachment, attObj.is_inline, attObj.filename_generated
                ))
                continue
                

            att_name = self.asciionly(att_name)

            res = self.matchMultipleSets(
                [user_names, domain_names, default_names], att_name, suspect, att_name)
            if res == ATTACHMENT_SILENTDELETE:
                self._debuginfo(
                    suspect, "Attachment name=%s SILENT DELETE : blocked by name" % att_name)
                return DELETE
            if res == ATTACHMENT_BLOCK:
                self._debuginfo(
                    suspect, "Attachment name=%s : blocked by name)" % att_name)
                message = suspect.tags['FiletypePlugin.errormessage']
                return blockactioncode, message

            # go through content type rules
            res = self.matchMultipleSets(
                [user_ctypes, domain_ctypes, default_ctypes], contenttype_mime, suspect, att_name)
            if res == ATTACHMENT_SILENTDELETE:
                self._debuginfo(
                    suspect, "Attachment name=%s content-type=%s SILENT DELETE: blocked by mime content type (message source)" % (att_name, contenttype_mime))
                return DELETE
            if res == ATTACHMENT_BLOCK:
                self._debuginfo(
                    suspect, "Attachment name=%s content-type=%s : blocked by mime content type (message source)" % (att_name, contenttype_mime))
                message = suspect.tags['FiletypePlugin.errormessage']
                return blockactioncode, message

            contenttype_magic = attObj.contenttype
            if contenttype_magic is not None:
                res = self.matchMultipleSets(
                    [user_ctypes, domain_ctypes, default_ctypes], contenttype_magic, suspect, att_name)
                if res == ATTACHMENT_SILENTDELETE:
                    self._debuginfo(
                        suspect, "Attachment name=%s content-type=%s SILENT DELETE: blocked by mime content type (magic)" % (att_name, contenttype_magic))
                    return DELETE
                if res == ATTACHMENT_BLOCK:
                    self._debuginfo(
                        suspect, "Attachment name=%s content-type=%s : blocked by mime content type (magic)" % (att_name, contenttype_magic))
                    message = suspect.tags['FiletypePlugin.errormessage']
                    return blockactioncode, message

            # archives
            if self.checkarchivenames or self.checkarchivecontent:

                #if archive_type is not None:
                if attObj.is_archive:

                    # check if extension was used to determine archive type and
                    # if yes, check if extension is enabled. This code
                    # is here to remain backward compatible in the behavior. It
                    # is recommended to define inactive archive-types and -extensions
                    # differently
                    if attObj.atype_fromext() is not None:
                        if not attObj.atype_fromext() in self.active_archive_extensions.keys():
                            # skip if extension is not in active list
                            continue


                    self.logger.debug("%s Extracting %s as %s" % (suspect.id, att_name,attObj.archive_type))
                    archivecontentmaxsize = self.config.getint(self.section, 'archivecontentmaxsize')
                    try:
                        archiveextractlevel = self.config.getint(self.section, 'archiveextractlevel')
                        if archiveextractlevel < 0: # value must be greater or equals 0
                            archiveextractlevel = None
                    except Exception:
                        archiveextractlevel = None
                        
                    try:


                        if self.checkarchivenames:
                            # here, check all the filenames, independent of how many files we would extract
                            # by the limits (att_mgr_default_maxnfiles, att_mgr_hard_maxnfiles)
                            if self.checkarchivecontent:
                                namelist = attObj.get_fileslist(0, archiveextractlevel, archivecontentmaxsize, None)
                            else:
                                namelist = attObj.fileslist_archive
                            passwordprotected = attObj.is_protected_archive
                            self.logger.debug(f"{suspect.id} Is {att_name} password protected: {passwordprotected}")
                            ruleset = [user_archive_names, domain_archive_names, default_archive_names]
                            if passwordprotected:
                                ruleset.extend([user_archive_crypto_names,
                                                domain_archive_crypto_names,
                                                default_archive_crypto_names])

                            for name in namelist:
                                res = self.matchMultipleSets(ruleset, name, suspect, name)
                                if res == ATTACHMENT_SILENTDELETE:
                                    self._debuginfo(
                                        suspect, "Blocked filename in archive %s SILENT DELETE" % att_name)
                                    return DELETE
                                if res == ATTACHMENT_BLOCK:
                                    self._debuginfo(
                                        suspect, "Blocked filename in archive %s" % att_name)
                                    message = suspect.tags['FiletypePlugin.errormessage']
                                    return blockactioncode, message

                        if filetype_handler.available() and self.checkarchivecontent:

                            maxnfiles2extract = suspect.att_mgr.get_maxfilenum_extract(None)
                            nocheckinfo = NoExtractInfo()
                            for archObj in attObj.get_objectlist(0, archiveextractlevel, archivecontentmaxsize,
                                                                 maxnfiles2extract, noextractinfo=nocheckinfo):
                                safename = self.asciionly(archObj.filename)
                                contenttype_magic = archObj.contenttype

                                # Keeping this check for backward compatibility
                                # This could easily be removed since memory is used anyway
                                if archivecontentmaxsize is not None and archObj.filesize > archivecontentmaxsize:
                                    nocheckinfo.append(archObj.filename, u"toolarge",
                                                       u"already extracted but too large for check: %u > %u"
                                                       % (archObj.filesize, archivecontentmaxsize))
                                    continue

                                res = self.matchMultipleSets(
                                    [user_archive_ctypes, domain_archive_ctypes, default_archive_ctypes],
                                    contenttype_magic, suspect, safename)
                                if res == ATTACHMENT_SILENTDELETE:
                                    self._debuginfo(
                                        suspect, "Extracted file %s from archive %s content-type=%s "
                                                 "SILENT DELETE: blocked by mime content type (magic)"
                                                 % (safename, att_name, contenttype_magic))
                                    return DELETE
                                if res == ATTACHMENT_BLOCK:
                                    self._debuginfo(
                                        suspect, "Extracted file %s from archive %s content-type=%s : "
                                                 "blocked by mime content type (magic)"
                                                 % (safename, att_name, contenttype_magic))
                                    message = suspect.tags['FiletypePlugin.errormessage']
                                    return blockactioncode, message

                            for item in nocheckinfo.get_filtered():
                                try:
                                    self._debuginfo(suspect, 'Archive File not checked: reason: %s -> %s'
                                                    % (item[0], item[1]))
                                except Exception as e:
                                    self._debuginfo(suspect, 'Archive File not checked: %s' % str(e))

                    except Exception as e:
                        self.logger.error("%s archive scanning failed in attachment %s: %s" % (suspect.id, att_name, str(e)))
        return DUNNO
    
    def walk_all_parts(self, message):
        """Like email.message.Message's .walk() but also tries to find parts in the message's epilogue"""
        for part in message.walk():
            yield part

        boundary = message.get_boundary()
        epilogue = message.epilogue
        if epilogue is None or boundary not in epilogue:
            return

        candidate_parts = epilogue.split(boundary)
        for candidate in candidate_parts:
            try:
                part_content = candidate.strip()
                if part_content.lower().startswith('content'):
                    message = email.message_from_string(part_content)
                    yield message

            except Exception as e:
                self.logger.info("hidden part extraction failed: %s"%str(e))


    def _debuginfo(self, suspect, message):
        """Debug to log and suspect"""
        suspect.debug(message)
        self.logger.debug('%s %s' % (suspect.id, message))
    
    
    def __str__(self):
        return "Attachment Blocker"
    
    
    def lint(self):
        allok = self.check_config() and self.lint_magic() and self.lint_sql() and self.lint_archivetypes()
        return allok
    
    
    def lint_magic(self):
        # the lint routine for magic is now implemented in "filetype.ThreadLocalMagic.lint" and can
        # be called using the global object "filetype_handler"
        return filetype_handler.lint()

    def lint_archivetypes(self):
        if not Archivehandle.avail('rar'):
            print("rarfile library not found, RAR support disabled")
        if not Archivehandle.avail('7z'):
            print("pylzma/py7zlip library not found, 7z support disabled")
        print("Archive scan, available file extensions: %s" % (",".join(sorted(Archivehandle.avail_archive_extensions_list))))
        print("Archive scan, active file extensions:    %s" % (",".join(sorted(self.active_archive_extensions.keys()))))
        return True
    
    
    def lint_sql(self):
        dbconn = ''
        if self.config.has_option(self.section, 'dbconnectstring'):
            dbconn = self.config.get(self.section, 'dbconnectstring')
        if dbconn.strip() != '':
            print("Reading per user/domain attachment rules from database")
            if not SQL_EXTENSION_ENABLED:
                print("Fuglu SQL Extension not available, cannot load attachment rules from database")
                return False
            query = self.config.get(self.section, 'query')
            dbfile = DBFile(dbconn, query)
            try:
                dbfile.getContent(
                    {'scope': 'lint', 'checktype': FUATT_CHECKTYPE_FN})
            except Exception as e:
                import traceback
                print(
                    "Could not get attachment rules from database. Exception: %s" % str(e))
                print(traceback.format_exc())
                return False
        else:
            print("No database configured. Using per user/domain file configuration from %s" %
                  self.config.get(self.section, 'rulesdir'))
        return True
