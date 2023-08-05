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
from fuglu.shared import PrependerPlugin, SuspectFilter
import os


class PluginSkipper(PrependerPlugin):

    """Skips plugins based on standard filter file
This can be used for example to skip spam filters on outgoing messages.
e.g. put this in /etc/fuglu/skipplugins.regex:

@incomingport    1099    SAPlugin
"""

    def __init__(self, config, section=None):
        PrependerPlugin.__init__(self, config, section)
        self.filter = None
        self.requiredvars = {
            'filterfile': {
                'default': '/etc/fuglu/skipplugins.regex',
            }
        }
        self.logger = self._logger()

    def __str__(self):
        return "Plugin Skipper"

    def pluginlist(self, suspect, pluginlist):
        """Removes scannerplugins based on filter file"""
        if not self._initfilter():
            return None

        args = self.filter.get_args(suspect)
        # each arg should be a comma separated list of classnames to skip

        skippluginlist = []

        for arg in args:
            skippluginlist.extend(arg.split(','))

        listcopy = pluginlist[:]
        for plug in pluginlist:
            name = plug.__class__.__name__
            if name in skippluginlist:
                listcopy.remove(plug)
        return listcopy

    def _initfilter(self):
        if self.filter is not None:
            return True

        filename = self.config.get(self.section, 'filterfile')
        if filename is None or filename == "":
            return False

        if not os.path.exists(filename):
            self.logger.error('Filterfile not found for skipper: %s' % filename)
            return False

        self.filter = SuspectFilter(filename)
        return True

    def lint(self):
        return self.check_config() and self.lint_filter()

    def lint_filter(self):
        filterfile = self.config.get(self.section, 'filterfile')
        filter = SuspectFilter(filterfile)
        return filter.lint()


class AppenderSkipper(PrependerPlugin):

    """
    Skips appender plugins based on standard filter file
    
    This can be used for example to skip appenders on outgoing messages.
    e.g. put this in /etc/fuglu/skipappenders.regex:

    @incomingport    1099    PluginTime
    """

    def __init__(self, config, section=None):
        PrependerPlugin.__init__(self, config, section)
        self.filter = None
        self.requiredvars = {
            'filterfile': {
                'default': '/etc/fuglu/skipappenders.regex',
            }
        }
        self.logger = self._logger()

    def __str__(self):
        return "Appender Plugin Skipper"

    def appenderlist(self, suspect, pluginlist):
        """Removes appender plugins based on filter file"""
        if not self._initfilter():
            return None

        args = self.filter.get_args(suspect)
        # each arg should be a comma separated list of classnames to skip

        skippluginlist = []

        for arg in args:
            skippluginlist.extend(arg.split(','))

        listcopy = pluginlist[:]
        for plug in pluginlist:
            name = plug.__class__.__name__
            if name in skippluginlist:
                listcopy.remove(plug)
        return listcopy

    def _initfilter(self):
        if self.filter is not None:
            return True

        filename = self.config.get(self.section, 'filterfile')
        if filename is None or filename == "":
            return False

        if not os.path.exists(filename):
            self.logger.error('Filterfile not found for skipper: %s' % filename)
            return False

        self.filter = SuspectFilter(filename)
        return True

    def lint(self):
        return self.check_config() and self.lint_filter()

    def lint_filter(self):
        filterfile = self.config.get(self.section, 'filterfile')
        filter = SuspectFilter(filterfile)
        return filter.lint()
