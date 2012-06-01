#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn

class MCResetCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve fabric IP info"

    @property
    def ipmitool_args(self):
        return ["mc", "reset", self._params['mode']]

mc_commands = {
    "mc_reset"  : MCResetCommand,
}
