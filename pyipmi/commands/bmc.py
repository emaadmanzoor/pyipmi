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


"""BMC related commands"""

from .. import Command
from .. bmc import BMCInfo, BMCGuid, BMCEnables, BMCResult, BMCResetResult
from pyipmi.tools.responseparser import ResponseParserMixIn, str2bool

class GetDeviceIdCommand(Command, ResponseParserMixIn):
    """Describes the get_device_id IPMI command

    This is "bmc info" to ipmitool
    """
    name = "Get Device ID"
    result_type = BMCInfo

    response_fields = {
        "Device ID" : {},
        "Device Revision" : {},
        "Firmware Revision" : {},
        "IPMI Version" : {},
        "Manufacturer ID" : {},
        "Product ID" : { "parser" : lambda s: s.split(' ')[0] },
        "Device Available" : { "parser" : str2bool }
    }

    ipmitool_args = ["bmc", "info"]


class BMCSelfTestCommand(Command, ResponseParserMixIn):
    """Describes the get self test results IPMI command

    This is "bmc selftest" to ipmitool
    """
    name = "BMC Self Test"
    result_type = BMCResult

    response_fields = {
        "Selftest" : { }
    }

    ipmitool_args = ["bmc", "selftest"]


class GetSystemGuidCommand(Command, ResponseParserMixIn):
    """Describes the get_system_guid IPMI command

    This is "bmc guid" to ipmitool
    """
    name = "Get System GUID"
    result_type = BMCGuid

    response_fields = {
        "System GUID" : {}
    }

    ipmitool_args = ["bmc", "guid"]

class GetCommandEnables(Command, ResponseParserMixIn):
    """The Get Command Enables command
    
    In ipmitool world, this is "bmc getenables"
    """
    name = 'Get Command Enables'
    result_type = BMCEnables

    response_fields = {
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


class BMCResetCommand(Command, ResponseParserMixIn):
    """The Get Command Enables command
    
    In ipmitool world, this is "bmc reset [warm|cold]"
    """
    name = 'BMC Reset'
    result_type = BMCResetResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ['bmc', 'reset', self._params['type']]


bmc_commands = {
    'get_device_id' : GetDeviceIdCommand,
    'get_system_guid' : GetSystemGuidCommand,
    'get_command_enables' : GetCommandEnables,
    'selftest' : BMCSelfTestCommand,
    'bmc_reset' : BMCResetCommand
}
