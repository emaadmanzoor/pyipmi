#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from ipmi import Command
from ipmi.bmc import BMCInfo, BMCGuid
from ipmi.ipmitool import BOOL_VAL, ipmitool_command

@ipmitool_command
class GetDeviceIdCommand(Command):
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

@ipmitool_command
class GetSystemGuidCommand(Command):
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
