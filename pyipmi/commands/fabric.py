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

"""
This module holdes cxoem "fabric" commands other than "fabric config"
commands.
"""

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

class UpdateConfigCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric update config command"""
    name = "Update Config"
    result_type = FabricUpdateConfigResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "update_config"]

class GetNodeIDCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get nodeid command"""
    name = "Get NodeID command"
    result_type = int

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return int(out)

    response_fields = {
    }

    ipmitool_args = ["cxoem", "fabric", "get", "nodeid"]

class GetIPAddrCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get ipaddr command"""
    name = "Get ipaddr command"
    result_type = str

    def parse_response(self, out, err):
        return out.strip()

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        result = ["cxoem", "fabric", "get", "ipaddr"]
        if self._params.get('nodeid', None):
            result.extend(['node', self._params['nodeid']])
        if self._params.get('iface', None):
            result.extend(['interface', self._params['iface']])
        return result

class GetMacAddrCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get macaddr command"""
    name = "Get macaddr command"
    result_type = str

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return out.strip()

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        result = ["cxoem", "fabric", "get", "macaddr", "interface",
                self._params['iface']]
        if self._params.get('nodeid', None):
            result.extend(['node', self._params['nodeid']])
        return result

class AddMacAddrCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric add macaddr command"""
    name = "Add macaddr command"

    @property
    def ipmitool_args(self):
        result = ['cxoem', 'fabric', 'add',
                'macaddr', self._params['macaddr'],
                'interface', self._params['iface']]
        if self._params['nodeid']:
            result += ['node', self._params['nodeid']]
        return result


class RmMacAddrCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric rm macaddr command"""
    name = "Remove macaddr command"

    @property
    def ipmitool_args(self):
        result = ['cxoem', 'fabric', 'rm',
                'macaddr', self._params['macaddr'],
                'interface', self._params['iface']]
        if self._params['nodeid']:
            result += ['node', self._params['nodeid']]
        return result

class GetLinkspeedCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get linkspeed command"""
    name = "Get linkspeed command"
    result_type = float

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return float(out)

    @property
    def ipmitool_args(self):
        result = ['cxoem', 'fabric', 'get', 'linkspeed']
        if self._params.get('link', None):
            result.extend(['link', self._params['link']])
        if self._params.get('actual', None):
            result.extend(['actual'])
        return result

class GetLinkStatsCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric info link_stats command"""
    name = "Get link_stats command"
    result_type = FabricGetLinkStatsResult
    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    def parse_response(self, out, err):
        return out.strip()

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return [
                    'cxoem', 'fabric', 'info', 'link_stats',
                    'link', self._params['link'],
                    'tftp', tftp_args[0],
                    'file', self._params['filename']
                ]
            else:
                return [
                    'cxoem', 'fabric', 'info', 'link_stats',
                    'link', self._params['link'],
                    'tftp', tftp_args[0],
                    'port', tftp_args[1],
                    'file', self._params['filename']
                ]
        else:
            return [
                'cxoem', 'fabric', 'info', 'link_stats',
                'link', self._params['link'],
                'file', self._params['filename']
            ]

class GetLinkMapCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric info linkmap command"""
    name = "Get linkmap command"
    result_type = FabricGetLinkMapResult
    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    def parse_response(self, out, err):
        return out.strip()
        
    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "info", "linkmap", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "info", "linkmap", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "info", "linkmap", "file",
                    self._params['filename']]

class GetRoutingTableCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric info routing_table command"""
    name = "Get routing_table command"
    result_type = FabricGetRoutingTableResult
    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    def parse_response(self, out, err):
        return out.strip()

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "info", "routing_table", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "info", "routing_table", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "info", "routing_table", "file",
                    self._params['filename']]

class GetDepthChartCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric info depth_chart command"""
    name = "Get depth_chart command"
    result_type = FabricGetDepthChartResult
    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    def parse_response(self, out, err):
        return out.strip()
        
    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "info", "depth_chart", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "info", "depth_chart", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "info", "depth_chart", "file",
                    self._params['filename']]


class GetUplinkSpeedCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get uplink_speed command"""
    name = "Get uplink speed command"
    result_type = int

    def parse_response(self, out, err):
        """Returns the output given from running the command"""
        if err:
            raise IpmiError(err)
        return int(out)

    ipmitool_args = ['cxoem', 'fabric', 'get', 'uplink_speed']


class GetUplinkInfoCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get uplink_info command"""
    name = "Get uplink info command"
    result_type = str

    def parse_response(self, out, err):
        """Returns the output given from running the command"""
        if err:
            raise IpmiError(err)
        return str(out)

    ipmitool_args = ['cxoem', 'fabric', 'get', 'uplink_info']


fabric_commands = {
    "fabric_updateconfig"  :UpdateConfigCommand,
    "fabric_getnodeid"  : GetNodeIDCommand,
    "fabric_getipaddr" : GetIPAddrCommand,
    "fabric_getmacaddr" : GetMacAddrCommand,
    "fabric_getlinkspeed" : GetLinkspeedCommand,
    "fabric_getlinkstats" : GetLinkStatsCommand,
    "fabric_getlinkmap" : GetLinkMapCommand,
    "fabric_getdepthchart" : GetDepthChartCommand,
    "fabric_getroutingtable" : GetRoutingTableCommand,
    "fabric_addmacaddr" : AddMacAddrCommand,
    "fabric_rmmacaddr" : RmMacAddrCommand,
    "fabric_info_getroutingtable" : GetRoutingTableCommand,
    "fabric_info_getlinkmap" : GetLinkMapCommand,
    "fabric_info_getdepthchart" : GetDepthChartCommand,
    "fabric_getuplinkspeed" : GetUplinkSpeedCommand,
    "fabric_getuplinkinfo" : GetUplinkInfoCommand
}
