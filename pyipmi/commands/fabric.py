#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.fabric import *

class FabricIPListCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve IP List"
    result_type = FabricIPListResult

    response_fields = {
        'File Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "config", "list_ip_addrs", "tftp",
                self._params['tftp_addr'], "file", self._params['filename']]

class FabricMACListCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem fabric list_macs IPMI command
    """

    name = "Retrieve MAC List"
    result_type = FabricMACListResult

    response_fields = {
        'File Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "config", "list_macs", "tftp",
                self._params['tftp_addr'], "file", self._params['filename']]

fabric_commands = {
    "fabric_iplist"  : FabricIPListCommand,
    "fabric_maclist" : FabricMACListCommand
}
