#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from ipmi import Command
from ipmi.bmc import BMCInfo
from _helpers import *

bmc_info_fields = {
    "Device ID" : {},
    "Device Revision" : {},
    "Firmware Revision" : {},
    "IPMI Version" : {},
    "Manufacturer ID" : {},
    "Product ID" : {},
    "Device Available" : { "conv" : BOOL_VAL }
}

class GetDeviceIdCommand(Command):
    """Describes the get_device_id IPMI command

    This is "bmc info" to ipmitool
    """

    name = "Get Device ID"
    ipmitool_args = ["bmc", "info"]

    def ipmitool_parse_results(self, response):
        status = BMCInfo()
        parse_response(status, response, bmc_info_fields)
        return status
