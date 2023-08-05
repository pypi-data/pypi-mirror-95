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
from fuglu.shared import AVScannerPlugin, DUNNO, Suspect
from fuglu.stringencode import force_bString, force_uString
import socket
import re
import os


class FprotPlugin(AVScannerPlugin):

    """ This plugin passes suspects to a f-prot scan daemon

Prerequisites: f-protd must be installed and running, not necessarily on the same box as fuglu though.

Notes for developers:


Tags:

 * sets ``virus['F-Prot']`` (boolean)
 * sets ``FprotPlugin.virus`` (list of strings) - virus names found in message
"""

    def __init__(self, config, section=None):
        AVScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()

        self.requiredvars = {
            'host': {
                'default': 'localhost',
                'description': 'hostname where fpscand runs',
            },
            'port': {
                'default': '10200',
                'description': "fpscand port",
            },
            'timeout': {
                'default': '30',
                'description': "network timeout",
            },
            'networkmode': {
                'default': 'False',
                'description': "Always send data over network instead of just passing the file name when possible. If fpscand runs on a different host than fuglu, you must enable this.",
            },
            'scanoptions': {
                'default': '',
                'description': 'additional scan options  (see `man fpscand` -> SCANNING OPTIONS for possible values)',
            },
            'maxsize': {
                'default': '10485000',
                'description': "maximum message size to scan",
            },
            'retries': {
                'default': '3',
                'description': "maximum retries on failed connections",
            },
            'virusaction': {
                'default': 'DEFAULTVIRUSACTION',
                'description': "plugin action if threat is detected",
            },
            'problemaction': {
                'default': 'DEFER',
                'description': "plugin action if scan fails",
            },
            'rejectmessage': {
                'default': 'threat detected: ${virusname}',
                'description': "reject message template if running in pre-queue mode and virusaction=REJECT",
            },
        }

        self.pattern = re.compile(b'^(\d)+ <(.+)> (.+)$')
        self.enginename = 'F-Prot'
    
    
    def examine(self, suspect):
        if self._check_too_big(suspect):
            return DUNNO

        # use msgrep only to check for Content-Type header
        # use source directly for Fprot to prevent exceptions converting the email-object to bytes
        msgrep = suspect.get_message_rep()
        content = suspect.get_original_source()

        networkmode = self.config.getboolean(self.section, 'networkmode')

        # this seems to be a bug in f-prot.
        # If no Content-Type header is set, then no scan is performed.
        # However, content of the header does not seem to matter.
        # Therefore we set a temporary dummy Content-Type header.
        if not 'Content-Type'.lower() in [k.lower() for k in msgrep.keys()]:
            content = Suspect.prepend_header_to_source('Content-Type', 'dummy', content)
            networkmode = True
            self.logger.debug('%s missing Content-Type header... falling back to network mode' % suspect.id)

        for i in range(0, self.config.getint(self.section, 'retries')):
            try:
                if networkmode:
                    viruses = self.scan_stream(content, suspect.id)
                else:
                    viruses = self.scan_file(suspect.tempfile)
                actioncode, message = self._virusreport(suspect, viruses)
                return actioncode, message
            except Exception as e:
                self.logger.warning("%s Error encountered while contacting fpscand (try %s of %s): %s" %
                                       (suspect.id, i + 1, self.config.getint(self.section, 'retries'), str(e)))
        self.logger.error("fpscand failed after %s retries" % self.config.getint(self.section, 'retries'))
        
        return self._problemcode()
    
    
    def _parse_result(self, result):
        dr = {}
        result = force_uString(result)
        for line in result.strip().split('\n'):
            m = self.pattern.match(force_bString(line))
            if m is None:
                self.logger.error('Could not parse line from f-prot: %s' % line)
                raise Exception('f-prot: Unparseable answer: %s' % result)
            status = force_uString(m.group(1))
            text = force_uString(m.group(2))
            details = force_uString(m.group(3))

            status = int(status)
            self.logger.debug("f-prot scan status: %s" % status)
            self.logger.debug("f-prot scan text: %s" % text)
            if status == 0:
                continue

            if status > 3:
                self.logger.warning("f-prot: got unusual status %s (result: %s)" % (status, result))

            # http://www.f-prot.com/support/helpfiles/unix/appendix_c.html
            if status & 1 == 1 or status & 2 == 2:
                # we have a infection
                if text[0:10] == "infected: ":
                    text = text[10:]
                elif text[0:27] == "contains infected objects: ":
                    text = text[27:]
                else:
                    self.logger.warn("Unexpected reply from f-prot: %s" % text)
                    continue
                dr[details] = text

        if len(dr) == 0:
            return None
        else:
            return dr
    
    
    def scan_file(self, filename):
        filename = os.path.abspath(filename)
        s = self.__init_socket__()
        s.sendall(force_bString('SCAN %s FILE %s' % (self.config.get(self.section, 'scanoptions'), filename)))
        s.sendall(b'\n')

        result = s.recv(20000)
        if len(result) < 1:
            self.logger.error('Got no reply from fpscand')
        s.close()

        return self._parse_result(result)
    
    
    def scan_stream(self, content, suspectid='(NA)'):
        """
        Scan a buffer

        content (string) : buffer to scan

        return either :
          - (dict) : {filename1: "virusname"}
          - None if no virus found
        """

        s = self.__init_socket__()
        content = force_bString(content)
        buflen = len(content)
        s.sendall(force_bString('SCAN %s STREAM fu_stream SIZE %s' % (self.config.get(self.section, 'scanoptions'), buflen)))
        s.sendall(b'\n')
        self.logger.debug('%s Sending buffer (length=%s) to fpscand...' % (suspectid, buflen))
        s.sendall(content)
        self.logger.debug('%s Sent %s bytes to fpscand, waiting for scan result' % (suspectid, buflen))

        result = force_uString(s.recv(20000))
        if len(result) < 1:
            self.logger.error('Got no reply from fpscand')
        s.close()

        return self._parse_result(result)
    
    
    def __init_socket__(self):
        host = self.config.get(self.section, 'host')
        port = self.config.getint(self.section, 'port')
        socktimeout = self.config.getint(self.section, 'timeout')
        try:
            s = socket.create_connection((host, port), socktimeout)
        except socket.error:
            raise Exception('Could not reach fpscand using network (%s, %s)' % (host, port))
        return s
    
    
    def __str__(self):
        return 'F-Prot AV'
    
    
    def lint(self):
        allok = self.check_config() and self.lint_eicar()
        networkmode = self.config.getboolean(self.section, 'networkmode')
        if not networkmode:
            allok = allok and self.lint_file()
        return allok

    def lint_file(self):
        import tempfile
        (handle, tempfilename) = tempfile.mkstemp(prefix='fuglu', dir=self.config.get('main', 'tempdir'))
        tempfilename = tempfilename

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
        with os.fdopen(handle, 'w+b') as fd:
            fd.write(force_bString(stream))

        try:
            viruses = self.scan_file(tempfilename)
        except Exception as e:
            print(e)
            return False

        try:
            os.remove(tempfilename)
        except Exception:
            pass

        try:
            for fname, virus in iter(viruses.items()):
                print("F-Prot AV (file mode): Found virus: %s in %s" % (virus, fname))
                if "EICAR" in virus:
                    return True
        except Exception as e:
            print(e)
            return False

        print("Couldn't find EICAR in tmp file: %s" % fname)
        return False
