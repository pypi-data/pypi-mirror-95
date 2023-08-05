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
from fuglu.shared import AVScannerPlugin, string_to_actioncode, DUNNO, actioncode_to_string
from fuglu.stringencode import force_bString, force_uString
from fuglu.protocolbase import set_keepalive_linux
import socket
import os
import struct
import threading
import errno
import subprocess
import time
import math

threadLocal = threading.local()
# it's probably a good idea to re-establish the connection every now and then
MAX_SCANS_PER_SOCKET = 5000


class ClamavPlugin(AVScannerPlugin):

    """This plugin passes suspects to a clam daemon. 

Actions: This plugin will delete infected messages. If clamd is not reachable or times out, messages can be DEFERRED.

Prerequisites: You must have clamd installed (for performance reasons I recommend it to be on the same box, but this is not absoluely necessary)

Notes for developers:


Tags:

 * sets ``virus['ClamAV']`` (boolean)
 * sets ``ClamavPlugin.virus`` (list of strings) - virus names found in message
"""

    def __init__(self, config, section=None):
        AVScannerPlugin.__init__(self, config, section)
        self.requiredvars = {
            'host': {
                'default': 'localhost',
                'description': 'hostname where clamd runs',
            },

            'port': {
                'default': '3310',
                'description': "tcp port number or path to clamd.sock for unix domain sockets\nexample /var/lib/clamav/clamd.sock or on ubuntu: /var/run/clamav/clamd.ctl ",
            },

            'timeout': {
                'default': '30',
                'description': 'socket timeout',
            },

            'pipelining': {
                'default': 'False',
                'description': "*EXPERIMENTAL*: Perform multiple scans over the same connection. May improve performance on busy systems.",
            },

            'maxsize': {
                'default': '22000000',
                'description': "maximum message size, larger messages will not be scanned.  \nshould match the 'StreamMaxLength' config option in clamd.conf ",
            },
            'retries': {
                'default': '3',
                'description': 'how often should fuglu retry the connection before giving up',
            },

            'virusaction': {
                'default': 'DEFAULTVIRUSACTION',
                'description': "action if infection is detected (DUNNO, REJECT, DELETE)",
            },

            'problemaction': {
                'default': 'DEFER',
                'description': "action if there is a problem (DUNNO, DEFER)",
            },

            'rejectmessage': {
                'default': 'threat detected: ${virusname}',
                'description': "reject message template if running in pre-queue mode and virusaction=REJECT",
            },
            
            'clamscanfallback': {
                'default': 'False',
                'description': "*EXPERIMENTAL*: fallback to clamscan if clamd is unavailable. YMMV, each scan can take 5-20 seconds and massively increase load on a busy system.",
            },
            
            'clamscan': {
                'default': '/usr/bin/clamscan',
                'description': "the path to clamscan executable",
            },
            
            'clamscantimeout': {
                'default': '30',
                'description': "process timeout",
            },
            'skip_on_previous_virus': {
                'default': 'none',
                'description': 'define AVScanner engine names causing current plugin to skip if they found already a virus',
            },
        }
        self.logger = self._logger()
        self.enginename = 'ClamAV'
    
    
    def __str__(self):
        return "Clam AV"

    def examine(self, suspect):
        if self._check_too_big(suspect):
            return DUNNO
        
        skip = self._skip_on_previous_virus(suspect)
        if skip:
            self.logger.info("%s %s" % (suspect.id, skip))
            return DUNNO

        content = suspect.get_source()

        for i in range(0, self.config.getint(self.section, 'retries')):
            try:
                viruses = self.scan_stream(content, suspect.id)
                actioncode, message = self._virusreport(suspect, viruses)
                return actioncode, message
            except socket.error as e:
                self.__invalidate_socket()

                # don't warn the first time if it's just a broken pipe which
                # can happen with the new pipelining protocol
                if not (i == 0 and e.errno == errno.EPIPE):
                    self.logger.warning("%s Error encountered while contacting clamd (try %s of %s): %s" % (
                        suspect.id, i + 1, self.config.getint(self.section, 'retries'), str(e)))
                else:
                    self.logger.exception(e)
            except Exception as e:
                self.logger.exception(e)
                self.__invalidate_socket()

        self.logger.error("%s Clamdscan failed after %s retries" %
                          (suspect.id, self.config.getint(self.section, 'retries')))
        
        if self.config.getboolean(self.section, 'clamscanfallback'):
            try:
                viruses = self.scan_shell(content)
                actioncode, message = self._virusreport(suspect, viruses)
                return actioncode, message
            except Exception:
                self.logger.error('%s failed to scan using fallback clamscan' % suspect.id)
        
        return self._problemcode()
    
    
    def scan_shell(self, content):
        clamscan = self.config.get(self.section, 'clamscan')
        timeout = self.config.getint(self.section, 'clamscantimeout')
        
        if not os.path.exists(clamscan):
            raise Exception('could not find clamscan executable in %s' % clamscan)
        
        try:
            process = subprocess.Popen([clamscan, u'-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE) # file data by pipe
            kill_proc = lambda p: p.kill()
            timer = threading.Timer(timeout, kill_proc, [process])
            timer.start()
            stdout = process.communicate(force_bString(content))[0]
            process.stdin.close()
            exitcode = process.wait()
            timer.cancel()
        except Exception:
            exitcode = -1
            stdout = b''
        
        if exitcode > 1: # 0: no virus, 1: virus, >1: error, -1 subprocess error
            raise Exception('clamscan error')
        elif exitcode < 0:
            raise Exception('clamscan timeout after %ss' % timeout)
        
        dr = {}
        
        for line in stdout.splitlines():
            line = line.strip()
            if line.endswith(b'FOUND'):
                filename, virusname, found = line.rsplit(None, 2)
                filename = force_uString(filename.rstrip(b':'))
                dr[filename] = force_uString(virusname)

        if dr == {}:
            return None
        else:
            return dr
    

    def scan_stream(self, content, suspectid ="(NA)"):
        """
        Scan byte buffer

        return either :
          - (dict) : {filename1: "virusname"}
          - None if no virus found
          - raises Exception if something went wrong
        """
        pipelining = self.config.getboolean(self.section, 'pipelining')
        s = self.__init_socket__(oneshot=not pipelining)
        s.sendall(b'zINSTREAM\0')
        default_chunk_size = 2048
        remainingbytes = force_bString(content)

        numChunksToSend = math.ceil(len(remainingbytes)/default_chunk_size)
        iChunk = 0
        chunklength = 0
        self.logger.debug('%s: sending message in %u chunks of size %u bytes' % (suspectid, numChunksToSend, default_chunk_size))

        while len(remainingbytes) > 0:
            iChunk = iChunk + 1
            chunklength = min(default_chunk_size, len(remainingbytes))
            #self.logger.debug('sending chunk %u/%u' % (iChunk,numChunksToSend))
            #self.logger.debug('sending %s byte chunk' % chunklength)
            chunkdata = remainingbytes[:chunklength]
            remainingbytes = remainingbytes[chunklength:]
            s.sendall(struct.pack(b'!L', chunklength))
            s.sendall(chunkdata)
        self.logger.debug('%s: sent chunk %u/%u, last number of bytes sent was %u' % (suspectid, iChunk, numChunksToSend, chunklength))
        self.logger.debug('%s: All chunks send, send 0 - size to tell ClamAV the whole message has been sent' % suspectid)
        s.sendall(struct.pack(b'!L', 0))
        self.logger.debug('%s: 0 has been sent, now wait for anser' % suspectid)
        dr = {}


        result = force_uString(self._read_until_delimiter(s, suspectid)).strip()
        self.logger.debug('%s: got result' % suspectid)

        if result.startswith('INSTREAM size limit exceeded'):
            raise Exception(
                "%s: Clamd size limit exeeded. Make sure fuglu's clamd maxsize config is not larger than clamd's StreamMaxLength" % suspectid)
        if result.startswith('UNKNOWN'):
            raise Exception("%s: Clamd doesn't understand INSTREAM command. very old version?" % suspectid)

        if pipelining:
            try:
                ans_id, filename, virusinfo = result.split(':', 2)
                filename = force_uString(filename.strip())  # use unicode for filename
                virusinfo = force_uString(virusinfo.strip())  # lets use unicode for the info
            except Exception:
                raise Exception("%s: Protocol error, could not parse result: %s" % (suspectid, result))

            threadLocal.expectedID += 1
            if threadLocal.expectedID != int(ans_id):
                raise Exception("Commands out of sync - expected ID %s - got %s" % (threadLocal.expectedID, ans_id))

            if virusinfo[-5:] == 'ERROR':
                raise Exception(virusinfo)
            elif virusinfo != 'OK':
                dr[filename] = virusinfo.replace(" FOUND", '')

            if threadLocal.expectedID >= MAX_SCANS_PER_SOCKET:
                try:
                    s.sendall(b'zEND\0')
                    s.close()
                finally:
                    self.__invalidate_socket()
        else:
            filename, virusinfo = result.split(':', 1)
            filename = force_uString(filename.strip())  # use unicode for filename
            virusinfo = force_uString(virusinfo.strip())  # use unicode for virus info
            if virusinfo[-5:] == 'ERROR':
                raise Exception(virusinfo)
            elif virusinfo != 'OK':
                dr[filename] = virusinfo.replace(" FOUND", '')
            s.close()

        if dr == {}:
            return None
        else:
            return dr
    
    
    def _read_until_delimiter(self, sock, suspectID = "(NA)"):
        data = b''
        maxFailedAttempts = 40
        failedAttempt = 0
        readtimeout = self.config.getint(self.section, 'timeout') * 3  # extra timeout condition
        starttime = time.time()
        
        while True:
            try:
                self.logger.debug(f"{suspectID}: try to receive chunk")
                chunk = sock.recv(4096)
                self.logger.debug(f"{suspectID}: Got chunk of length {len(chunk)}")
                if len(chunk) == 0:
                    # Extra timeout condition here because we don't reach the else
                    # statement and won't do this extra check. This happened in a docker
                    # swarm setup with multiple clam services during an update
                    runtime = time.time() - starttime
                    if runtime > readtimeout:
                        raise Exception(f"{suspectID}: 0-chunk-length read timeout after {runtime:.2f}s")
                    continue
                data += chunk
                if chunk.endswith(b'\0'):
                    self.logger.debug(f"{suspectID}: Got all chunks... data length {len(data)}")
                    break
                if b'\0' in chunk:
                    raise Exception("%s: Protocol error: got unexpected additional data after delimiter"%suspectID)
            except socket.error as e:
                # looks like there can be a socket error when we try to connect too quickly after sending, so
                # better retry several times
                # Got this idea from pyclamd, see:
                # https://bitbucket.org/xael/pyclamd/src/2089daa540e1343cf414c4728f1322c96a615898/pyclamd/pyclamd.py?at=default&fileviewer=file-view-default#pyclamd.py-614
                # There the sleep for 0.01 [s] for 5 tries, so 0.05 [s] in total to wait. But I'm happy to set a
                # maximum of 1 second by 40*0.025 [s] if this helps to avoid a complete rescan of the message
                time.sleep(0.025)
                failedAttempt += 1
                self.logger.warning("%s: Failed receive attempt %u/%u: %s" % (suspectID,failedAttempt, maxFailedAttempts, str(e)))
                if failedAttempt == maxFailedAttempts:
                    raise
            else:
                # Sometimes we get one socket error and after that we never get a proper answer to satisfy
                # break or exception condition in try block, neither are there subsequent socket errors.
                # This can lead to an endless loop where a worker remains forever in this while loop,
                # rendering the worker useless and causing high cpu load. We thus add this additional
                # loop termination condition.
                runtime = time.time() - starttime
                if runtime > readtimeout:
                    raise Exception(f"{suspectID}: Read timeout after {runtime:.2f}s")

        return data[:-1]  # remove \0 at the end
    
    
    def __invalidate_socket(self):
        threadLocal.clamdsocket = None
        threadLocal.expectedID = 0
    
    
    def __init_socket__(self, oneshot=False):
        """initialize a socket connection to clamd using host/port/file defined in the configuration
        this connection is initialized with clamd's "IDSESSION" and cached per thread

         set oneshot=True to get a socket without caching it and without initializing it with an IDSESSION
         """

        existing_socket = getattr(threadLocal, 'clamdsocket', None)

        socktimeout = self.config.getint(self.section, 'timeout')

        if existing_socket is not None and not oneshot:
            existing_socket.settimeout(socktimeout)
            return existing_socket

        clamd_HOST = self.config.get(self.section, 'host')
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
            s.settimeout(socktimeout)
            try:
                s.connect(sock)
            except socket.error:
                raise Exception('Could not reach clamd using unix socket %s' % sock)
        else:
            clamd_PORT = self.config.getint(self.section, 'port')
            proto = socket.AF_INET
            if ':' in clamd_HOST:
                proto = socket.AF_INET6
            s = socket.socket(proto, socket.SOCK_STREAM)
            s.settimeout(socktimeout)
            try:
                s.connect((clamd_HOST, clamd_PORT))
            except socket.error:
                raise Exception('Could not reach clamd using network (%s, %s)' % (clamd_HOST, clamd_PORT))
            # set keepalive options
            set_keepalive_linux(s)

        # initialize an IDSESSION
        if not oneshot:
            s.sendall(b'zIDSESSION\0')
            threadLocal.clamdsocket = s
            threadLocal.expectedID = 0
        return s
    
    
    def lint(self):
        viract = self.config.get(self.section, 'virusaction')
        print("Virusaction: %s" % actioncode_to_string(
            string_to_actioncode(viract, self.config)))
        allok = self.checkConfig() and self.lint_ping() and self.lint_version() and self.lint_eicar()
        
        if self.config.getboolean(self.section, 'clamscanfallback'):
            print('WARNING: Fallback to clamscan enabled')
            starttime = time.time()
            allok = self.lint_eicar('scan_shell')
            if allok:
                runtime = time.time()-starttime
                print('clamscan scan time: %.2fs' % runtime)

        # print lint info for skip
        self.lintinfo_skip()
        return allok
    
    
    def lint_ping(self):
        try:
            s = self.__init_socket__(oneshot=True)
        except Exception as e:
            print("Could not contact clamd: %s" % (str(e)))
            return False
        s.sendall(force_bString('PING'))
        result = s.recv(20000)
        print("Got Pong: %s" % force_uString(result))
        if result.strip() != b'PONG':
            print("Invalid PONG: %s" % force_uString(result))
        return True
    
    
    def lint_version(self):
        try:
            s = self.__init_socket__(oneshot=True)
        except Exception:
            return False
        s.sendall(b'VERSION')
        result = s.recv(20000)
        print("Got Version: %s" % force_uString(result))
        return True
