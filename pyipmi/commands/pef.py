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
from pyipmi.pef import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class PEFGetInfoCommand(Command, ResponseParserMixIn):
    """Describes the get PEF info IPMI command

    This is "pef info" to ipmitool
    """
    name = "Get PEF Capabilities"
    result_type = PEFInfoResult

    response_fields = {
        'Version' : {},
        'PEF table size' : {},
        'Alert policy table size' : {},
        'System GUID' : {},
        'Alert' : {},
        'Power-off' : {},
        'Reset' : {},
        'Power-cycle' : {},
        'OEM-defined' : {},
        'Diagnostic-interrupt' : {}
    }

    ipmitool_args = ["-v", "pef", "info"]


class PEFGetPolicyCommand(Command, ResponseParserMixIn):
    """Describes the get PEF policies ipmitool command

    This is "pef policy" to ipmitool
    """

    name = "Get PEF Policy"
    result_type = PEFPolicyResult

    response_fields = {
    }

    ipmitool_args = ["pef", "policy"]


class PEFGetStatusCommand(Command, ResponseParserMixIn):
    """Describes the get PEF status ipmitool command

    This is "pef status" to ipmitool
    """
    name = "Get PEF Status"
    result_type = PEFStatusResult

    response_fields = {
        'Last SEL addition' : {},
        'Last SEL record ID' : {},
        'Last S/W processed ID' : {},
        'Last BMC processed ID' : {},
        'PEF' : {},
        'PEF event messages' : {},
        'PEF startup delay' : {},
        'Alert startup delay' : {},
        'Alert' : {},
        'Power-off' : {},
        'Reset' : {},
        'Power-cycle' : {},
        'OEM-defined' : {},
        'Diagnostic-interrupt' : {}
    }

    ipmitool_args = ["pef", "status"]


class PEFListEntriesCommand(Command, ResponseParserMixIn):
    """Describes the get PEF list entries ipmitool command

    This is "pef list" to ipmitool
    """
    name = "List PEF Entries"

    response_parser = ResponseParserMixIn.parse_colon_record_list

    result_type = PEFListResult

    response_fields = {
        'PEF table entry' : {},
        'Status' : {}
    }

    ipmitool_args = ["-v", "pef", "list"]


pef_commands = {
    'pef_get_info'     : PEFGetInfoCommand,
    'pef_get_status'   : PEFGetStatusCommand,
    'pef_get_policies' : PEFGetPolicyCommand,
    'pef_list_entries' : PEFListEntriesCommand
}
