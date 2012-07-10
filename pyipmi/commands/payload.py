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


"""A series of wrappers around RMCP+ Payload commands"""

from pyipmi import Command, InteractiveCommand, IpmiError
from pyipmi.tools.responseparser import ResponseParserMixIn


class ActivatePayloadCommand(InteractiveCommand, ResponseParserMixIn):
    """Describes the Activate Payload command"""

    #TODO: there could be other payload types

    name = "Activate Payload"
    ipmitool_args = ["-I", "lanplus", "-C", "0", "sol", "activate"]


class DeactivatePayloadCommand(Command, ResponseParserMixIn):
    """Describes the Deactivate Payload command"""

    #TODO: there could be other payload types

    def handle_command_error(self, out, err):
        if err.find('Info: SOL payload already de-activated') > -1:
            return

        raise IpmiError(err)

    name = "Deactivate Payload"
    ipmitool_args = ["-I", "lanplus", "sol", "deactivate"]


payload_commands = {
    "activate_payload" : ActivatePayloadCommand,
    "deactivate_payload" : DeactivatePayloadCommand
}
