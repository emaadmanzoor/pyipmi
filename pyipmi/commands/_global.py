#Copyright 2011 Calxeda, Inc.  All Rights Reserved.
"""BMC (global) related commands"""

from .. import Command
from .. bmc import BMCInfo, BMCGuid
from .. tools.ipmitool import BOOL_VAL, IpmitoolCommandMixIn

class GetDeviceIdCommand(Command, IpmitoolCommandMixIn):
    """Describes the get_device_id IPMI command

    This is "bmc info" to ipmitool
    """
    name = "Get Device ID"
    result_type = BMCInfo

    ipmitool_response_fields = {
        "Device ID" : {},
        "Device Revision" : {},
        "Firmware Revision" : {},
        "IPMI Version" : {},
        "Manufacturer ID" : {},
        "Product ID" : { "conv" : lambda s: s.split(' ')[0] },
        "Device Available" : { "conv" : BOOL_VAL }
    }

    ipmitool_args = ["bmc", "info"]

class GetSystemGuidCommand(Command, IpmitoolCommandMixIn):
    """Describes the get_system_guid IPMI command

    This is "bmc guid" to ipmitool
    """
    name = "Get System GUID"
    result_type = BMCGuid

    ipmitool_response_fields = {
        "System GUID" : {}
    }

    ipmitool_args = ["bmc", "guid"]

global_commands = {
    "get_device_id" : GetDeviceIdCommand,
    "get_system_guid" : GetSystemGuidCommand
}
