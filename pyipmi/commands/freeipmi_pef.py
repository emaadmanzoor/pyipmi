# Copyright (c) 2012, Calxeda Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of Calxeda Inc. nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.


"""PEF related commands"""

from .. import Command
from pyipmi.freeipmi_pef import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class FreeIPMIPEFInfoCommand(Command, ResponseParserMixIn):
    """Describes the get PEF info IPMI command

    This is "--info" to ipmi-pef-config
    """
    name = "Get PEF Info and Capabilities"
    result_type = FreeIPMIPEFInfoResult

    response_fields = {
        'PEF version' : {},
        'Alert action' : {},
        'Power down action' : {},
        'Power reset action' : {},
        'Power cycle action' : {},
        'OEM action' : {},
        'Diagnostic interrupt action' : {},
        'OEM event record filtering' : {},
        'Number of Event Filter Table entries' : {},
        'Number of Event Filters' : {},
        'Number of Alert Policy entries' : {},
        'Number of Alert Strings' : {}
    }

    ipmi_pef_config_args = ['--info']


class FreeIPMIPEFCheckout(Command, ResponseParserMixIn):
    """Retrieve platform event filtering configuration

    """
    name = "Checkout PEF Configuration"

    def get_next_line(self, text):
        line, c, rest = text.partition('\n')
        line = line.strip()
        return line, rest

    def parse_section(self, rest):
        config_dict = {}
        line, rest = self.get_next_line(rest)
        while line != "EndSection":
            if line[0] == '#':
                line, rest = self.get_next_line(rest)
                continue
            keyname, c, value = line.partition(" ")
            config_dict[keyname.strip()] = value.strip()
            line, rest = self.get_next_line(rest)
        return config_dict, rest

    def parse_results(self, response, err):
        """Parse the output from "pef checkout."  If a filename was given,
        there will be no response
        """

        section_list = {}
        line, rest = self.get_next_line(response)
        while line != "":
            if line[0] == '#':
                line, rest = self.get_next_line(rest)
                continue
            keyword, c, value = line.partition(' ')
            if keyword.strip() == "Section":
                param_list, rest = self.parse_section(rest)
                section_list[value.strip()] = param_list
            line, rest = self.get_next_line(rest)
        return section_list

    @property
    def ipmi_pef_config_args(self):
        """
        """
        section = self._params.get("section")
        filename = self._params.get('filename')
        key = self._params.get('key')

        if filename:
            if section:
                section = "--section=%s" % section
            else:
                section = ""
            return ["--checkout", "--filename=" + filename, section]

        if key and section:
            return ["--checkout", "--key-pair=" + section + ":" + key]

        if section:
            return ["--checkout", "--section=" + section]

        return ["--checkout"]


class FreeIPMIPEFCommit(Command, ResponseParserMixIn):

    """Update PEF configuration from file or key-value pair

    """
    name = "Update PEF Configuration"
    result_type = FreeIPMIPEFCommitResult

    response_fields = {
    }

    @property
    def ipmi_pef_config_args(self):
        """
        """
        filename = self._params.get('filename')

        if filename:
            return ["--commit", "--filename=" + filename]

        key_value_pair = self._params.get('key_value_pair')
        section = self._params.get('section')
        if key_value_pair and section:
            return ["--commit", "--key-pair=" + section + ":" + key_value_pair]

        raise Exception("Command pef-config --commit requires either filename or key-value pair")


class FreeIPMIPEFDiff(Command, ResponseParserMixIn):
    """ Command to diff current PEF configuration against a file or key-value pair
    
    """
    name = "PEF Diff"
    result_type = FreeIPMIDiffResult

    response_fields = {
    }

    @property
    def ipmi_pef_config_args(self):
        """
        """
        filename = self._params.get('filename')
        section = self._params.get('section')
        key = self._params.get('key')

        if filename:
            if section:
                section = "--section=%s" % section
            else:
                section = ""
            return ["--diff", "--filename=" + filename, section]

        if key and section:
            return ["--diff", "--key-pair=" + section + ":" + key]

        raise Exception("Command pef-config --diff requires either filename or key")


class FreeIPMIPEFListSections(Command, ResponseParserMixIn):
    """Describes the get PEF list sections command

    """
    name = "List PEF Table Sections"

    def parse_results(self, response, err):
        """Parse the output from "--listsections," which is a list
        of section names separated by a single line break
        """
        result = map(lambda x: x.strip(), response.splitlines())
        return result

    ipmi_pef_config_args = ["--listsections"]


freeipmi_pef_commands = {
    'pef_config_info'   : FreeIPMIPEFInfoCommand,
    'pef_checkout'      : FreeIPMIPEFCheckout,
    'pef_commit'        : FreeIPMIPEFCommit,
    'pef_diff'          : FreeIPMIPEFDiff,
    'pef_list_sections' : FreeIPMIPEFListSections
}
