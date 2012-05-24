#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.fabric import *

class FabricGetIPInfoCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve fabric IP info"
    result_type = FabricGetIPInfoResult

    response_fields = {
        'File Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                self._params['tftp_addr'], "file", self._params['filename']]

class FabricGetMACAddressesCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem fabric list_macs IPMI command
    """

    name = "Retrieve fabric MAC addresses"
    result_type = FabricGetMACAddressesResult

    response_fields = {
        'File Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                self._params['tftp_addr'], "file", self._params['filename']]

fabric_commands = {
    "fabric_getipinfo"  : FabricGetIPInfoCommand,
    "fabric_getmacaddresses" : FabricGetMACAddressesCommand
}
