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
from fuglu.shared import ScannerPlugin, DUNNO, string_to_actioncode, SuspectFilter
import os


class ActionOverridePlugin(ScannerPlugin):

    """ Override actions based on a Suspect Filter file. For example, delete all messages from a specific sender domain. """

    def __init__(self, config, section=None):
        ScannerPlugin.__init__(self, config, section)
        self.logger = self._logger()
        self.requiredvars = {
            'actionrules': {
                'default': '/etc/fuglu/actionrules.regex',
                'description': 'Rules file',
            }
        }
        self.filter = None

    def __str__(self):
        return "Action Override"

    def lint(self):
        allok = self.check_config() and self.lint_filter()
        return allok

    def lint_filter(self):
        filterfile = self.config.get(self.section, 'actionrules')
        sfilter = SuspectFilter(filterfile)
        return sfilter.lint()

    def examine(self, suspect):
        actionrules = self.config.get(self.section, 'actionrules')
        if actionrules is None or actionrules == "":
            return DUNNO

        if not os.path.exists(actionrules):
            self.logger.error(
                'Action Rules file does not exist : %s' % actionrules)
            return DUNNO

        if self.filter is None:
            self.filter = SuspectFilter(actionrules)

        (match, arg) = self.filter.matches(suspect)
        if match:
            if arg is None or arg.strip() == '':
                self.logger.error("Rule match but no action defined.")
                return DUNNO

            arg = arg.strip()
            spl = arg.split(None, 1)
            actionstring = spl[0]
            message = None
            if len(spl) == 2:
                message = spl[1]
            self.logger.debug(
                "%s: Rule match! Action override: %s" % (suspect.id, arg.upper()))

            actioncode = string_to_actioncode(actionstring, self.config)
            if actioncode is not None:
                return actioncode, message

            elif actionstring.upper() == 'REDIRECT':
                suspect.to_address = message.strip()
                # todo: check for invalid adress, multiple adressses, set suspect.recipients instead of to_address
                # todo: document redirect action
            else:
                self.logger.error("Invalid action: %s" % arg)
                return DUNNO

        return DUNNO
