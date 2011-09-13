#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
from pyipmi import Command
from pyipmi.base.chassis import ChassisStatus
from pyipmi.tools.ipmitool import BOOL_VAL, IpmitoolCommandMixIn

class ChassisStatusCommand(Command, IpmitoolCommandMixIn):
    """Describes the chassis status IPMI command"""

    name = "Chassis Status"

    ipmitool_args = ["chassis", "status"]
    result_type = ChassisStatus

    ipmitool_response_fields = {
        'System Power' : {'attr' : 'power_on', 'conv' : lambda v: v == 'on'},
        'Power Overload' : {'conv' : BOOL_VAL},
        'Power Interlock' : {},
        'Main Power Fault' : {'conv' : BOOL_VAL},
        'Power Control Fault' : {'conv' : BOOL_VAL},
        'Power Restore Policy' : {}
    }

class ChassisControlCommand(Command, IpmitoolCommandMixIn):
    """Describes the IPMI chassis control command

    ipmitool calls this "chassis power"
    """

    @property
    def ipmitool_args(self):
        return ["chassis", "power", self._params["mode"]]

chassis_commands = {
    "chassis_status" : ChassisStatusCommand,
    "chassis_control" : ChassisControlCommand,
}
