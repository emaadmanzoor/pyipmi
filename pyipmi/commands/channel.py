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


"""channel related commands"""

from .. import Command
from pyipmi.channel import *
from pyipmi.tools.responseparser import ResponseParserMixIn
import re


class ChannelInfoCommand(Command, ResponseParserMixIn):
    """Describes the get channel info IPMI command

    This is "channel info" to ipmitool
    """

    def parse_response(self, out, err):
        """ Strip out extraneous colons to allow more generic parsing
        """
        out_list = map(lambda x: x.strip(), out.split('\n'))
        new_out_list = []

        setting_prefix = 'Active'
        for line in out_list:
            m = re.match("Channel 0x([0-9a-fA-F]+) info:", line)
            if m:
                line = "Channel : %s" % m.group(1)

            m = re.match("(Alerting|Per-message Auth|User Level Auth|Access Mode)\s+:\s+(\S+)", line)
            if m:
                line = "%s %s : %s" % (setting_prefix, m.group(1), m.group(2))

            m = re.match("Volatile\(active\) Settings", line)
            if m:
                setting_prefix = 'Active'
                continue

            m = re.match("Non-Volatile Settings", line)
            if m:
                setting_prefix = 'NV'
                continue

            new_out_list.append(line)

        new_out = '\n'.join(new_out_list)
        return self.response_parser(new_out, err)

    name = "Channel Info"
    result_type = ChannelInfoResult

    response_fields = {
        'Channel' : {},
        'Channel Medium Type' : {},
        'Channel Protocol Type' : {},
        'Session Support' : {},
        'Active Session Count' : {},
        'Protocol Vendor ID' : {},
        'Active Alerting' : {},
        'Active Per-message Auth' : {},
        'Active User Level Auth' : {},
        'Active Access Mode' : {},
        'NV Alerting' : {},
        'NV Per-message Auth' : {},
        'NV User Level Auth' : {},
        'NV Access Mode' : {}
    }

    ipmitool_args = ["channel", "info"]


class ChannelGetAccessCommand(Command, ResponseParserMixIn):
    """Describes the get channel access IPMI command

    This is "channel getaccess" to ipmitool
    """

    response_parser = ResponseParserMixIn.parse_colon_record_list

    name = "Channel Get Access"
    result_type = ChannelGetAccessResult

    response_fields = {
        'Maximum User IDs' : {},
        'Enabled User IDs' : {},
        'User ID' : {},
        'User Name' : {},
        'Fixed Name' : {},
        'Access Available' : {},
        'Link Authentication' : {},
        'IPMI Messaging' : {},
        'Privilege Level' : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["channel", "getaccess", self._params['channel'],
                self._params['userid']]


class ChannelSetAccessCommand(Command, ResponseParserMixIn):
    """Describes the set channel access IPMI command

    This is "channel setaccess" to ipmitool
    """

    name = "Channel Set Access"
    result_type = ChannelSetAccessResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        callin = ipmi = link = priv_level = ""

        if self._params.get('callin'):
            callin = "callin=%s" % self._params.get('callin')
        if self._params.get('ipmi'):
            ipmi = "ipmi=%s" % self._params.get('ipmi')
        if self._params.get('link'):
            link = "link=%s" % self._params.get('link')
        if self._params.get('priv_level'):
            priv_level = "privilege=%s" % self._params.get('priv_level')

        return ["channel", "setaccess", self._params['channel'],
                self._params['userid'], callin, ipmi, link, priv_level]


class ChannelGetCiphersCommand(Command, ResponseParserMixIn):
    """Describes the get channel cipher suites IPMI command

    This is "channel getciphers <ipmi | sol>" to ipmitool
    """

    def parse_response(self, out, err):
        """ Strip out extraneous colons to allow more generic parsing
        """
        out.strip()
        output_list = map(lambda x: x.strip(), out.split('\n'))
        result = {}

        for line in output_list:
            if line == '':
                continue
            line_list = map(lambda x: x.strip(), line.split())
            if line_list[0] == 'ID':
                continue
            suite = line_list[0]
            result[suite] = ChannelGetCiphersResult()
            result[suite].iana = line_list[1]
            result[suite].auth_alg = line_list[2]
            result[suite].integrity_alg = line_list[3]
            result[suite].confidentiality_alg = line_list[4]

        return result

    name = "Channel Get Cipher Suites"
    result_type = ChannelGetCiphersResult

    @property
    def ipmitool_args(self):
        return ["channel", "getciphers", self._params['mode']]


channel_commands = {
    'channel_info'            : ChannelInfoCommand,
    'channel_get_access'      : ChannelGetAccessCommand,
    'channel_set_access'      : ChannelSetAccessCommand,
    'channel_get_ciphers'     : ChannelGetCiphersCommand
}
