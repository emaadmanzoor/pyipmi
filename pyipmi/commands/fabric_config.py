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


from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.fabric import *
from pyipmi import IpmiError

class CommandWithErrors(Command, ResponseParserMixIn):

    def parse_response(self, out, err):
        """Parse the response to a command

        The 'ipmitool_response_format' attribute is used to determine
        what parser to use to for interpreting the results.

        Arguments:
        out -- the text response of an command from stdout
        err -- the text response of an command from stderr
        """

        out = out + err
        return self.response_parser(out, err)

class GetIPInfoCommand(CommandWithErrors):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve fabric IP info"
    result_type = FabricGetIPInfoResult

    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "ipinfo", "file",
                    self._params['filename']]

class GetUplinkInfoCommand(CommandWithErrors):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve fabric Uplink info"
    result_type = FabricGetUplinkInfoResult

    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "config", "get", "uplink_info",
                        "tftp", tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "config", "get", "uplink_info",
                        "tftp", tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "uplink_info", "file",
                    self._params['filename']]


class GetMACAddressesCommand(CommandWithErrors):
    """ Describes the cxoem fabric list_macs IPMI command
    """

    name = "Retrieve fabric MAC addresses"
    result_type = FabricGetMACAddressesResult

    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "macaddrs", "file",
                    self._params['filename']]

class UpdateConfigCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config update config command"""
    name = "Update Config"

    ipmitool_args = ['cxoem', 'fabric', 'config', 'update_config']

class GetIPSrcCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get ipsrc command"""
    name = "Get ipsrc command"
    result_type = int

    def parse_response(self, out, err):
        return int(out)

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "config", "get", "ipsrc"]

class SetIPSrcCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric set ipsrc command"""
    name = "Set ipsrc command"

    @property
    def ipmitool_args(self):
        return ['cxoem',
                'fabric',
                'config',
                'set',
                'ipsrc',
                self._params['ipsrc_mode']]

class FactoryDefaultCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config factory_default command"""
    name = "Fabric config factory_default command"

    ipmitool_args = ['cxoem', 'fabric', 'config', 'factory_default']

class GetIPAddrBase(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config get ipaddr_base command"""
    name = "Get fabric config ipaddr_base command"
    result_type = str

    ipmitool_args = ['cxoem', 'fabric', 'config', 'get', 'ipaddr_base']

    def parse_response(self, out, err):
        return out.strip()

class SetIPAddrBase(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config set ipaddr_base command"""
    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'ipaddr_base',
                self._params['ipaddr']]

class GetLinkspeedCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config get linkspeed command"""
    name = "Get global linkspeed command"
    result_type = float

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return float(out)

    ipmitool_args = ['cxoem', 'fabric', 'config', 'get', 'linkspeed']

class SetLinkspeedCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config set linkspeed command"""
    name = "Set linkspeed command"

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'linkspeed',
                   self._params['linkspeed']]

class GetLinkspeedPolicyCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config get ls_policy command"""
    name = "Get global ls_policy command"
    result_type = int

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return int(out)

    ipmitool_args = ['cxoem', 'fabric', 'config', 'get', 'ls_policy']

class SetLinkspeedPolicyCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config set ls_policy command"""
    name = "Set linkspeed command"

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'ls_policy',
                   self._params['ls_policy']]

class GetUplinkCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config get uplink command"""
    name = "Get uplink command"
    result_type = int

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return int(out)

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'get', 'uplink', 'interface',
                self._params['iface']]

class SetUplinkCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config set uplink command"""
    name = "Set uplink command"

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'uplink',
                self._params['uplink'], 'interface', self._params['iface']]

class GetLinkUsersFactorCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config get lu_factor command"""
    name = "Get global link users factor command"
    result_type = int

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return int(out)

    ipmitool_args = ['cxoem', 'fabric', 'config', 'get', 'lu_factor']

class SetLinkUsersFactorCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric config set lu_factor command"""
    name = "Set global link users factor command"

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'lu_factor',
                   self._params['lu_factor']]

class SetMACAddressBaseCommand(Command, ResponseParserMixIn):
    name = "Set the base MAC address for a custom range"

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'macaddr_base',
                self._params['macaddr']]

class GetMACAddressBaseCommand(Command, ResponseParserMixIn):
    name = "Get the base MAC address for a custom range"
    result_type = str
    ipmitool_args = ['cxoem', 'fabric', 'config', 'get', 'macaddr_base']

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return out.strip()

class SetMACAddressMaskCommand(Command, ResponseParserMixIn):
    name = "Set the MAC address mask for a custom range"

    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'macaddr_mask',
                self._params['mask']]

class GetMACAddressMaskCommand(Command, ResponseParserMixIn):
    name = "Get the MAC address mask for a custom range"
    result_type = str
    ipmitool_args = ['cxoem', 'fabric', 'config', 'get', 'macaddr_mask']

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return out.strip()

class SetNetmaskCommand(Command, ResponseParserMixIn):
    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'netmask',
                self._params['netmask']]

class SetDefaultGatewayCommand(Command, ResponseParserMixIn):
    @property
    def ipmitool_args(self):
        return ['cxoem', 'fabric', 'config', 'set', 'defgw',
                self._params['ipaddr']]


fabric_config_commands = {
    "fabric_config_getipinfo"  : GetIPInfoCommand,
    "fabric_config_getmacaddresses" : GetMACAddressesCommand,
    "fabric_config_updateconfig"  : UpdateConfigCommand,
    "fabric_config_getipsrc" : GetIPSrcCommand,
    "fabric_config_setipsrc" : SetIPSrcCommand,
    "fabric_config_factory_default" : FactoryDefaultCommand,
    "fabric_config_get_ipaddr_base" : GetIPAddrBase,
    "fabric_config_set_ipaddr_base" : SetIPAddrBase,
    "fabric_config_getlinkspeed" : GetLinkspeedCommand,
    "fabric_config_setlinkspeed" : SetLinkspeedCommand,
    "fabric_config_getlinkspeedpolicy" : GetLinkspeedPolicyCommand,
    "fabric_config_setlinkspeedpolicy" : SetLinkspeedPolicyCommand,
    "fabric_config_getuplinkinfo" : GetUplinkInfoCommand,
    "fabric_config_getuplink" : GetUplinkCommand,
    "fabric_config_setuplink" : SetUplinkCommand,
    "fabric_config_getlinkusersfactor" : GetLinkUsersFactorCommand,
    "fabric_config_setlinkusersfactor" : SetLinkUsersFactorCommand,
    "fabric_config_set_macaddr_base" : SetMACAddressBaseCommand,
    "fabric_config_get_macaddr_base" : GetMACAddressBaseCommand,
    "fabric_config_set_macaddr_mask" : SetMACAddressMaskCommand,
    "fabric_config_get_macaddr_mask" : GetMACAddressMaskCommand,
    "fabric_config_set_netmask": SetNetmaskCommand,
    "fabric_config_set_defgw": SetDefaultGatewayCommand,
}
