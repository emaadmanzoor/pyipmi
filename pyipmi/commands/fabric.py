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
        tftp_args = self._params['tftp_addr'].split(":")
        if len(tftp_args) == 1:
            return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                    tftp_args[0], "file", self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                    tftp_args[0], "port", tftp_args[1], "file",
                    self._params['filename']]

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
        tftp_args = self._params['tftp_addr'].split(":")
        if len(tftp_args) == 1:
            return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                    tftp_args[0], "file", self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                    tftp_args[0], "port", tftp_args[1], "file",
                    self._params['filename']]

class FabricUpdateConfigCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric update config command"""
    name = "Update Config"
    result_type = FabricUpdateConfigResult
    
    response_fields = {
    }
    
    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "update_config"]

fabric_commands = {
    "fabric_getipinfo"  : FabricGetIPInfoCommand,
    "fabric_getmacaddresses" : FabricGetMACAddressesCommand,
    "fabric_updateconfig"  :FabricUpdateConfigCommand
}
