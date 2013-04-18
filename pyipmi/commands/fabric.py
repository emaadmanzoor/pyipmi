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

class FabricUpdateConfigCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric update config command"""
    name = "Update Config"
    result_type = FabricUpdateConfigResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "update_config"]

class FabricGetNodeIDCommand(Command, ResponseParserMixIn):
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

class FabricGetIPAddrCommand(Command, ResponseParserMixIn):
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

class FabricGetMacAddrCommand(Command, ResponseParserMixIn):
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

class FabricGetLinkspeedCommand(Command, ResponseParserMixIn):
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

fabric_commands = {
    "fabric_updateconfig"  :FabricUpdateConfigCommand,
    "fabric_getnodeid"  : FabricGetNodeIDCommand,
    "fabric_getipaddr" : FabricGetIPAddrCommand,
    "fabric_getmacaddr" : FabricGetMacAddrCommand,
    "fabric_getlinkspeed" : FabricGetLinkspeedCommand,
}
