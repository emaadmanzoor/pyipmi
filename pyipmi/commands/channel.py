#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
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


channel_commands = {
    'channel_info'            : ChannelInfoCommand
}
