# Copyright (c) 2012, Calxeda Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of Calxeda Inc. nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.


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

class ChassisPolicyCommand(Command, ResponseParserMixIn):
    """Describes the IPMI chassis policy command"""

    @property
    def ipmitool_args(self):
        """The chassis policy command takes a 'state' parameter"""
        return ['chassis', 'policy', self._params['state']]

chassis_commands = {
    'chassis_status' : ChassisStatusCommand,
    'chassis_control' : ChassisControlCommand,
    'chassis_policy' : ChassisPolicyCommand
}
