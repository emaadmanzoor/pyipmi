#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from _chassis import *
from _global import *

ipmi_commands = {
    "chassis_status" : ChassisStatusCommand,
    "chassis_control" : ChassisControlCommand,
    "get_device_id" : GetDeviceIdCommand
}
