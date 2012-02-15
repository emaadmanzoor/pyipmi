#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
"""lan config related commands"""

from .. import Command
from pyipmi.lan import *
from pyipmi.tools.responseparser import (ResponseParserMixIn,
                                         str_to_list,
                                         str_to_dict)


class LANPrintCommand(Command, ResponseParserMixIn):
    """Describes the lan print ipmitool command
    """
    name = "LAN Print"
    result_type = LANPrintResults

    def parse_response(self, out, err):
        """ Strip out extraneous colons to allow more generic parsing
        """
        new_out_list = map(lambda x: x.lstrip(' \t\n:'), out.split('\n'))
        new_out = reduce(lambda x, y: x + '\n' + y, new_out_list)

        return self.response_parser(new_out, err)

    response_fields = {
        'Set in Progress'       : {},
        'Auth Type Support'     : {'parser' : str_to_list},
        'Auth Type Enable'      : {'lines'  : 5,
                                   'parser' : str_to_dict,
                                   'operator' : ':',
                                   'delimiter' : '\n',
                                   'value_parser' : str_to_list},
        'IP Address Source'     : {},
        'IP Address'            : {},
        'Subnet Mask'           : {},
        'MAC Address'           : {},
        'SNMP Community String' : {},
        'IP Header'             : {'parser' : str_to_dict,
                                   'operator' : '=',
                                   'delimiter' : ' '},
        'BMC ARP Control'       : {'parser' : str_to_list,
                                   'delimiter' : ','},
        'Gratituous ARP Intrvl' : {},
        'Default Gateway IP'    : {},
        'Default Gateway MAC'   : {},
        'TFTP Server IP'        : {},
        'NTP Server IP'         : {},
        'TFTP UDP port'         : {},
        'NTP UDP port'          : {},
        '802.1q VLAN ID'        : {},
        '802.1q VLAN Priority'  : {},
        'RMCP+ Cipher Suites'  : {'parser' : str_to_list,
                                   'delimiter' : ','},
        'Cipher Suite Priv Max' : {}
    }

    @property
    def ipmitool_args(self):
        channel = self._params.get('channel', '')
        return ["lan", "print", channel]


class LANSetCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool lan set command
    """
    name = "LAN Set"
    result_type = LANSetResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["lan", "set", self._params['channel'], self._params['command'],
                self._params['param']]


lan_commands = {
    'lan_print'             : LANPrintCommand,
    'lan_set'               : LANSetCommand
}
