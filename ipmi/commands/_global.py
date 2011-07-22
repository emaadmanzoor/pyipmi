#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from ipmi import Command
from ipmi.bmc import BMCInfo
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
        "Product ID" : {},
        "Device Available" : { "conv" : BOOL_VAL }
    }

    ipmitool_args = ["bmc", "info"]

global_commands = {
    "get_device_id" : GetDeviceIdCommand
}
