#Copyright 2011-2012 Calxeda, Inc.  All Rights Reserved.

"""Chassis related IPMI commands"""
from .. import Command
from .. chassis import ChassisStatus
from pyipmi.tools.responseparser import ResponseParserMixIn, str2bool

class ChassisStatusCommand(Command, ResponseParserMixIn):
    """Describes the chassis status IPMI command"""

    name = 'Chassis Status'

    ipmitool_args = ['chassis', 'status']
    result_type = ChassisStatus

    response_fields = {
        'System Power' : {'attr' : 'power_on', 'parser' : lambda v: v == 'on'},
        'Power Overload' : {'parser' : str2bool},
        'Power Interlock' : {},
        'Main Power Fault' : {'parser' : str2bool},
        'Power Control Fault' : {'parser' : str2bool},
        'Power Restore Policy' : {}
    }

class ChassisControlCommand(Command, ResponseParserMixIn):
    """Describes the IPMI chassis control command

    ipmitool calls this "chassis power"
    """

    @property
    def ipmitool_args(self):
        """The chassis control command takes a 'mode' parameter

        Look at ipmitool's manpage for more info.
        """
        return ['chassis', 'power', self._params['mode']]

chassis_commands = {
    'chassis_status' : ChassisStatusCommand,
    'chassis_control' : ChassisControlCommand,
}
