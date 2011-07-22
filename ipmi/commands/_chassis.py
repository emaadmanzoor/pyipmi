#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from ipmi import Command
from ipmi.chassis import ChassisStatus
from _helpers import *

chassis_status_fields = {
    'System Power' : {'attr' : 'power_on', 'conv' : lambda v: v == 'on'},
    'Power Overload' : {'conv' : BOOL_VAL},
    'Power Interlock' : {},
    'Main Power Fault' : {'conv' : BOOL_VAL},
    'Power Control Fault' : {'conv' : BOOL_VAL},
    'Power Restore Policy' : {}
}

class ChassisStatusCommand(Command):
    """Describes the chassis status IPMI command"""

    name = "Chassis Status"

    def ipmitool_args(self):
        return ["chassis", "status"]

    def ipmitool_parse_results(self, response):
        status = ChassisStatus()
        parse_response(status, response, chassis_status_fields)
        return status

class ChassisControlCommand(Command):
    """Describes the IPMI chassis control command

    ipmitool calls this "chassis power"
    """

    def ipmitool_args(self):
        return ["chassis", "power", self._params["mode"]]

    def ipmitool_parse_results(self, response):
        return None
