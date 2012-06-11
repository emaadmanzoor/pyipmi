#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

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
