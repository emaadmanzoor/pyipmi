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


"""A series of wrappers around SOL commands"""

from pyipmi import Command, IpmiError
from pyipmi.tools.responseparser import ResponseParserMixIn, str2bool


def bit_rate_parser(bit_rate):
    """Parse a bit rate returned from ipmitool's "sol info" command"""
    assert bit_rate in ('IPMI-Over-Serial-Setting', '9.6', '19.2',
                        '38.4', '57.6', '115.2')

    if bit_rate != 'IPMI-Over-Serial-Setting':
        bit_rate = float(bit_rate)
    #TODO: maybe find the IPMI-Over-Serial-Setting?

    return bit_rate

def channel_parser(channel):
    """Parse a channel returned from ipmitool's "sol info" command.
    Channel format is: "%d (%x)" % (channel, channel)
    """

    chan, xchan = channel.split(' (')
    return int(chan)

def bool2str(boolval):
    """Map True to 'true', False to 'false'"""
    return str(boolval).lower()

def priv_level_formatter(level):
    """Format privilege level"""
    level = level.lower()
    if level == "administrator":
        level = "admin"
    return level

# need to know four ipmitool-specific things about each configuration parameter
# set_name: name used in ipmitool's "sol set" command
# get_name: name printed from ipmitool's "sol info" command
# parser: a function to parse the value printed by ipmitool's "sol info" command
# formatter: formatter tool-independant values into formats required by tool
IPMITOOL_SOL_PARAMETERS = {
                'set_in_progress': {
                    'set_name' : 'set-in-progress',
                    'get_name' : 'Set in progress',
                    'parser' : lambda s: s.replace('-', '_'),
                    'formatter' : lambda s: s.replace('_', '-'),
                },
                'enable' : {
                    'set_name' : 'enabled',
                    'get_name' : 'Enabled',
                    'parser' : str2bool,
                    'formatter' : bool2str,
                },
                'force_encryption' : {
                    'set_name' : 'force-encryption',
                    'get_name' : 'Force Encryption',
                    'parser' : str2bool,
                    'formatter' : bool2str,
                },
                'force_authentication' : {
                    'set_name' : 'force-authentication',
                    'get_name' : 'Force Authentication',
                    'parser' : str2bool,
                    'formatter' : bool2str,
                },
                'privilege_level' : {
                    'set_name' : 'privilege-level',
                    'get_name' : 'Privilege Level',
                    'parser' : str,
                    'formatter' : priv_level_formatter,
                },
                'character_accumulate_interval' : {
                    'set_name' : 'character-accumulate-level',
                    'get_name' : 'Character Accumulate Level (ms)',
                    'parser' : lambda s: int(s) / 5,
                    'formatter' : str,
                },
                'character_send_threshold' : {
                    'set_name' : 'character-send-threshold',
                    'get_name' : 'Character Send Threshold',
                    'parser' : int,
                    'formatter' : str,
                },
                'retry_count' : {
                    'set_name' : 'retry-count',
                    'get_name' : 'Retry Count',
                    'parser' : int,
                    'formatter' : str,
                },
                'retry_interval' : {
                    'set_name' : 'retry-interval',
                    'get_name' : 'Retry Interval (ms)',
                    'parser' : lambda s: int(s) / 10,
                    'formatter' : str,
                },
                'volatile_bit_rate' : {
                    'set_name' : 'volatile-bit-rate',
                    'get_name' : 'Volatile Bit Rate (kbps)',
                    'parser' : bit_rate_parser,
                    'formatter' : str,
                },
                'non_volatile_bit_rate' : {
                    'set_name' : 'non-volatile-bit-rate',
                    'get_name' : 'Non-Volatile Bit Rate (kbps)',
                    'parser' : bit_rate_parser,
                    'formatter' : str,
                },
                'payload_channel' : {
                    'set_name' : None,
                    'get_name' : 'Payload Channel',
                    'parser' : channel_parser,
                    'formatter' : None,
                },
                'payload_port_number' : {
                    'set_name' : None,
                    'get_name' : 'Payload Port',
                    'parser' : int,
                    'formatter' : None,
                }
}

# TODO: why does atom only work with lanplus, but qemu works on the lan iface?
# TODO: enable/disable encryption
IPMITOOL_SOL_ARGS = ["-I", "lanplus", "-C", "0", "sol"]

class SetSOLConfigurationParametersCommand(Command, ResponseParserMixIn):
    """Describes the Set SOL Configuration Parameters command"""

    # ipmitool handles setting set-in-progress/set-complete for us
    # however, other tools might not. this is where that'd be handled

    name = "Set SOL Configuration Parameters"

    @property
    def ipmitool_args(self):
        param = self._params['param']
        ipmitool_param = IPMITOOL_SOL_PARAMETERS[param]['set_name']
        formatter = IPMITOOL_SOL_PARAMETERS[param]['formatter']
        val = formatter(self._params['value'])

        if param is None:
            raise IpmiError('ipmitool does not support "sol set %s" ' % param)

        return IPMITOOL_SOL_ARGS + ["set", ipmitool_param, val, 'noguard']


class GetSOLConfigurationParametersCommand(Command, ResponseParserMixIn):
    """Describes the Get SOL Configuration Parameters command"""

    name = "Get SOL Configuration Parameters"
    ipmitool_args = IPMITOOL_SOL_ARGS + ["info"]

    def parse_results(self, response, err):
        """Parse the output from "sol info" for the desired parameters,
        format the result, and return it.
        """
        response = response.split('\n')
        result = {}

        params = self._params['params']
        for param in params:
            field = IPMITOOL_SOL_PARAMETERS[param]['get_name']
            parse = IPMITOOL_SOL_PARAMETERS[param]['parser']

            field_value, = filter(lambda s: s.find(field) == 0, response)
            field, value = field_value.split(': ')
            result[param] = parse(value)

        return result


sol_commands = {
    "set_sol_config_params" : SetSOLConfigurationParametersCommand,
    "get_sol_config_params" : GetSOLConfigurationParametersCommand
}
