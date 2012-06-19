#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.mc import *

class CommandWithErrors(Command, ResponseParserMixIn):

    def parse_response(self, out, err):
        """Parse the response to a command

        The 'ipmitool_response_format' attribute is used to determine
        what parser to use to for interpreting the results.

        Arguments:
        out -- the text response of an command from stdout
        err -- the text response of an command from stderr
        """

        out = out + err
        return self.response_parser(out, err)

class MCResetCommand(CommandWithErrors):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve fabric IP info"
    result_type = MCResetResult

    response_fields = {
        "Error" : {}
    }

    @property
    def ipmitool_args(self):
        return ["mc", "reset", self._params['mode']]

mc_commands = {
    "mc_reset"  : MCResetCommand,
}
