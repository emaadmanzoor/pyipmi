#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

"""A series of wrappers around SOL commands"""

from pyipmi import Command, IpmiError
from pyipmi.tools.ipmitool import IpmitoolCommandMixIn, str2bool
from pyipmi.sol import SOL_CONFIGURATION_PARAMETERS


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

# need to know three ipmitool-specific things about each configuration parameter
# set_name: name used in ipmitool's "sol set" command
# get_name: name printed from ipmitool's "sol info" command
# parser: a function to parse the value printed by ipmitool's "sol info" command
Ipmitool_SOL_Parameters = {'set in progress':{'set_name':'set-in-progress',
                                   'get_name':'Set in progress',
                                   'parser':str},
                'enable':{'set_name':'enabled',
                          'get_name':'Enabled',
                          'parser':str2bool},
                'force encryption':{'set_name':'force-encryption',
                                    'get_name':'Force Encryption',
                                    'parser':str2bool},
                'force authentication':{'set_name':'force-authentication',
                                       'get_name':'Force Authentication',
                                       'parser':str2bool},
                'privilege level':{'set_name':'privilege-level',
                                   'get_name':'Privilege Level',
                                   'parser':str},
                'character accumulate interval':{'set_name':'character-accumulate-level',
                                                 'get_name':'Character Accumulate Level (ms)',
                                                 'parser':int},
                'character send threshold':{'set_name':'character-send-threshold',
                                            'get_name':'Character Send Threshold',
                                            'parser':int},
                'retry count':{'set_name':'retry-count',
                               'get_name':'Retry Count',
                               'parser':int},
                'retry interval':{'set_name':'retry-interval',
                                  'get_name':'Retry Interval (ms)',
                                  'parser':int},
                'volatile bit rate':{'set_name':'volatile-bit-rate',
                                     'get_name':'Volatile Bit Rate (kbps)',
                                     'parser':bit_rate_parser},
                'non-volatile bit rate':{'set_name':'non-volatile-bit-rate',
                                         'get_name':'Non-Volatile Bit Rate (kbps)',
                                         'parser':bit_rate_parser},
                'payload channel':{'set_name':None,
                                   'get_name':'Payload Channel',
                                   'parser':channel_parser},
                'payload port number':{'set_name':None,
                                'get_name':'Payload Port',
                                'parser':int}}

class SetSOLConfigurationParametersCommand(Command, IpmitoolCommandMixIn):
    """Describes the Set SOL Configuration Parameters command"""

    name = "Set SOL Configuration Parameters"

    @property
    def ipmitool_args(self):
        param = self._params['param']
        ipmitool_param = Ipmitool_SOL_Parameters[param]['set_name']
        val = str(self._params['value']).lower()

        if param is None:
            raise IpmiError('ipmitool does not support "sol set %s" ' % param)

        return ["sol", "set", ipmitool_param, val]


class GetSOLConfigurationParametersCommand(Command, IpmitoolCommandMixIn):
    """Describes the Get SOL Configuration Parameters command"""

    name = "Get SOL Configuration Parameters"
    ipmitool_args = ["sol", "info"]

    def ipmitool_parse_results(self, response, err):
        """Parse the output from "sol info" for the desired parameters,
        format the result, and return it.
        """
        response = response.split('\n')
        result = {}

        params = self._params['params']
        for param in params:
            field = Ipmitool_SOL_Parameters[param]['get_name']
            parse = Ipmitool_SOL_Parameters[param]['parser']

            field_value, = filter(lambda s: s.find(field) == 0, response)
            field, value = field_value.split(': ')
            result[param] = parse(value)

        return result


sol_commands = {
    "set_sol_config_params" : SetSOLConfigurationParametersCommand,
    "get_sol_config_params" : GetSOLConfigurationParametersCommand
}
