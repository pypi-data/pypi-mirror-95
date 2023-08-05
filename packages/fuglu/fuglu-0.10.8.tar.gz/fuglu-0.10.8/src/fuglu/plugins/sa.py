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
from fuglu.shared import ScannerPlugin, DUNNO, DEFER, Suspect, string_to_actioncode, apply_template
from fuglu.extensions.sql import DBConfig, get_session, SQL_EXTENSION_ENABLED
from fuglu.stringencode import force_bString, force_uString
from string import Template
import time
import socket
import email
import re
import os
from fuglu.lib.patchedemail import PatchedMessage
from email.mime.text import MIMEText

GTUBE = """Date: Mon, 08 Sep 2008 17:33:54 +0200
To: oli@unittests.fuglu.org
From: oli@unittests.fuglu.org
Subject: test scanner

  XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X
"""



class SAPlugin(ScannerPlugin):

    """This plugin passes suspects to spamassassin daemon.

Prerequisites: SPAMD must be installed and running (not necessarily on the same box as fuglu)

Notes for developers:

if forwardoriginal=False, the message source will be completely replaced with the answer from spamd.

Tags:

 * reads ``SAPlugin.skip``, (boolean) skips scanning if this is True
 * reads ``SAPlugin.tempheader``, (text) prepends this text to the scanned message (use this to pass temporary headers to spamassassin which should not be visible in the final message)
 * sets ``spam['spamassassin']`` (boolean)
 * sets ``SAPlugin.spamscore`` (float) if possible
 * sets ``SAPlugin.skipreason`` (string) if the message was not scanned (fuglu >0.5.0)
 * sets ``SAPlugin.report``, (string) report from spamd or spamheader (where score was found) depending on forwardoriginal setting
"""

    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.requiredvars = {
            'host': {
                'default': 'localhost',
                'description': 'hostname where spamd runs',
            },

            'port': {
                'default': '783',
                'description': "tcp port number or path to spamd unix socket",
            },

            'timeout': {
                'default': '30',
                'description': 'how long should we wait for an answer from sa',
            },

            'maxsize': {
                'default': '256000',
                'description': "maximum size in bytes. larger messages will be skipped",
            },

            'strip_oversize':{
                'default': '1',
                'description': "enable scanning of messages larger than maxsize. all attachments will be stripped and only headers, plaintext and html part will be scanned. If message is still oversize it will be truncated.",
            },

            'retries': {
                'default': '3',
                'description': 'how often should fuglu retry the connection before giving up',
            },

            'scanoriginal': {
                'default': 'True',
                'description': "should we scan the original message as retreived from postfix or scan the current state \nin fuglu (which might have been altered by previous plugins)\nonly set this to disabled if you have a custom plugin that adds special headers to the message that will be \nused in spamassassin rules",
            },

            'forwardoriginal': {
                'default': 'False',
                'description': """forward the original message or replace the content as returned by spamassassin\nif this is enabled, no spamassassin headers will be visible in the final message.\n"original" in this case means "as passed to spamassassin", eg. if 'scanoriginal' above is disabled this will forward the\nmessage as retreived from previous plugins """,
            },

            'spamheader': {
                'default': 'X-Spam-Status',
                'description': """what header does SA set to indicate the spam status\nNote that fuglu requires a standard header template configuration for spamstatus and score extraction\nif 'forwardoriginal' is set to 0\neg. start with _YESNO_ or _YESNOCAPS_ and contain score=_SCORE_""",
            },
            
            'spamheader_prepend': {
                'default': 'X-Spam-',
                'description': 'tells fuglu what spamassassin prepends to its headers. Set this according to your spamassassin config especially if you forwardoriginal=0 and strip_oversize=1',
            },
            
            'peruserconfig': {
                'default': 'True',
                'description': 'enable user_prefs in SA. This hands the recipient address over the spamd connection which allows SA to search for configuration overrides',
            },
            
            'lowercase_user': {
                'default': 'True',
                'description': 'lowercase user (envelope rcpt) before passing it to spamd'
            },

            'highspamlevel': {
                'default': '15',
                'description': 'spamscore threshold to mark a message as high spam',
            },

            'highspamaction': {
                'default': 'DEFAULTHIGHSPAMACTION',
                'description': "what should we do with high spam (spam score above highspamlevel)",
            },

            'lowspamaction': {
                'default': 'DEFAULTLOWSPAMACTION',
                'description': "what should we do with low spam (eg. detected as spam, but score not over highspamlevel)",
            },

            'problemaction': {
                'default': 'DEFER',
                'description': "action if there is a problem (DUNNO, DEFER)",
            },

            'rejectmessage': {
                'default': 'message identified as spam',
                'description': "reject message template if running in pre-queue mode",
            },

            'check_sql_blacklist': {
                'default': 'False',
                'description': "consult spamassassins(or any other) sql blacklist for messages that are too big for spam checks\nrequires the sql extension to be enabled",
            },

            'sql_blacklist_dbconnectstring': {
                'default': 'mysql:///localhost/spamassassin',
                'description': "sqlalchemy db connect string",
                'confidential': True,
            },

            'sql_blacklist_sql': {
                'default': """SELECT value FROM userpref WHERE prefid='blacklist_from' AND username in ('$GLOBAL',concat('%',${to_domain}),${to_address})""",
                'description': "SQL query to get the blacklist entries for a suspect\nyou may use template variables: ${from_address} ${from_domain} ${to_address} ${to_domain}",
            },
            'attach_suspect_tags': {
                'default': '',
                'description': "Suspect tags to attach as text part to message for scanning",
            },

        }
        self.logger = self._logger()


    def __str__(self):
        return "SpamAssassin"


    def lint(self):
        allok = self.check_config() and self.lint_ping() and self.lint_spam() and self.lint_blacklist()
        return allok


    def lint_blacklist(self):
        if not self.config.has_option(self.section, 'check_sql_blacklist') or not self.config.getboolean(self.section, 'check_sql_blacklist'):
            return True

        if not SQL_EXTENSION_ENABLED:
            print("SQL Blacklist requested but SQLALCHEMY is not enabled")
            return False

        session = get_session(self.config.get(self.section, 'sql_blacklist_dbconnectstring'))
        suspect = Suspect('dummy@example.com', 'dummy@example.com', '/dev/null')
        conf_sql = self.config.get(self.section, 'sql_blacklist_sql')
        sql, params = self._replace_sql_params(suspect, conf_sql)
        try:
            session.execute(sql, params)
            print("Blacklist SQL Query OK")
            return True
        except Exception as e:
            print(e)
            return False


    def lint_ping(self):
        """ping sa"""
        retries = self.config.getint(self.section, 'retries')
        for i in range(0, retries):
            try:
                self.logger.debug('Contacting spamd (Try %s of %s)' % (i + 1, retries))
                s = self.__init_socket()
                s.sendall(b'PING SPAMC/1.2')
                s.sendall(b"\r\n")
                s.shutdown(socket.SHUT_WR)
                socketfile = s.makefile("rb")
                line = force_uString(socketfile.readline())
                line = line.strip()
                answer = line.split()
                if len(answer) != 3:
                    print("Invalid SPAMD PONG: %s" % line)
                    return False

                if answer[2] != "PONG":
                    print("Invalid SPAMD Pong: %s" % line)
                    return False
                print("Got: %s" % line)
                return True
            except socket.timeout:
                print('SPAMD Socket timed out.')
            except socket.herror as h:
                print('SPAMD Herror encountered : %s' % str(h))
            except socket.gaierror as g:
                print('SPAMD gaierror encountered: %s' % str(g))
            except socket.error as e:
                print('SPAMD socket error: %s' % str(e))

            time.sleep(1)
        return False


    def lint_spam(self):
        spamflag, score, rules = self.safilter_symbols(GTUBE, 'test')
        if 'GTUBE' in rules:
            print("GTUBE Has been detected correctly")
            return True
        else:
            print("SA did not detect GTUBE")
            return False


    def _replace_sql_params(self, suspect, conf_sql):
        """replace template variables in sql with parameters and set sqlalchemy parameters from suspect"""
        values = {}
        values['from_address'] = ':fromaddr'
        values['to_address'] = ':toaddr'
        values['from_domain'] = ':fromdomain'
        values['to_domain'] = ':todomain'

        template = Template(conf_sql)

        sql = template.safe_substitute(values)

        params = {
            'fromaddr': suspect.from_address,
            'toaddr': suspect.to_address,
            'fromdomain': suspect.from_domain,
            'todomain': suspect.to_domain,
        }

        return sql, params


    def check_sql_blacklist(self, suspect, runtimeconfig=None):
        """Check this message against the SQL blacklist. returns highspamaction on hit, DUNNO otherwise"""
        #work in progress
        if not self.config.has_option(self.section, 'check_sql_blacklist') or not self.config.getboolean(self.section, 'check_sql_blacklist'):
            return DUNNO

        if not SQL_EXTENSION_ENABLED:
            self.logger.error('Cannot check sql blacklist, SQLALCHEMY extension is not available')
            return DUNNO

        dbconnectionstring = self.config.get(self.section, 'sql_blacklist_dbconnectstring')
        conf_sql = self.config.get(self.section, 'sql_blacklist_sql')
        try:
            dbsession = get_session(dbconnectionstring)
            sql, params = self._replace_sql_params(suspect, conf_sql)
            resultproxy = dbsession.execute(sql, params)
        except Exception as e:
            self.logger.error('Could not read blacklist from DB connection %s: %s' % (dbconnectionstring, str(e)))
            suspect.debug('Blacklist check failed: %s' % e)
            return DUNNO

        for result in resultproxy:
            dbvalue = result[0]  # this value might have multiple words
            allvalues = dbvalue.split()
            for blvalue in allvalues:
                self.logger.debug(blvalue)
                # build regex
                # translate glob to regexr
                # http://stackoverflow.com/questions/445910/create-regex-from-glob-expression
                regexp = re.escape(blvalue).replace(r'\?', '.').replace(r'\*', '.*?')
                self.logger.debug(regexp)
                pattern = re.compile(regexp)

                if pattern.search(suspect.from_address):
                    self.logger.debug('%s Blacklist match : %s for sa pref %s' % (suspect.id, suspect.from_address, blvalue))
                    confcheck = self.config
                    if runtimeconfig is not None:
                        confcheck = runtimeconfig
                    configaction = string_to_actioncode(confcheck.get(self.section, 'highspamaction'), self.config)
                    suspect.tags['spam']['SpamAssassin'] = True
                    prependheader = self.config.get( 'main', 'prependaddedheaders')
                    suspect.addheader("%sBlacklisted" % prependheader, blvalue)
                    suspect.debug('Sender is Blacklisted: %s' % blvalue)
                    if configaction is None:
                        return DUNNO
                    return configaction

        return DUNNO


    def _problemcode(self):
        retcode = string_to_actioncode(
            self.config.get(self.section, 'problemaction'), self.config)
        if retcode is not None:
            return retcode
        else:
            # in case of invalid problem action
            return DEFER


    def _extract_spamstatus(self, msgrep, spamheadername, suspect):
        """
        extract spamstatus and score from messages returned by spamassassin
        Assumes a default spamheader configuration, eg
        add_header spam Flag _YESNOCAPS_
        or
        add_header all Status _YESNO_, score=_SCORE_ required=_REQD_ tests=_TESTS_ autolearn=_AUTOLEARN_ version=_VERSION_

        :param msgrep: email.message.Message object built from the returned source
        :param spamheadername: name of the header containing the status information
        :return: tuple isspam,spamscore . isspam is a boolean, spamscore a float or None if the spamscore can't be extracted
        """
        isspam = False
        spamheader = msgrep[spamheadername]

        spamscore = None
        if spamheader is None:
            self.logger.warning('%s Did not find Header %s in returned message from SA' % (suspect.id, spamheadername))
        else:
            if re.match(r"""^YES""", spamheader.strip(), re.IGNORECASE) is not None:
                isspam = True

            patt = re.compile('Score=([\-\d.]{1,10})', re.IGNORECASE)
            m = patt.search(spamheader)

            if m is not None:
                spamscore = float(m.group(1))
                self.logger.debug('%s Spamscore: %s' % (suspect.id, spamscore))
                suspect.debug('Spamscore: %s' % spamscore)
            else:
                self.logger.warning('%s Could not extract spam score from header: %s' % (suspect.id, spamheader))
                suspect.debug( 'Could not read spam score from header %s' % spamheader)
            return isspam, spamscore, spamheader
        return isspam, spamscore, spamheader
    
    
    def _get_content(self, suspect):
        maxsize = self.config.getint(self.section, 'maxsize')
        
        if self.config.getboolean(self.section, 'scanoriginal'):
            content = suspect.get_original_source()
        else:
            content = suspect.get_source()

        # keep copy of original content before stripping
        content_orig = content
        
        stripped = False
        if suspect.size > maxsize:
            stripped = True
            # send maxsize-1 to be consistent with previous implementation
            content = suspect.source_stripped_attachments(content=content, maxsize=maxsize - 1, with_mime_headers=True)
            suspect.set_tag('SAPlugin.stripped', True)
            suspect.write_sa_temp_header('X-Fuglu-OrigSize', str(len(content_orig)))
            self.logger.info('%s stripped attachments, body size reduced from %s to %s bytes' % (
            suspect.id, len(content_orig), len(content)))
        # stick to bytes
        content = force_bString(content)
    
        # write fugluid
        suspect.write_sa_temp_header('X-Fuglu-Suspect', str(suspect.id))
    
        # prepend temporary headers set by other plugins
        tempheaders = suspect.get_sa_temp_headers()
        if tempheaders != b'':
            content = tempheaders + content
    
        # add incoming port information
        try:
            portheader = b'X-Fuglu-Incomingport: %i\r\n' % int(suspect.get_tag('incomingport', 0))
            content = portheader + content
        except (TypeError, ValueError) as e:
            self.logger.error('%s could not add incomingport header: %s' % (suspect.id, str(e)))
    
        # add envelope sender information
        msgrep = suspect.get_message_rep()
        if not 'Return-Path' in msgrep.keys():
            from_address = suspect.from_address or '<>'  # bounce address should be <>
            content = force_bString('Return-Path: %s' % from_address + '\r\n') + content
            self.logger.info(f'{suspect.id} Set temp Return-Path header as {from_address}')
        else:
            self.logger.debug(f'{suspect.id} Return-Path already set as {msgrep["Return-Path"]}')

        extralines = self._text_from_tags(suspect=suspect)
        if extralines:
            msgrep = email.message_from_bytes(content, _class=PatchedMessage)
            if msgrep.is_multipart():
                msgrep.attach(MIMEText("\n".join(extralines)))
                content = msgrep.as_bytes()
            else:
                content += b"\r\n" + b"\r\n".join(force_bString(extralines))

        return content, content_orig, stripped

    @staticmethod
    def _getlist_space_comma_separated(inputstring):
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

    def _text_from_tags(self, suspect):
        """Collect lines to append from given tags"""
        lines = []
        appendtags = self.config.get(self.section, 'attach_suspect_tags')
        try:
            tags = Suspect.getlist_space_comma_separated(appendtags)
        except Exception:
            tags = []

        for tag in tags:
            tag = force_uString(suspect.get_tag(tag, []))
            if not isinstance(tag, list):
                tag = [tag]
            lines.extend(tag)
            self.logger.debug(f"{suspect.id} Got {len(tag)} additional lines from suspect tag {tag}")
        return lines

    def examine(self, suspect):
        # check if someone wants to skip sa checks
        if suspect.get_tag('SAPlugin.skip') is True:
            self.logger.debug('%s Skipping SA Plugin (requested by previous plugin)' % suspect.id)
            suspect.set_tag('SAPlugin.skipreason', 'requested by previous plugin')
            return DUNNO
        
        runtimeconfig = DBConfig(self.config, suspect)
        
        maxsize = self.config.getint(self.section, 'maxsize')
        strip_oversize = self.config.getboolean(self.section, 'strip_oversize')
        
        if suspect.size > maxsize and not strip_oversize:
            self.logger.info('%s Size Skip, %s > %s' % (suspect.id, suspect.size, maxsize))
            suspect.debug('Too big for spamchecks. %s > %s' % (suspect.size, maxsize))
            prependheader = self.config.get('main', 'prependaddedheaders')
            suspect.addheader("%sSA-SKIP" % prependheader, 'Too big for spamchecks. %s > %s' % (suspect.size, maxsize))
            suspect.set_tag('SAPlugin.skipreason', 'size skip')
            return self.check_sql_blacklist(suspect)
        
        content, content_orig, stripped = self._get_content(suspect)
        
        forwardoriginal = self.config.getboolean(self.section, 'forwardoriginal')
        if forwardoriginal:
            ret = self.safilter_report(content, suspect.to_address)
            if ret is None:
                suspect.debug('SA report Scan failed - please check error log')
                self.logger.error('%s SA report scan FAILED' % suspect.id)
                suspect.addheader('%sSA-SKIP' % self.config.get('main', 'prependaddedheaders'), 'SA scan failed')
                suspect.set_tag('SAPlugin.skipreason', 'scan failed')
                return self._problemcode()
            isspam, spamscore, report = ret
            suspect.tags['SAPlugin.report'] = report
        
        else:
            filtered = self.safilter(content, suspect.to_address)
            if filtered is None:
                suspect.debug('SA Scan failed - please check error log')
                self.logger.error('%s SA scan FAILED' % suspect.id)
                suspect.addheader('%sSA-SKIP' % self.config.get('main', 'prependaddedheaders'), 'SA scan failed')
                suspect.set_tag('SAPlugin.skipreason', 'scan failed')
                return self._problemcode()
            else:
                if stripped:
                    # create msgrep of filtered msg
                    if isinstance(content,str):
                        msgrep_filtered = email.message_from_string(filtered, _class=PatchedMessage)
                    else:
                        msgrep_filtered = email.message_from_bytes(filtered, _class=PatchedMessage)
                    header_new = []
                    for h,v in msgrep_filtered.items():
                        header_new.append(force_uString(h).strip() + ': ' + force_uString(v).strip())
                    # add headers to msg
                    sa_prepend = self.config.get(self.section, 'spamheader_prepend')
                    for i in header_new:
                        if sa_prepend == '' or sa_prepend is None:
                            break
                        if re.match('^' + sa_prepend + '[^:]+: ', i, re.I):
                            # in case of stripped msg add header to original content
                            content_orig = force_bString(i) + b'\r\n' + force_bString(content_orig)
                        else:
                            continue
                    content = content_orig
                else:
                    content = filtered
                    
            if isinstance(content,str):
                newmsgrep = email.message_from_string(content, _class=PatchedMessage)
            else:
                newmsgrep = email.message_from_bytes(content, _class=PatchedMessage)
            
            # if original content is forwarded there's no need to reset the attachmant
            # manager. Only header have been changed.
            suspect.set_source(content,att_mgr_reset=(not forwardoriginal))
            spamheadername = self.config.get(self.section, 'spamheader')
            isspam, spamscore, report = self._extract_spamstatus(newmsgrep, spamheadername, suspect)
            suspect.tags['SAPlugin.report'] = report
            self.logger.debug('suspect %s %s %s %s' % (suspect.id, isspam, spamscore, suspect.get_tag('SAPlugin.report')))
        
        action = DUNNO
        message = None
        
        if isspam:
            self.logger.debug('%s Message is spam' % suspect.id)
            suspect.debug('Message is spam')
            
            configaction = string_to_actioncode(
                runtimeconfig.get(self.section, 'lowspamaction'), self.config)
            if configaction is not None:
                action = configaction
            values = dict(spamscore=spamscore)
            message = apply_template(
                self.config.get(self.section, 'rejectmessage'), suspect, values)
        else:
            self.logger.debug('%s Message is not spam' % suspect.id)
            suspect.debug('Message is not spam')
        
        suspect.tags['spam']['SpamAssassin'] = isspam
        suspect.tags['highspam']['SpamAssassin'] = False
        if spamscore is not None:
            suspect.tags['SAPlugin.spamscore'] = spamscore
            highspamlevel = runtimeconfig.getfloat(self.section, 'highspamlevel')
            if spamscore >= highspamlevel:
                suspect.tags['highspam']['SpamAssassin'] = True
                configaction = string_to_actioncode(runtimeconfig.get(self.section, 'highspamaction'), self.config)
                if configaction is not None:
                    action = configaction
        return action, message


    def __init_socket(self):
        unixsocket = False

        try:
            self.config.getint(self.section, 'port')
        except ValueError:
            unixsocket = True

        if unixsocket:
            sock = self.config.get(self.section, 'port')
            if not os.path.exists(sock):
                raise Exception("unix socket %s not found" % sock)
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.settimeout(self.config.getint(self.section, 'timeout'))
            try:
                s.connect(sock)
            except socket.error:
                raise Exception('Could not reach spamd using unix socket %s' % sock)
        else:
            host = self.config.get(self.section, 'host')
            port = self.config.getint(self.section, 'port')
            timeout = self.config.getfloat(self.section, 'timeout')
            try:
                s = socket.create_connection((host, port), timeout)
            except socket.error:
                raise Exception('Could not reach spamd using network (%s, %s)' % (host, port))

        return s


    def safilter(self, messagecontent, user):
        """pass content to sa, return sa-processed mail"""
        retries = self.config.getint(self.section, 'retries')
        peruserconfig = self.config.getboolean(self.section, 'peruserconfig')
        if self.config.getboolean(self.section, 'lowercase_user'):
            user = user.lower()
        spamsize = len(messagecontent)
        for i in range(0, retries):
            try:
                self.logger.debug('Contacting spamd (Try %s of %s)' % (i + 1, retries))
                s = self.__init_socket()
                s.sendall(force_bString('PROCESS SPAMC/1.2'))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("Content-length: %s" % spamsize))
                s.sendall(force_bString("\r\n"))
                if peruserconfig:
                    s.sendall(force_bString("User: %s" % user))
                    s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString(messagecontent))
                self.logger.debug('Sent %s bytes to spamd' % spamsize)
                s.shutdown(socket.SHUT_WR)
                socketfile = s.makefile("rb")
                line1_info = socketfile.readline()
                line1_info = force_uString(line1_info)  # convert to unicode string
                self.logger.debug(line1_info)
                line2_contentlength = socketfile.readline()
                line3_empty = socketfile.readline()
                content = socketfile.read()
                self.logger.debug('Got %s message bytes from back from spamd' % len(content))
                answer = line1_info.strip().split()
                if len(answer) != 3:
                    self.logger.error("Got invalid status line from spamd: %s" % line1_info)
                    continue

                version, number, status = answer
                if status != 'EX_OK':
                    self.logger.error("Got bad status from spamd: %s" % status)
                    continue

                return content
            except socket.timeout:
                self.logger.error('SPAMD Socket timed out.')
            except socket.herror as h:
                self.logger.error('SPAMD Herror encountered : %s' % str(h))
            except socket.gaierror as g:
                self.logger.error('SPAMD gaierror encountered: %s' % str(g))
            except socket.error as e:
                self.logger.error('SPAMD socket error: %s' % str(e))
            except Exception as e:
                self.logger.error('SPAMD communication error: %s' % str(e))

            time.sleep(1)
        return None


    def safilter_symbols(self, messagecontent, user):
        """Pass content to sa, return spamflag, score, rules"""
        ret = self._safilter_content(messagecontent, user, 'SYMBOLS')
        if ret is None:
            return None

        status, score, content = ret

        content = force_uString(content)
        rules = content.split(',')
        return status, score, rules


    def safilter_report(self, messagecontent, user):
        return self._safilter_content(messagecontent, user, 'REPORT')


    def _safilter_content(self, messagecontent, user, command):
        """pass content to sa, return body"""
        assert command in ['SYMBOLS', 'REPORT', ]
        retries = self.config.getint(self.section, 'retries')
        peruserconfig = self.config.getboolean(self.section, 'peruserconfig')
        if self.config.getboolean(self.section, 'lowercase_user'):
            user = user.lower()
        spamsize = len(messagecontent)
        for i in range(0, retries):
            try:
                self.logger.debug('Contacting spamd  (Try %s of %s)' % (i + 1, retries))
                s = self.__init_socket()
                s.sendall(force_bString('%s SPAMC/1.2' % command))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("Content-length: %s" % spamsize))
                s.sendall(force_bString("\r\n"))
                if peruserconfig:
                    s.sendall(force_bString("User: %s" % user))
                    s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString(messagecontent))
                self.logger.debug('Sent %s bytes to spamd' % spamsize)
                s.shutdown(socket.SHUT_WR)
                socketfile = s.makefile("rb")
                line1_info = force_uString(socketfile.readline())
                self.logger.debug(line1_info)
                line2_spaminfo = force_uString(socketfile.readline())

                line3 = force_uString(socketfile.readline())
                content = socketfile.read()
                content = content.strip()

                self.logger.debug('Got %s message bytes from back from spamd' % len(content))
                answer = line1_info.strip().split()
                if len(answer) != 3:
                    self.logger.error("Got invalid status line from spamd: %s" % line1_info)
                    continue

                version, number, status = answer
                if status != 'EX_OK':
                    self.logger.error("Got bad status from spamd: %s" % status)
                    continue

                self.logger.debug('Spamd said: %s' % line2_spaminfo)
                spamword, spamstatusword, colon, score, slash, required = line2_spaminfo.split()
                spstatus = False
                if spamstatusword == 'True':
                    spstatus = True

                return spstatus, float(score), content
            except socket.timeout:
                self.logger.error('SPAMD Socket timed out.')
            except socket.herror as h:
                self.logger.error('SPAMD Herror encountered : %s' % str(h))
            except socket.gaierror as g:
                self.logger.error('SPAMD gaierror encountered: %s' % str(g))
            except socket.error as e:
                self.logger.error('SPAMD socket error: %s' % str(e))
            except Exception as e:
                self.logger.error('SPAMD communication error: %s' % str(e))

            time.sleep(1)
        return None


    def debug_proto(self, messagecontent, command='SYMBOLS'):
        """proto debug.. only used for development"""
        command = command.upper()
        assert command in ['CHECK', 'SYMBOLS', 'REPORT',
                           'REPORT_IFSPAM', 'SKIP', 'PING', 'PROCESS', 'TELL']

        host = "127.0.0.1"
        port = 783
        timeout = 20

        spamsize = len(messagecontent)

        s = socket.create_connection((host, port), timeout)
        s.sendall(command.encode() + b' SPAMC/1.2')
        s.sendall(b"\r\n")
        s.sendall(b"Content-length: " + str(spamsize).encode())
        s.sendall(b"\r\n")
        s.sendall(b"\r\n")
        s.sendall(messagecontent)
        s.shutdown(socket.SHUT_WR)
        socketfile = s.makefile("rb")
        gotback = socketfile.read()
        print(gotback)



SALEARN_LOCAL = 'local'
SALEARN_REMOTE = 'remote'
SALEARN_HAM = 'ham'
SALEARN_SPAM = 'spam'
SALEARN_SET = 'Set'
SALEARN_REMOVE = 'Remove'


class SALearn(SAPlugin):
    """This plugin passes suspects to spamassassin daemon (bayes learning/unlearning only).

Prerequisites: SPAMD must be installed and running (not necessarily on the same box as fuglu)

Tags:

 * reads ``salearn.class``, (text or None) set to 'ham' or 'spam' for learning, any other value will disable learning
 * reads ``SAPlugin.action``, (text) set to 'Set' or 'Remove' for respective action. If unset, defaults to 'Set'.
"""
    
    
    def __init__(self, config, section):
        SAPlugin.__init__(self, config, section)
        self.requiredvars = {
            'host': {
                'default': 'localhost',
                'description': 'hostname where spamd runs',
            },

            'port': {
                'default': '783',
                'description': "tcp port number or path to spamd unix socket",
            },

            'timeout': {
                'default': '30',
                'description': 'how long should we wait for an answer from sa',
            },

            'maxsize': {
                'default': '256000',
                'description': "maximum size in bytes. larger messages will be skipped",
            },

            'retries': {
                'default': '3',
                'description': 'how often should fuglu retry the connection before giving up',
            },
            
            'peruserconfig': {
                'default': 'True',
                'description': 'enable user_prefs in SA. This hands the recipient address over the spamd connection which allows SA to search for configuration overrides',
            },

            'problemaction': {
                'default': 'DUNNO',
                'description': "action if there is a problem (DUNNO, DEFER)",
            },
            
            'learn_local': {
                'default': 'True',
                'description': 'learn to local database',
            },
            
            'learn_remote': {
                'default': 'True',
                'description': 'learn to remote database',
            },
            
            'learn_default': {
                'default': SALEARN_SPAM,
                'description': 'default learn action (ham, spam or leave empty)'
            }
        
        }
        
    
    def _get_databases(self):
        databases = []
        if self.config.getboolean(self.section, 'learn_local'):
            databases.append(SALEARN_LOCAL)
        if self.config.getboolean(self.section, 'learn_remote'):
            databases.append(SALEARN_REMOTE)
        return databases
        
    
    def examine(self, suspect):
        spamsize = suspect.size
        maxsize = self.config.getint(self.section, 'maxsize')

        if spamsize > maxsize:
            self.logger.info('%s Size Skip, %s > %s' % (suspect.id, spamsize, maxsize))
            suspect.debug('Too big for spamchecks. %s > %s' % (spamsize, maxsize))
            return DUNNO
        
        messageclass = suspect.get_tag('salearn.class', self.config.get(self.section, 'learn_default'))
        learnaction = suspect.get_tag('salearn.action', SALEARN_SET)
        
        if messageclass not in [SALEARN_SPAM, SALEARN_HAM]:
            self.logger.debug('%s not learning message, message class tag value=%s' % (suspect.id, messageclass))
        else:
            databases = self._get_databases()
            ret = self._salearn_content(suspect.get_original_source(), suspect.to_address, messageclass, learnaction, databases)
            if not ret:
                return self._problemcode()
        return DUNNO
    
    
    def _salearn_content(self, messagecontent, user, messageclass=SALEARN_SPAM, learnaction=SALEARN_SET, databases=(SALEARN_LOCAL, SALEARN_REMOTE)):
        """pass content to sa, return body"""
        assert messageclass in [SALEARN_HAM, SALEARN_SPAM]
        assert learnaction in [SALEARN_SET, SALEARN_REMOVE]
        assert 1<=len(databases)<=2
        for db in databases:
            assert db in [SALEARN_LOCAL, SALEARN_REMOTE]
            
        retries = self.config.getint(self.section, 'retries')
        peruserconfig = self.config.getboolean(self.section, 'peruserconfig')
        if self.config.getboolean(self.section, 'lowercase_user') and user:
            user = user.lower()
        spamsize = len(messagecontent)
        for i in range(0, retries):
            try:
                self.logger.debug('Contacting spamd  (Try %s of %s)' % (i + 1, retries))
                s = self.__init_socket()
                s.sendall(force_bString('TELL SPAMC/1.2'))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("Content-length: %s" % spamsize))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("Message-class: %s" % messageclass))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("%s: %s" % (learnaction, ', '.join(databases))))
                s.sendall(force_bString("\r\n"))
                if peruserconfig:
                    s.sendall(force_bString("User: %s" % user))
                    s.sendall(force_bString("\r\n"))
                s.sendall(force_bString("\r\n"))
                s.sendall(force_bString(messagecontent))
                self.logger.debug('Sent %s bytes to spamd' % spamsize)
                s.shutdown(socket.SHUT_WR)
                socketfile = s.makefile("rb")
                line1_info = force_uString(socketfile.readline())
                self.logger.debug(line1_info)
                line2_spaminfo = force_uString(socketfile.readline())
                
                answer = line1_info.strip().split()
                if len(answer) != 3:
                    self.logger.error("Got invalid status line from spamd: %s" % line1_info)
                    continue
                
                version, number, status = answer
                if status != 'EX_OK':
                    self.logger.error("Got bad status from spamd: %s" % status)
                    continue
                
                self.logger.debug('Spamd said: %s' % line2_spaminfo)
                hdr, status = line2_spaminfo.split(':')
                if (learnaction==SALEARN_SET and hdr=='DidSet') \
                    or (learnaction==SALEARN_REMOVE and hdr=='DidRemove'):
                    success = True
                else:
                    success = False
                
                return success
            except socket.timeout:
                self.logger.error('SPAMD Socket timed out.')
            except socket.herror as h:
                self.logger.error('SPAMD Herror encountered : %s' % str(h))
            except socket.gaierror as g:
                self.logger.error('SPAMD gaierror encountered: %s' % str(g))
            except socket.error as e:
                self.logger.error('SPAMD socket error: %s' % str(e))
            except Exception as e:
                self.logger.error('SPAMD communication error: %s' % str(e))
            
            time.sleep(1)
        return None
    
    
    def lint(self):
        allok = self.check_config() and self.lint_ping()
        if allok:
            databases = self._get_databases()
            allok = 1<=len(databases)<=2
            if not allok:
                print('ERROR: Enable at least one of learn_local, learn_remote')
        return allok



if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        print('need command argument')
        sys.exit(1)
    plugin = SAPlugin(None)
    print("sending...")
    print("--------------")
    plugin.debug_proto(GTUBE, sys.argv[1])
    print("--------------")


