#Copyright 2011 Calxeda, Inc.  All Rights Reserved.
"""BMC (global) related commands"""

from .. import Command
from .. bmc import BMCInfo, BMCGuid, BMCEnables
from .. tools.ipmitool import str2bool, IpmitoolCommandMixIn

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
        "Product ID" : { "parser" : lambda s: s.split(' ')[0] },
        "Device Available" : { "parser" : str2bool }
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

class GetCommandEnables(Command, IpmitoolCommandMixIn):
    """The Get Command Enables command
    
    In ipmitool world, this is "bmc getenables"
    """
    name = 'Get Command Enables'
    result_type = BMCEnables

    ipmitool_response_fields = {
        'Receive Message Queue Interrupt' : {
                'attr' : 'recv_msg_intr',
                'parser' : str2bool
        },
        'Event Message Buffer Full Interrupt' : {
                'attr' : 'event_msg_intr',
                'parser' : str2bool
        },
        'Event Message Buffer' : {
                'attr' : 'event_msg',
                'parser' : str2bool
        },
        'System Event Logging' : {
                'attr' : 'system_event_log',
                'parser' : str2bool
        },
        'OEM 0' : {
                'attr' : 'oem0',
                'parser' : str2bool
        },
        'OEM 1' : {
                'attr' : 'oem1',
                'parser' : str2bool
        },
        'OEM 2' : {
                'attr' : 'oem2',
                'parser' : str2bool
        }
    }

    ipmitool_args = ['bmc', 'getenables']


global_commands = {
    'get_device_id' : GetDeviceIdCommand,
    'get_system_guid' : GetSystemGuidCommand,
    'get_command_enables' : GetCommandEnables
}
