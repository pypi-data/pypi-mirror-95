# -*- coding: UTF-8 -*-
#   Copyright 2009-2021 Fumail Project
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
from fuglu.stringencode import force_uString
from fuglu.extensions.sql import DBConfig
import json
import tempfile
import os
from http.client import HTTPConnection
from fuglu.stringencode import force_bString



GTUBE = """Date: Mon, 08 Sep 2008 17:33:54 +0200
To: oli@unittests.fuglu.org
From: oli@unittests.fuglu.org
Subject: test scanner

  XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X
"""



class RSpamdPlugin(ScannerPlugin):
    """
    Scan messages with rspamd through rspamd's RESTful interface.
    
    This plugin aims to mimick the behaviour of the fuglu stock SA plugin as closely as possible.
    """
    
    
    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
        self.requiredvars = {
            'host': {
                'default': '127.0.0.1',
                'description': 'hostname where rspamd runs',
            },

            'port': {
                'default': '11333',
                'description': 'port number of rspamd TCP socket ("normal" worker)',
            },

            'timeout': {
                'default': '30',
                'description': 'how long should we wait for an answer from rspamd',
            },

            'maxsize': {
                'default': '256000',
                'description': "maximum size in bytes. larger messages will be skipped",
            },

            'scanoriginal': {
                'default': 'True',
                'description': "should we scan the original message as retreived from postfix or scan the current state \nin fuglu (which might have been altered by previous plugins)\nonly set this to disabled if you have a custom plugin that adds special headers to the message that will be \nused in rspamd rules",
            },

            'forwardoriginal': {
                'default': 'False',
                'description': """forward the original message or add spam report\nif this is enabled, no rspamd spam report headers will be visible in the final message.\n"original" in this case means "as passed to rspamd", eg. if 'scanoriginal' above is disabled this will forward the\nmessage as retreived from previous plugins """,
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
        
        }
    
    
    
    def __str__(self):
        return "RSpamd"
    
    
    
    def lint(self):
        allok = self.check_config()
        # further checks are not easy to implement:
        # - rspamd does not support gtube
        # - no lint function implemented in workers
        # - may only check tcp connection...
        allok = allok and self._lint_gtube()
        return allok
    
    
    
    def _lint_gtube(self):
        tmpfile = tempfile.mkstemp()[1]
        with open(tmpfile, 'w') as fh:
            fh.write(GTUBE)
        
        suspect = Suspect('oli@unittests.fuglu.org', 'oli@unittests.fuglu.org', tmpfile)
        data = self.rspamd_json(suspect)
        
        os.remove(tmpfile)
        print(data)
        return (None not in data)    
    
    
    def rspamd_json(self, suspect):
        # https://rspamd.com/doc/architecture/protocol.html
        
        host = self.config.get(self.section, 'host')
        port = self.config.getint(self.section, 'port')
        timeout = self.config.getint(self.section, 'timeout')

        if self.config.getboolean(self.section, 'scanoriginal'):
            content = suspect.get_original_source()
        else:
            content = suspect.get_source()
        
        content = force_bString(content)
        # prepend temporary headers set by other plugins
        tempheaders = suspect.get_sa_temp_headers()
        if tempheaders != b'':
            content = tempheaders + content
        
        clientinfo = suspect.get_client_info(self.config)
        if clientinfo is not None:
            helo, clienthostname, clientip = clientinfo
            clientinfoheaders = {
                "IP": clientip,
                "Helo": helo,
                "Hostname": clienthostname,
            }
        else:
            clientinfoheaders = {}
            
        msgrep = suspect.get_message_rep()
        subj=msgrep['X-Spam-Prev-Subject']
        if subj is None:
            subj=msgrep['Subject']
        if subj is None:
            subj=''
        
        headers = {
            #"Deliver-To": suspect.to_address,
            "From": suspect.from_address,
            "Queue-Id": suspect.id,
            "Rcpt": suspect.to_address,
            "Subject": subj,
            #"User": '', # n/a
            "Message-Length": suspect.size,
            "Json": "yes", # enforce json reply even if not set in rspamd config
        }
        headers.update(clientinfoheaders)
        
        try:
            conn = HTTPConnection(host, port, timeout=timeout)
            conn.request("POST", "/symbols", content, {})
            response = conn.getresponse()
            #response.status, response.reason
            jsondata = force_uString(response.read())
            reply = json.loads(jsondata)
        except Exception as e:
            reply = None
            self.logger.error('Failed to get rspamd response for %s: %s' % (suspect.id, str(e)))
        
        if reply and 'default' in reply: # rspamd 1.6
            replydata = reply['default']
        elif reply and len(reply) == 1: #rspamd 0.6
            replydata = reply[0]
        else:
            replydata = None
        
        if replydata:
            isspam = 'is_spam' in replydata and replydata['is_spam'] == True
            if not isspam and 'action' in replydata:
                self.logger.debug('%s rspamd action is: %s' % (suspect.id, replydata['action']))
                if replydata['action'] not in ['no_action', 'no action']:
                    isspam = True
            # action is defined in metrics.conf, defaults are: reject = 15, add_header = 6, greylist = 4
            # we treat every action other than "no_action" as "rspamd detected spam"
            
            spamscore = None
            if 'score' in replydata:
                spamscore = replydata['score']
                
            report, symbols = self._gen_report(replydata)
            return isspam, spamscore, report, symbols
        
        else:
            if reply is not None:
                self.logger.error('rspamd reply of wrong length %s for %s' % (len(reply), suspect.id))
            return None, None, None, None
    
    
    
    def _gen_report(self, reply):
        report = []
        symbols = []
        if 'symbols' in reply: # rspamd 0.6
            weight = 0
            name = 'UNKNOWN'
            desc = ''
            options = ''
            for symbol in reply['symbols']:
                if 'weight' in symbol:
                    weight = symbol['weight']
                if 'name' in symbol:
                    name = symbol['name']
                if 'description' in symbol:
                    desc = symbol['description']
                if 'optios' in symbol:
                    options = ' '.join(symbol['options'])
                line = '%s %s %s %s' % (weight, name, desc, options)
                report.append(line)
                symbols.append(name)
        else: # rspamd 1.6
            keys = reply.keys()
            for key in keys:
                score = 0
                name = 'UNKNOWN'
                desc = ''
                if key.isupper():
                    symbol = reply[key]
                    if 'score' in symbol:
                        score = symbol['score']
                    if 'name' in symbol:
                        name = symbol['name']
                    if 'description' in symbol:
                        desc = symbol['description']
                    elif 'options' in symbol:
                        desc = ' / '.join(symbol['options'])
                    line = '%s %s %s' % (score, name, desc)
                    report.append(line)
                    symbols.append(name)
                    
        return report, symbols
    
    
    
    def examine(self, suspect):
        if suspect.get_tag('RSpamd.skip') is True:
            self.logger.debug('%s Skipping RSpamd Plugin (requested by previous plugin)' % suspect.id)
            suspect.set_tag('RSpamd.skipreason', 'requested by previous plugin')
            return DUNNO
        
        maxsize = self.config.getint(self.section, 'maxsize')
        if suspect.size > maxsize:
            self.logger.info('%s Size Skip, %s > %s' %
                             (suspect.id, suspect.size, maxsize))
            suspect.debug('Too big for spamchecks. %s > %s' %
                          (suspect.size, maxsize))
            prependheader = self.config.get('main', 'prependaddedheaders')
            suspect.addheader(
                "%sRSPAMD-SKIP" % prependheader, 'Too big for spamchecks. %s > %s' % (suspect.size, maxsize))
            suspect.set_tag('RSpamd.skipreason', 'size skip')
            return DUNNO
        
        runtimeconfig = DBConfig(self.config, suspect)
        
        isspam, spamscore, report, symbols = self.rspamd_json(suspect)
        
        action = DUNNO
        message = None
        
        if isspam is None:
            return self._problemcode()
        
        elif isspam:
            self.logger.debug('%s Message is spam' % suspect.id)
            suspect.debug('Message is spam')
            
            configaction = string_to_actioncode(runtimeconfig.get(self.section, 'lowspamaction'), self.config)
            if configaction is not None:
                action = configaction
            values = dict(spamscore=spamscore)
            message = apply_template(self.config.get(self.section, 'rejectmessage'), suspect, values)
        else:
            self.logger.debug('%s Message is not spam' % suspect.id)
            suspect.debug('Message is not spam')
        
        suspect.tags['RSpamd.report'] = '\n'.join(report)
        suspect.tags['spam']['RSpamd'] = isspam
        suspect.tags['highspam']['RSpamd'] = False
        if spamscore is not None:
            suspect.tags['RSpamd.spamscore'] = spamscore
            highspamlevel = runtimeconfig.getfloat(
                self.section, 'highspamlevel')
            if spamscore >= highspamlevel:
                suspect.tags['highspam']['RSpamd'] = True
                configaction = string_to_actioncode(
                    runtimeconfig.get(self.section, 'highspamaction'), self.config)
                if configaction is not None:
                    action = configaction
        
        forwardoriginal = self.config.getboolean(self.section, 'forwardoriginal')
        if not forwardoriginal:
            # rspamd sample headers: https://github.com/vstakhov/rspamd/issues/799
            suspect.addheader('%sRSPAMD-Spam' % self.config.get('main', 'prependaddedheaders'),
                              'yes' if isspam else 'no')
            suspect.addheader('%sRSPAMD-Spam-Symbols' % self.config.get('main', 'prependaddedheaders'),
                              ','.join(symbols))
        
        return action, message
    
    
    
    def _problemcode(self):
        retcode = string_to_actioncode(self.config.get(self.section, 'problemaction'), self.config)
        if retcode is not None:
            return retcode
        else:
            # in case of invalid problem action
            return DEFER
        
        
    

    
    
