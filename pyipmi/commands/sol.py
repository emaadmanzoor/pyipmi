#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

"""A series of wrappers around SOL commands"""

from pyipmi import Command
from pyipmi.tools.ipmitool import IpmitoolCommandMixIn
from pyipmi.sol import SOLConfigurationParameters


class SetSOLConfigurationParametersCommand(Command, IpmitoolCommandMixIn):
    """Describes the Set SOL Configuration Parameters command"""

    name = "Set SOL Configuration Parameters"
    ipmitool_args = ["sol", ""]


class GetSOLConfigurationParametersCommand(Command, IpmitoolCommandMixIn):
    """Describes the Get SOL Configuration Parameters command"""

    name = "Get SOL Configuration Parameters"
    ipmitool_args = ["sol", ""]
    result_type = SOLConfigurationParameters


sol_commands = {
    "set_sol_config_params" : SetSOLConfigurationParametersCommand,
    "get_sol_config_params" : GetSOLConfigurationParametersCommand
}
