# -*- coding: utf-8 -*-
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

import code
import datetime
import inspect
import logging
import multiprocessing
import os
import re
import socket
import sys
import threading
import time
import traceback
import configparser
import fuglu.procpool
import fuglu.asyncprocpool
from fuglu import __version__ as FUGLU_VERSION
from fuglu.connectors.esmtpconnector import ESMTPServer
from fuglu.connectors.milterconnector import MilterServer
from fuglu.connectors.asyncmilterconnector import MilterServer as ASYNCMilterServer
from fuglu.connectors.ncconnector import NCServer
from fuglu.connectors.smtpconnector import SMTPServer
from fuglu.debug import ControlServer, CrashStore
from fuglu.funkyconsole import FunkyConsole
from fuglu.shared import (HAVE_BEAUTIFULSOUP, Suspect, default_template_values)
from fuglu.mshared import BasicMilterPlugin
from fuglu.stats import StatsThread
from fuglu.stringencode import force_bString, force_uString
from fuglu.threadpool import ThreadPool
from fuglu.mixins import DefConfigMixin


#--------------------#
#- exit error codes -#
#--------------------#
EXIT_NOTSET = -1
EXIT_EXCEPTION = -2
EXIT_LOGTERMERROR = -3
EXIT_FATAL = 66
# other positive ints result from
# counting errors in the setup

def check_version_status(lint=False):
    import pkg_resources
    """Check our version string in DNS for known issues and warn about them

    the lookup should be <7 chars of commitid>.<patch>.<minor>.<major>.versioncheck.fuglu.org
    in case of a release version, use 'release' instead of commit id

    lookup examples:
    - 0.9.1 -> 0.release.1.9.0.versioncheck.fuglu.org
    - 0.9.1rc5 -> 5.rc.1.9.0.versioncheck.fuglu.org
    - 0.9.1.dev20181204183236 -> 20181204183236.dev.1.9.0.versioncheck.fuglu.org

    DNS will return NXDOMAIN or 127.0.0.<bitmask>
    2: generic non security related issue
    4: low risk security issue
    8: high risk security issue
    """
    bitmaskmap = {
        2: "there is a known (not security related) issue with this version - consider upgrading",
        4: "there is a known low-risk security issue with this version - an upgrade is recommended",
        8: "there is a known high-risk security issue with this version - upgrade as soon as possible!",
    }

    try:
        version_obj = pkg_resources.parse_version(FUGLU_VERSION)._version
        if not isinstance(version_obj, pkg_resources.extern.packaging.version._Version):
            version_obj = None
    except AttributeError:
        # Older versions of setuptools (< 20.2.2) return a tuple.
        # Accessing "_version" will raise an attribute error.
        version_obj = None
    except Exception as e:
        # Skip test for other problems...
        logging.getLogger("fuglu.check_version_status").warning(str(e))
        version_obj = None

    if version_obj is None:
        logging.getLogger("fuglu.check_version_status")\
            .warning("Version string %s could not be parsed to pkg_resources version object", FUGLU_VERSION)
        return

    (major, minor, micro) = version_obj.release
    (stage_str, stage_id) = ('release', 0)

    if version_obj.dev:
        stage_str = version_obj.dev[0]
        stage_id = version_obj.dev[1]
    
    if version_obj.pre:
        stage_str = version_obj.pre[0]
        stage_id = version_obj.pre[1]

    if version_obj.post:
        stage_str = version_obj.post[0]
        stage_id = version_obj.post[1]

    parts = {
        'major': major,
        'minor': minor,
        'micro': micro,
        'stage_str': stage_str,
        'stage_id': stage_id
    }

    lookup = "{stage_id}.{stage_str}.{micro}.{minor}.{major}.versioncheck.fuglu.org".format(**parts)
    result = None
    try:
        result = socket.gethostbyname(lookup)
    except Exception:
        # DNS fails happen - try again next time
        pass

    if result is None:
        return

    ret = re.match(r'^127\.0\.0\.(?P<replycode>\d{1,4})$', result)
    if ret is not None:
        code = int(ret.groupdict()['replycode'])
        for bitmask, message in bitmaskmap.items():
            if code & bitmask == bitmask:
                logging.warn(message)
                if lint:
                    fc = FunkyConsole()
                    print(fc.strcolor(message, "yellow"))


def sigterm(signum, frame):
    """Handler for sigterm event, do the same as for sigint -> raise KeyboardInterrupt"""
    raise KeyboardInterrupt("SIGTERM received!")


class MainController(DefConfigMixin):
    """main class to startup and control the app"""

    def __init__(self, config, logQueue=None, logProcessFacQueue=None, nolog=False):
        """
        Main controller instance
        Note: The logQueue and logProcessFacQueue keyword args are only needed in the fuglu main process when logging
              to files. For default logging to the screen there is not logQueue needed.

        Args:
            config (configparser.RawConfigParser()): Config file parser (file already read)

        Keyword Args:
            logQueue (multiprocessing.queue or None): Queue where to put log messages (not directly used, only by loggers as defined in logtools.client_configurer)
            logProcessFacQueue (multiprocessing.queue or None): Queue where to put new logging configurations (logtools.logConfig objects)
            nolog (bool): if True set logging level to error which will basically prevent logging
        """

        # initialise mixin
        DefConfigMixin.__init__(self, config)

        self.requiredvars = {
            # main section
            'identifier': {
                'section': 'main',
                'description': """identifier can be any string that helps you identifying your config file\nthis helps making sure the correct config is loaded. this identifier will be printed out when fuglu is reloading its config""",
                'default': 'dist',
            },

            'daemonize': {
                'section': 'main',
                'description': "run as a daemon? (fork)",
                'default': "1",
            },
            
            'scantimelogger':{
                'section':'main',
                'description':"Enable session scantime logger",
                'default':"0",
            },

            'user': {
                'section': 'main',
                'description': "run as user",
                'default': "nobody",
            },

            'group': {
                'section': 'main',
                'description': "run as group",
                'default': "nobody",
            },

            'plugindir': {
                'section': 'main',
                'description': "comma separated list of directories in which fuglu searches for additional plugins and their dependencies",
                'default': "",
            },

            'plugins': {
                'section': 'main',
                'description': "what SCANNER plugins do we load, comma separated",
                'default': "archive,attachment,clamav,spamassassin",
            },

            'prependers': {
                'section': 'main',
                'description': "what PREPENDER plugins do we load, comma separated",
                'default': "debug,skip",
            },

            'appenders': {
                'section': 'main',
                'description': "what APPENDER plugins do we load, comma separated\nappender plugins are plugins run after the scanning plugins\nappenders will always be run, even if a a scanner plugin decided to delete/bounce/whatever a message\n(unless a mail is deferred in which case running the appender would not make sense as it will come again)",
                'default': "",
            },

            'bindaddress': {
                'section': 'main',
                'description': "address fuglu should listen on. usually 127.0.0.1 so connections are accepted from local host only",
                'default': "127.0.0.1",
            },

            'incomingport': {
                'section': 'main',
                'description': "incoming port(s) (postfix connects here)\nyou can use multiple comma separated ports here\nf.ex. to separate incoming and outgoing mail and a special port for debugging messages\n10025: standard incoming mail\n10099: outgoing mail\n10888: debug port",
                'default': "10025,10099,10888",
            },

            'outgoinghost': {
                'section': 'main',
                'description': "outgoing hostname/ip where postfix is listening for re-injects.\nuse ${injecthost} to connect back to the IP where the incoming connection came from",
                'default': "127.0.0.1",
            },

            'outgoingport': {
                'section': 'main',
                'description': "outgoing port  where postfix is listening for re-injects)",
                'default': "10026",
            },

            'outgoinghelo': {
                'section': 'main',
                'description': "#outgoing helo we should use for re-injects\nleave empty to auto-detect current hostname",
                'default': "",
            },

            'tempdir': {
                'section': 'main',
                'description': "temp dir where fuglu can store messages while scanning",
                'default': "/tmp",
            },

            'prependaddedheaders': {
                'section': 'main',
                'description': "String to prepend to added headers",
                'default': "X-Fuglu-",
            },

            'trashdir': {
                'section': 'main',
                'description': "If a plugin decides to delete a message, save a copy here\ndefault empty, eg. do not save a backup copy",
                'default': "",
            },

            'trashlog': {
                'section': 'main',
                'description': "list all deleted messages in 00-fuglutrash.log in the trashdir",
                'default': "0",
            },

            'disablebounces': {
                'section': 'main',
                'description': "if this is set to True/1/yes , no Bounces will be sent from Fuglu eg. after a blocked attachment has been detected\nThis may be used for debugging/testing to make sure fuglu can not produce backscatter",
                'default': "0",
            },
            
            'nobouncefile': {
                'section': 'main',
                'description': 'list of domains to which no bounces will be sent',
                'default': '/etc/fuglu/rules/nobounce.txt',
            },

            'debuginfoheader': {
                'section': 'main',
                'description': "write debug info header to every mail",
                'default': "0",
            },

            'spamstatusheader': {
                'section': 'main',
                'description': "write a Spamstatus YES/NO header",
                'default': "1",
            },

            'suspectidheader': {
                'section': 'main',
                'description': "write suspect ID to every mail",
                'default': "1",
            },

            'mrtgdir': {
                'section': 'main',
                'description': "write mrtg statistics",
                'default': "",
            },

            'controlport': {
                'section': 'main',
                'description': "port where fuglu provides statistics etc (used by fuglu_control). Can also be a path to a unix socket",
                'default': "/tmp/fuglu_control.sock",
            },

            'logtemplate': {
                'section': 'main',
                'description': "Log pattern to use for all suspects in fuglu log. set empty string to disable logging generic suspect info. Supports the usual template variables plus: ${size}, ${spam} ${highspam}, ${modified} ${decision} ${tags} (short tags representagion) ${fulltags} full tags output, ${decision}",
                'default': 'Suspect ${id} from=${from_address} to=${to_address} size=${size} spam=${spam} virus=${virus} modified=${modified} decision=${decision}',
            },

            'versioncheck': {
                'section': 'main',
                'description': "warn about known severe problems/security issues of current version.\nNote: This performs a DNS lookup of gitrelease.patchlevel.minorversion.majorversion.versioncheck.fuglu.org on startup and fuglu --lint.\nNo other information of any kind is transmitted to outside systems.\nDisable this if you consider the DNS lookup an unwanted information leak.",
                'default': '1',
            },

            'address_compliance_checker': {
                'section': 'main',
                'description': "Method to check mail address validity (\"Default\",\"LazyLocalPart\")",
                'default': "Default",
            },
            'address_compliance_fail_action': {
                'section': 'main',
                'description': "Action to perform if address validity check fails (\"defer\",\"reject\",\"discard\")",
                'default': "defer",
            },
            'address_compliance_fail_message': {
                'section': 'main',
                'description': "Reply message if address validity check fails",
                'default': "invalid sender or recipient address",
            },
            'remove_tmpfiles_on_error': {
                'section': 'main',
                'description': "Remove temporary message file from disk for receive or address compliance errors",
                'default': '1',
            },

            # performance section
            'minthreads': {
                'default': "2",
                'section': 'performance',
                'description': 'minimum scanner threads',
            },
            'maxthreads': {
                'default': "40",
                'section': 'performance',
                'description': 'maximum scanner threads',
            },
            'minfreethreads': {
                'default': "0",
                'section': 'performance',
                'description': 'minimum free scanner threads',
            },
            'backend': {
                'default': "thread",
                'section': 'performance',
                'description': "Method for parallelism, either 'thread' or 'process' ",
            },
            'initialprocs': {
                'default': "0",
                'section': 'performance',
                'description': "Initial number of processes when backend='process'. If 0 (the default), automatically selects twice the number of available virtual cores. Despite its 'initial'-name, this number currently is not adapted automatically.",
            },

            'att_mgr_cachesize': {
                'default': "50000000",
                'section': 'performance',
                'description': "Maximum cache size to keep attachemnts (archives extracted) per suspect during mail analysis (in bytes, default: 50MB)"
            },
            'att_mgr_default_maxextract': {
                'default': "50000000",
                'section': 'performance',
                'description': "Default maximum filesize to extract from archives (in bytes, default: 50MB)"
            },
            'att_mgr_hard_maxextract': {
                'default': "500000000",
                'section': 'performance',
                'description': "Upper maximum filesize limit to extract from archives (in bytes, default: 500MB)"
            },
            'att_mgr_default_maxnfiles': {
                'default': "500",
                'section': 'performance',
                'description': "Default limit for maximum number of files to be extracted from archives (default: 500)"
            },
            'att_mgr_hard_maxnfiles': {
                'default': "500",
                'section': 'performance',
                'description': "Upper limit for maximum number of files to be extracted from archives (default: 500)"
            },

            # spam section
            'defaultlowspamaction': {
                'default': "DUNNO",
                'section': 'spam',
                'description': """what to do with messages that plugins think are spam but  not so sure  ("low spam")\nin normal usage you probably never set this something other than DUNNO\nthis is a DEFAULT action, eg. anti spam plugins should take this if you didn't set \n a individual override""",
            },

            'defaulthighspamaction': {
                'default': "DUNNO",
                'section': 'spam',
                'description': """what to do with messages if a plugin is sure it is spam ("high spam") \nin after-queue mode this is probably still DUNNO or maybe DELETE for courageous people\nthis is a DEFAULT action, eg. anti spam plugins should take this if you didn't set\n a individual override """,
            },

            # virus section
            'defaultvirusaction': {
                'default': "DELETE",
                'section': 'virus',
                'description': """#what to do with messages if a plugin detects a virus\nin after-queue mode this should probably be DELETE\nin pre-queue mode you could use REJECT\nthis is a DEFAULT action, eg. anti-virus plugins should take this if you didn't set \n a individual override""",
            },

            # smtpconnector
            'requeuetemplate': {
                'default': "FUGLU REQUEUE(${id}): ${injectanswer}",
                'section': 'smtpconnector',
                'description': """confirmation template sent back to the connecting postfix for accepted messages""",
            },

            # esmtpconnector
            'queuetemplate': {
                'default': "${injectanswer}",
                'section': 'esmtpconnector',
                'description': """confirmation template sent back to the connecting client for accepted messages""",
            },
            'ignore_multiple_recipients': {
                'default': "0",
                'section': 'esmtpconnector',
                'description': """only deliver the message to the first recipient, ignore the others. This is useful in spamtrap setups where we don't want to create duplicate deliveries.""",
            },

            # databaseconfig
            'dbconnectstring': {
                'default': "",
                'section': 'databaseconfig',
                'description': """read runtime configuration values from a database. requires sqlalchemy to be installed""",
                'confidential': True,
            },

            'sql': {
                'default': """SELECT value FROM fugluconfig WHERE `section`=:section AND `option`=:option AND `scope` IN ('$GLOBAL',CONCAT('%',:to_domain),:to_address) ORDER BY `scope` DESC""",
                'section': 'databaseconfig',
                'description': """sql query that returns a configuration value override. sql placeholders are ':section',':option' in addition the usual suspect filter default values like ':to_domain', ':to_address' etc\nif the statement returns more than one row/value only the first value in the first row is used""",
            },

            # environment
            'boundarydistance': {
                'default': "0",
                'section': 'environment',
                'description': """Distance to the boundary MTA ("how many received headers should fuglu skip to determine the last untrusted host information"). Only required if plugins need to have information about the last untrusted host(SPFPlugin)""",
            },
            'trustedhostsregex': {
                'default': "",
                'section': 'environment',
                'description': """Optional regex that should be applied to received headers to skip trusted (local) mta helo/ip/reverse dns.\nOnly required if plugins need to have information about the last untrusted host and the message doesn't pass a fixed amount of hops to reach this system in your network""",
            },
            'trustedreceivedregex': {
                'default': "",
                'section': 'environment',
                'description': """Optional regex that should be applied to received headers to skip trusted (local) mta transfers (for example LMTP).\nOnly required if plugins need to have information about the last untrusted host and the message doesn't pass a fixed amount of hops to reach this system in your network""",
            },

            #  plugin alias
            'debug': {
                'default': "fuglu.plugins.p_debug.MessageDebugger",
                'section': 'PluginAlias',
            },

            'skip': {
                'default': "fuglu.plugins.p_skipper.PluginSkipper",
                'section': 'PluginAlias',
            },

            'fraction': {
                'default': "fuglu.plugins.p_fraction.PluginFraction",
                'section': 'PluginAlias',
            },

            'archive': {
                'default': "fuglu.plugins.archive.ArchivePlugin",
                'section': 'PluginAlias',
            },

            'attachment': {
                'default': "fuglu.plugins.attachment.FiletypePlugin",
                'section': 'PluginAlias',
            },

            'clamav': {
                'default': "fuglu.plugins.clamav.ClamavPlugin",
                'section': 'PluginAlias',
            },

            'spamassassin': {
                'default': "fuglu.plugins.sa.SAPlugin",
                'section': 'PluginAlias',
            },

            'vacation': {
                'default': "fuglu.plugins.vacation.VacationPlugin",
                'section': 'PluginAlias',
            },

            'actionoverride': {
                'default': "fuglu.plugins.actionoverride.ActionOverridePlugin",
                'section': 'PluginAlias',
            },

            'icap': {
                'default': "fuglu.plugins.icap.ICAPPlugin",
                'section': 'PluginAlias',
            },

            'sssp': {
                'default': "fuglu.plugins.sssp.SSSPPlugin",
                'section': 'PluginAlias',
            },

            'fprot': {
                'default': "fuglu.plugins.fprot.FprotPlugin",
                'section': 'PluginAlias',
            },

            'scriptfilter': {
                'default': "fuglu.plugins.script.ScriptFilter",
                'section': 'PluginAlias',
            },

            'dkimsign': {
                'default': "fuglu.plugins.domainauth.DKIMSignPlugin",
                'section': 'PluginAlias',
            },

            'dkimverify': {
                'default': "fuglu.plugins.domainauth.DKIMVerifyPlugin",
                'section': 'PluginAlias',
            },

            'spf': {
                'default': "fuglu.plugins.domainauth.SPFPlugin",
                'section': 'PluginAlias',
            },
        }

        self.config = config
        self.servers = []
        self.logger = self._logger()
        if nolog:
            self.logger.setLevel(logging.ERROR)
        self.stayalive = True
        self.threadpool = None
        self.procpool = None
        self.asyncprocpool = None
        self.controlserver = None
        self.started = datetime.datetime.now()
        self.statsthread = None
        self.debugconsole = False
        self._logQueue = logQueue
        self._logProcessFacQueue = logProcessFacQueue
        self.configFileUpdates = None
        self.logConfigFileUpdates = None
        self.plugins = []
        self.prependers = []
        self.appenders = []
        self.milterdict = {}

    @property
    def logQueue(self):
        return self._logQueue

    @property
    def logProcessFacQueue(self):
        return self._logProcessFacQueue

    @logProcessFacQueue.setter
    def logProcessFacQueue(self, lProc):
        self._logProcessFacQueue = lProc

    def _logger(self):
        myclass = self.__class__.__name__
        loggername = "fuglu.%s" % (myclass,)
        return logging.getLogger(loggername)
    
    @staticmethod
    def get_connectorinfo(portspec, default_protocol, default_bindaddress):
        protocol = default_protocol
        bindaddress = default_bindaddress
        port = portspec.strip()
        portformat = port.count(':')
        # 0: "port" -> example: 10028
        # 1: "protocol:port" -> example: milter:10028
        # 2: "protocol:bindaddress:port" -> example: milter:127.0.0.1:10028
        if portformat == 0:
            pass
        elif portformat == 1:
            protocol, port = port.split(':')
        elif portformat == 2:
            protocol, bindaddress, port = port.split(':')
        else:
            raise ValueError("Error in bind definition: %s"%portspec)
        return protocol, bindaddress, port

    def start_connector(self, portspec):
        protocol = 'smtp'
        bindaddress = self.config.get('main', 'bindaddress')

        protocol, bindaddress, port = MainController.get_connectorinfo(portspec, protocol, bindaddress)

        self.logger.info("starting connector %s/%s/%s" % (protocol, bindaddress, port))
        try:
            port = int(port)
            if protocol == 'smtp':
                smtpserver = SMTPServer(
                    self, port=port, address=bindaddress)
                tr = threading.Thread(target=smtpserver.serve, args=())
                tr.daemon = True
                tr.start()
                self.servers.append(smtpserver)
            elif protocol == 'esmtp':
                esmtpserver = ESMTPServer(
                    self, port=port, address=bindaddress)
                tr = threading.Thread(target=esmtpserver.serve, args=())
                tr.daemon = True
                tr.start()
                self.servers.append(esmtpserver)
            elif protocol == 'milter':

                backend = self.config.get('performance', 'backend')
                if backend == "asyncio":
                    self.logger.debug("Starting ASYNCMilterServer....")
                    milterserver = ASYNCMilterServer(
                        self, port=port, address=bindaddress)
                    milterserver.serve()
                else:
                    self.logger.debug("Starting MilterServer....")
                    milterserver = MilterServer(
                        self, port=port, address=bindaddress)

                    tr = threading.Thread(target=milterserver.serve, args=())
                    tr.daemon = True
                    tr.start()
                self.servers.append(milterserver)
            elif protocol == 'netcat':
                ncserver = NCServer(
                    self, port=port, address=bindaddress)
                tr = threading.Thread(target=ncserver.serve, args=())
                tr.daemon = True
                tr.start()
                self.servers.append(ncserver)
            else:
                self.logger.error(
                    'Unknown Interface Protocol: %s, ignoring server on port %s' % (protocol, port))
        except Exception as e:
            self.logger.error(
                "could not start connector %s/%s : %s" % (protocol, port, str(e)))

    def _start_stats_thread(self):
        self.logger.info("Init Stat Engine")
        statsthread = StatsThread(self.config)
        mrtg_stats_thread = threading.Thread(name='MRTG-Statswriter', target=statsthread.writestats, args=())
        mrtg_stats_thread.daemon = True
        mrtg_stats_thread.start()
        return statsthread

    def _start_threadpool(self):
        self.logger.info("Init Threadpool")
        try:
            minthreads = self.config.getint('performance', 'minthreads')
            maxthreads = self.config.getint('performance', 'maxthreads')
            minfreethreads = self.config.getint('performance', 'minfreethreads')
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.logger.warning('Performance section not configured, using default thread numbers')
            minthreads = 1
            maxthreads = 3
            minfreethreads = 0

        queuesize = maxthreads * 10
        return ThreadPool(self,
                          minthreads=minthreads, maxthreads=maxthreads,
                          queuesize=queuesize, freeworkers=minfreethreads)

    def _start_processpool(self):
        numprocs = self.config.getint('performance', 'initialprocs')
        if numprocs < 1:
            numprocs = multiprocessing.cpu_count() *2
        self.logger.info("Init process pool with %s worker processes"%(numprocs))
        pool = fuglu.procpool.ProcManager(self._logQueue, numprocs = numprocs, config = self.config)
        return pool

    def _start_async_processpool(self):
        numprocs = self.config.getint('performance', 'initialprocs')
        if numprocs < 1:
            numprocs = multiprocessing.cpu_count() * 2

        try:
            async_coroutines = self.config.getint('performance', 'async_coroutines', 10)
        except Exception as e:
            async_coroutines = 1

        queuesize = int(async_coroutines*numprocs*1.5)
        self.logger.info(f"Init async process pool with {numprocs} worker processes (queuesize={queuesize})")
        pool = fuglu.asyncprocpool.ProcManager(self._logQueue, numprocs=numprocs, config=self.config, queuesize=queuesize)
        return pool

    def _start_connectors(self):
        self.logger.info("Starting interface sockets...")
        ports = self.config.get('main', 'incomingport')
        for port in ports.split(','):
            self.start_connector(port)

    def _start_control_server(self):
        control = ControlServer(self, address=self.config.get(
            'main', 'bindaddress'), port=self.config.get('main', 'controlport'))
        ctrl_server_thread = threading.Thread(
            name='Control server', target=control.serve, args=())
        ctrl_server_thread.daemon = True
        ctrl_server_thread.start()
        return control

    def _run_main_loop(self):
        if self.debugconsole:
            self.run_debugconsole()
        else:
            if self.config.getboolean('main', 'versioncheck'):
                # log possible issues with this version
                check_version_status()

            backend = self.config.get('performance', 'backend')
            if backend == "asyncio":
                import asyncio
                loop = asyncio.get_event_loop()
                try:
                    loop.run_forever()
                except KeyboardInterrupt:
                    self.logger.info(f"Got keyboard interrupt")
                    self.stayalive = False
                except Exception as e:
                    self.logger.error("Catched exception in main loop!")
                    self.logger.exception(e)
                    self.logger.error("Stopping!")
                    self.stayalive = False
                finally:
                    self.logger.info('Shutdown...')
                    self.shutdown()
                    loop.close()
            else:
                # mainthread dummy loop
                while self.stayalive:
                    try:
                        time.sleep(1)
                    except KeyboardInterrupt:
                        self.stayalive = False
                    except Exception as e:
                        self.logger.error("Catched exception in main loop!")
                        self.logger.exception(e)
                        self.logger.error("Stopping!")
                        self.stayalive = False

    def startup(self):
        self.load_extensions()
        ok = self.load_plugins()
        if not ok:
            sys.stderr.write(
                "Some plugins failed to load, please check the logs. Aborting.\n")
            self.logger.info('Fuglu shut down after fatal error condition')
            return EXIT_FATAL

        self.statsthread = self._start_stats_thread()
        backend = self.config.get('performance', 'backend')
        if backend == 'process':
            self.procpool = self._start_processpool()
        elif backend == 'thread':
            self.threadpool = self._start_threadpool()
        elif backend == 'asyncprocess':
            self.asyncprocpool = self._start_async_processpool()

        self._start_connectors()
        self.controlserver = self._start_control_server()

        self.logger.info('Startup complete')
        self._run_main_loop()
        self.logger.info('Shutdown...')
        self.shutdown()
        return 0

    def run_debugconsole(self):

        # do not import readline at the top, it will cause undesired output, for example when generating the default config
        # http://stackoverflow.com/questions/15760712/python-readline-module-prints-escape-character-during-import

        print("Fuglu Interactive Console started")
        print("")
        print("pre-defined locals:")

        mc = self
        print("mc : maincontroller")

        terp = code.InteractiveConsole(locals())
        terp.interact("")

    def run_netconsole(self, port=1337, address="0.0.0.0"):
        """start a network console"""
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        addr_f = socket.getaddrinfo(address, 0)[0][0]

        serversocket = socket.socket(addr_f)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((address, port))
        serversocket.listen(1)
        clientsocket, _ = serversocket.accept()  # client socket
        self.logger.info("Interactive python connection from %s/%s" % (address, address))

        class sw(object):  # socket wrapper
            def __init__(self, s):
                self.s = s

            def read(self, length):
                return force_uString(self.s.recv(length))

            def write(self, st):
                return self.s.send(force_bString(st))

            def readline(self):
                return self.read(256)
        sw = sw(clientsocket)
        sys.stdin = sw
        sys.stdout = sw
        sys.stderr = sw
        mc = self
        terp = code.InteractiveConsole(locals())
        try:
            terp.interact("Fuglu Python Shell - MainController available as 'mc'")
        except Exception:
            pass
        self.logger.info("done talking to %s - closing interactive shell on %s/%s" % (address, address, port))
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        try:
            clientsocket.close()
        except Exception as e:
            self.logger.warning("Failed to close shell client socket: %s" % str(e))
        try:
            serversocket.close()
        except Exception as e:
            self.logger.warning("Failed to close shell server socket: %s" % str(e))

    def reload(self):
        """apply config changes"""
        self.logger.info('Applying configuration changes...')

        backend = self.config.get('performance', 'backend')

        if backend == 'thread':
            if self.threadpool is not None:
                minthreads = self.config.getint('performance', 'minthreads')
                maxthreads = self.config.getint('performance', 'maxthreads')
                minfreethreads = self.config.getint('performance', 'minfreethreads')

                if minthreads > maxthreads:
                    minthreads, maxthreads = maxthreads, minthreads

                self.threadpool.minthreads = minthreads
                self.threadpool.maxthreads = maxthreads
                self.threadpool.minfreethreads = minfreethreads
                self.logger.info('Keep existing threadpool')
            else:
                self.logger.info('Create new threadpool')
                self.threadpool = self._start_threadpool()

            # stop existing procpool
            if self.procpool is not None:
                self.logger.info('Delete old procpool')
                self.procpool.shutdown(self.threadpool)
                self.procpool = None

        elif backend == 'process':
            # start new procpool
            currentProcPool = self.procpool
            self.logger.info('Create new processpool')
            self.procpool = self._start_processpool()

            # stop existing procpool
            # -> the procpool has to be recreated to take configuration changes
            #    into account (each worker process has its own controller unlike using threadpool)
            if currentProcPool is not None:
                self.logger.info('Delete old processpool')
                currentProcPool.shutdown(self.procpool)

            # stop existing threadpool
            if self.threadpool is not None:
                self.logger.info('Delete old threadpool')
                self.threadpool.shutdown(self.procpool)
                self.threadpool = None
        else:
            self.logger.error('backend not detected -> ignoring input!')

        # smtp engine changes?
        ports = self.config.get('main', 'incomingport')
        portspeclist = ports.split(',')
        portlist = []

        for portspec in portspeclist:
            protocol = 'smtp'
            bindaddress = self.config.get('main', 'bindaddress')
            protocol, bindaddress, port = MainController.get_connectorinfo(portspec, protocol, bindaddress)

            # ideally we should check all three arguments
            port = int(port)

            portlist.append(port)
            alreadyRunning = False
            for serv in self.servers:
                if serv.port == port:
                    alreadyRunning = True
                    break

            if not alreadyRunning:
                self.logger.info('start new connector at %s' % str(portspec))
                self.start_connector(portspec)
            else:
                self.logger.info('keep connector at %s' % str(portspec))

        servercopy = self.servers[:]
        for serv in servercopy:
            if serv.port not in portlist:
                self.logger.info('Closing server socket on port %s' % serv.port)
                serv.shutdown()
                self.servers.remove(serv)
            else:
                self.logger.info('Keep server socket on port %s' % serv.port)

        self.logger.info('Config changes applied')

    def shutdown(self):
        if self.statsthread:
            self.statsthread.stayalive = False
        for server in self.servers:
            self.logger.info('Closing server socket on port %s' % server.port)
            server.shutdown()

        if self.controlserver is not None:
            self.controlserver.shutdown()

        # stop existing procpool
        if self.procpool is not None:
            self.logger.info('Delete procpool')
            self.procpool.shutdown()
            self.procpool = None
        # stop existing threadpool
        if self.threadpool is not None:
            self.logger.info('Delete threadpool')
            self.threadpool.shutdown()
            self.threadpool = None

        # stop existing async procpool
        if self.asyncprocpool is not None:
            self.logger.info('Delete async procpool')
            self.asyncprocpool.shutdown()
            self.asyncprocpool = None

        self.stayalive = False
        self.logger.info('Shutdown complete')
        self.logger.info('Remaining threads: %s' % threading.enumerate())

    def _lint_dependencies(self, fc):
        print(fc.strcolor('Checking dependencies...', 'magenta'))
        try:
            import sqlalchemy
            print(fc.strcolor('sqlalchemy: Version %s installed' % sqlalchemy.__version__, 'green'))
        except ImportError:
            print(fc.strcolor('sqlalchemy: not installed', 'yellow') +
                  " Optional dependency, required if you want to enable any database lookups")

        if HAVE_BEAUTIFULSOUP:
            import bs4 as BeautifulSoup
            print(fc.strcolor('BeautifulSoup: Version %s installed' % BeautifulSoup.__version__, 'green'))
            try:
                from lxml import etree
                if etree.LXML_VERSION <= (2,2):
                    print(fc.strcolor('WARNING: your lxml version is prone to segfaults. An update is recommended.', 'red'))
            except ImportError:
                print(fc.strcolor('ERROR: missing lxml as required dependency for BeautifulSoup', 'yellow'))
        else:
            print(fc.strcolor('BeautifulSoup: not installed', 'yellow') +
                  " Optional dependency, this improves accuracy for stripped body searches in filters - not required with a default config")

        try:
            import magic

            if hasattr(magic, 'open'):
                magic_vers = "python-file/libmagic bindings (http://www.darwinsys.com/file/)"
                print(fc.strcolor('magic: found %s' % magic_vers, 'green'))
            elif hasattr(magic, 'from_buffer'):
                magic_vers = "python-magic (https://github.com/ahupp/python-magic)"
                print(fc.strcolor('magic: found %s' % magic_vers, 'green'))
            else:
                print(fc.strcolor('magic: unsupported version', 'yellow') +
                      " File type detection requires either the python bindings from http://www.darwinsys.com/file/ or python magic from https://github.com/ahupp/python-magic")
        except ImportError:
            print(fc.strcolor('magic: not installed', 'yellow') +
                  " Optional dependency, without python-file or python-magic the attachment plugin's automatic file type detection will easily be fooled")

        try:
            import libmilter
            libmilter_vers = libmilter.__version__
            print(fc.strcolor('libmilter: found %s' % libmilter_vers, 'green'))
        except ImportError:
            print(fc.strcolor('libmilter: not installed', 'yellow') +
                  " Optional dependency, only needed if fuglu runs as milter")

    def lint(self):
        errors = 0
        fc = FunkyConsole()
        self._lint_dependencies(fc)

        print(fc.strcolor('Loading extensions...', 'magenta'))
        exts = self.load_extensions()
        for ext in exts:
            (name, enabled, status) = ext
            pname = fc.strcolor(name, 'cyan')
            if enabled:
                penabled = fc.strcolor('enabled', 'green')
            else:
                penabled = fc.strcolor('disabled', 'red')
            print("%s: %s (%s)" % (pname, penabled, status))

        print(fc.strcolor('Loading plugins...', 'magenta'))
        if not self.load_plugins():
            print(fc.strcolor('At least one plugin failed to load', 'red'))
            errors +=1
        print(fc.strcolor('Plugin loading complete', 'magenta'))

        print("Linting ", fc.strcolor("main configuration", 'cyan'))
        if not self.checkConfig():
            print(fc.strcolor("ERROR", "red"))
            errors += 1
        else:
            print(fc.strcolor("OK", "green"))

        trashdir = self.config.get('main', 'trashdir').strip()
        if trashdir != "" and not os.path.isdir(trashdir):
            print(fc.strcolor("Trashdir %s does not exist" % trashdir, 'red'))
            errors += 1

        # sql config override
        sqlconfigdbconnectstring = self.config.get('databaseconfig', 'dbconnectstring')
        if sqlconfigdbconnectstring.strip() != '':
            print()
            print("Linting ", fc.strcolor("sql configuration", 'cyan'))
            try:
                from fuglu.extensions.sql import get_session
                sess = get_session(sqlconfigdbconnectstring)
                tempsuspect = Suspect(
                    'sender@example.com', 'recipient@example.com', '/dev/null',
                    att_cachelimit=self.config.getint('performance', 'att_mgr_cachesize'),
                    att_defaultlimit=self.config.getint('performance', 'att_mgr_default_maxextract'),
                    att_maxlimit=self.config.getint('performance', 'att_mgr_hard_maxextract')
                )
                sqlvars = dict(
                    section='testsection', option='testoption', scope='$GLOBAL')
                default_template_values(tempsuspect, sqlvars)
                sess.execute(self.config.get('databaseconfig', 'sql'), sqlvars)
                sess.remove()
                print(fc.strcolor("OK", 'green'))
            except Exception as e:
                print(fc.strcolor("Failed %s" % str(e), 'red'))
                errors += 1

        allplugins = self.plugins + self.prependers + self.appenders

        perrors = 0
        for plugin in allplugins:
            print()
            print("Linting Plugin ", fc.strcolor(str(plugin), 'cyan'),
                  'Config section:', fc.strcolor(str(plugin.section), 'cyan'))
            try:
                result = plugin.lint()
            except Exception as e:
                CrashStore.store_exception()
                print("ERROR: %s" % e)
                result = False

            if result:
                print(fc.strcolor("OK", "green"))
            else:
                perrors += 1
                errors += 1
                print(fc.strcolor("ERROR", "red"))
        print("%s plugins reported errors." % perrors)

        if "milter" in self.config.get('main', 'incomingport') \
                and self.config.get('performance', 'backend') != 'process':

            try:
                minfreethreads = self.config.getint('performance', 'minfreethreads')
                if minfreethreads < 1:
                    print(fc.strcolor('\nMilter enabled with "thread" backend but "minfreethreads < 1"', 'yellow'))
                    print("To keep milter responsive it is recommended to set minfreethreads >= 1\n"
                          "to make fuglu more resonsive.\n")
            except (configparser.NoSectionError, configparser.NoOptionError):
                print(fc.strcolor('\nMilter enabled with "thread" backend but "minfreethreads is not defined!"', 'yellow'))
                print("To keep fuglu-milter responsive it is recommended to set minfreethreads >= 1\n")

        for state, allplugins in self.milterdict.items():
            perrors = 0
            for plugin in allplugins:
                print()
                print(f"Linting MPlugin (state={state})", fc.strcolor(str(plugin), 'cyan'),
                       'Config section:', fc.strcolor(str(plugin.section), 'cyan'))
                try:
                    result = plugin.lint(state=state)
                except Exception as e:
                    CrashStore.store_exception()
                    print("ERROR: %s" % e)
                    result = False

                if result:
                    print(fc.strcolor("OK", "green"))
                else:
                    perrors += 1
                    errors += 1
                    print(fc.strcolor("ERROR", "red"))
            if allplugins:
                print(f"{perrors} milter-plugins (state={state})reported errors.")

        if self.config.getboolean('main', 'versioncheck'):
            check_version_status(lint=True)

        return errors

    @staticmethod
    def propagate_defaults(requiredvars, config, defaultsection=None):
        """propagate defaults from requiredvars if they are missing in config"""
        for option, infodic in requiredvars.items():
            if 'section' in infodic:
                section = infodic['section']
            else:
                section = defaultsection
                if defaultsection is None:
                    raise ValueError(f"Option({option}): Defaultsection can not be None if it is actually used!")

            default = infodic['default']

            if not config.has_section(section):
                config.add_section(section)

            if not config.has_option(section, option):
                config.set(section, option, default)

    def propagate_core_defaults(self):
        """check for missing core config options and try to fill them with defaults
        must be called before we can do plugin loading stuff
        """
        MainController.propagate_defaults(self.requiredvars, self.config, 'main')

    def checkConfig(self):
        """Check if all required options without default are in the config file
        Fill missing values with defaults if possible
        """
        all_ok = True
        fc = FunkyConsole()
        for config, infodic in self.requiredvars.items():
            section = infodic['section']
            try:
                var = self.config.get(section, config)

                if 'validator' in infodic and not infodic["validator"](var):
                    print("Validation failed for [%s] :: %s" % (section, config))
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
                section = infodic['section']
                if section not in missingsections and not self.config.has_section(section):
                    missingsections.add(section)

            for section in missingsections:
                print(fc.strcolor(f"Missing configuration section [{section}] :: "
                              f"All variables will use default values", "yellow"))
        return all_ok

    def load_extensions(self):
        """load fuglu extensions"""
        ret = []
        import fuglu.extensions
        for extension in fuglu.extensions.__all__:
            mod = __import__('fuglu.extensions.%s' % extension)
            ext = getattr(mod, 'extensions')
            fl = getattr(ext, extension)
            enabled = getattr(fl, 'ENABLED')
            status = getattr(fl, 'STATUS')
            name = getattr(fl, '__name__')
            ret.append((name, enabled, status))
        return ret

    def get_component_by_alias(self, pluginalias):
        """Returns the full plugin component from an alias. if this alias is not configured, return the original string"""

        try:
            pluginalias = self.config.get("PluginAlias", pluginalias)
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass
        
        return pluginalias

    def load_plugins(self, propagate_plugin_config: bool=False):
        """
        load plugins defined in config

        propagate_plugin_default is only used by "fuglu_conf" to propagate the default values into the
        config for printing defaults/changed values
        """
        allOK = True
        plugindirs = [dir for dir in self.config.get('main', 'plugindir').strip().split(',') if dir]
        for plugindir in plugindirs:
            if os.path.isdir(plugindir):
                self.logger.debug('Searching for additional plugins in %s' % plugindir)
                if plugindir not in sys.path:
                    sys.path.insert(0, plugindir)
            else:
                self.logger.warning('Plugin directory %s not found' % plugindir)

        self.logger.debug('Module search path %s' % sys.path)
        self.logger.debug('Loading scanner plugins')
        newplugins, loadok = self._load_all(self.config.get('main', 'plugins'))
        if not loadok:
            allOK = False

        newprependers, loadok = self._load_all(
            self.config.get('main', 'prependers'))
        if not loadok:
            allOK = False

        newappenders, loadok = self._load_all(
            self.config.get('main', 'appenders'))
        if not loadok:
            allOK = False

        try:
            milterplugins, loadok = self._load_all(
                self.config.get('main', 'mplugins'))
            if not loadok:
                allOK = False
        except (configparser.NoSectionError, configparser.NoOptionError):
            milterplugins = []

        try:
            # create new dictionary with keys of all milter states
            milterdict = dict((k, []) for k in BasicMilterPlugin.ALL_STATES.keys())
            for mplugin in milterplugins:
                for s in mplugin.state:
                    milterdict[s].append(mplugin)
        except Exception as e:
            self.logger.error(f"ERROR: {e}", exc_info=e)
            milterdict = {}
            allOK = False

        if allOK:
            self.plugins = newplugins
            self.prependers = newprependers
            self.appenders = newappenders
            self.milterdict = milterdict
            if propagate_plugin_config:
                self._propagate_plugin_defaults_to_config()

        return allOK

    def _load_all(self, configstring):
        """load all plugins from config string. returns tuple ([list of loaded instances],allOk)"""
        pluglist = []
        config_re = re.compile(
            """^(?P<structured_name>[a-zA-Z0-9\.\_\-]+)(?:\((?P<config_override>[a-zA-Z0-9\.\_\-]+)\))?$""")
        allOK = True
        plugins = configstring.split(',')
        for plug in plugins:
            if plug == "":
                continue
            m = config_re.match(plug)
            if m is None:
                self.logger.error('Invalid Plugin Syntax: %s' % plug)
                allOK = False
                continue
            structured_name, configoverride = m.groups()
            structured_name = self.get_component_by_alias(structured_name)
            try:
                plugininstance = self._load_component(
                    structured_name, configsection=configoverride)
                pluglist.append(plugininstance)
            except (configparser.NoSectionError, configparser.NoOptionError):
                CrashStore.store_exception()
                self.logger.error("The plugin %s is accessing the config in __init__ -> can not load default values" % structured_name)
            except Exception as e:
                CrashStore.store_exception()
                self.logger.error('Could not load plugin %s : %s' %
                                     (structured_name, e))
                exc = traceback.format_exc()
                self.logger.error(exc)
                allOK = False

        return pluglist, allOK

    def _load_component(self, structured_name, configsection=None):
        # from:
        # http://mail.python.org/pipermail/python-list/2003-May/204392.html
        component_names = structured_name.split('.')
        mod = __import__('.'.join(component_names[:-1]))
        for component_name in component_names[1:]:
            mod = getattr(mod, component_name)

        if configsection is None:
            plugininstance = mod(self.config)
        else:
            # check if plugin supports config override
            if 'section' in inspect.getargspec(mod.__init__)[0]:
                plugininstance = mod(self.config, section=configsection)
            else:
                raise Exception('Cannot set Config Section %s : Plugin %s does not support config override' % (
                    configsection, mod))
        return plugininstance

    def _propagate_plugin_defaults_to_config(self):
        """
        propagate_plugin_default is only used by "fuglu_conf" to propagate the default values into the
        config for printing defaults/changed values
        """

        # plugins, prependers, appenders
        milterplugins = []
        for mpluginlist in self.milterdict.values():
            if mpluginlist:
                milterplugins.extend(mpluginlist)
        print(f"propagate... milterplugins: {milterplugins}")

        allplugs = self.plugins + self.prependers + self.appenders + milterplugins
        remove_plugin = []
        for plug in allplugs:
            if hasattr(plug, 'requiredvars'):
                requiredvars = getattr(plug, 'requiredvars')
                if type(requiredvars) == dict:
                    try:
                        MainController.propagate_defaults(requiredvars, self.config, plug.section)
                    except ValueError:
                        remove_plugin.append(plug)

        if len(remove_plugin) > 0:
            # if there are problems print then to screen and into log.
            # The screen output will be ignored in daemon mode but there
            # are the log messages
            fc = FunkyConsole()

            msg_string = "Warning: \"None\" plugin section name found in %u plugin%s!" % \
                         (len(remove_plugin), "s" if len(remove_plugin) > 1 else "")

            print(fc.strcolor(msg_string, "yellow"))
            self.logger.warning(msg_string)

            for plug in remove_plugin:
                if plug in self.plugins:
                    msg_string = "Warning: Removing plugin %s from plugin-list" % plug
                    self.logger.warning(msg_string)
                    print(fc.strcolor(msg_string, "yellow"))

                    self.plugins.remove(plug)
                elif plug in self.prependers:
                    msg_string = "Warning: Removing plugin %s from prependers-list" % plug
                    self.logger.warning(msg_string)
                    print(fc.strcolor(msg_string, "yellow"))

                    self.prependers.remove(plug)
                elif plug in self.appenders:
                    msg_string = "Warning: Removing plugin %s from appenders-list" % plug
                    self.logger.warning(msg_string)
                    print(fc.strcolor(msg_string, "yellow"))
                    self.appenders.remove(plug)
                else:
                    msg_string = "Error: Could not remove plugin %s, not found in any list!" % str(plug)
                    self.logger.error(msg_string)
                    print(fc.strcolor(msg_string, "red"))
                    raise ValueError("Plugin %s with bad config section name not found in any list!" % str(plug))
