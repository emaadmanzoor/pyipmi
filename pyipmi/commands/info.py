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


from .. import Command
from pyipmi.info import *
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi import IpmiError

class InfoBasicCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem info basic IPMI command
    """

    name = "Retrieve basic SoC info"

    ipmitool_args = ["cxoem", "info", "basic"]

    def parse_results(self, out, err):
        """ Parse ipmitool output
        """
        result = InfoBasicResult()

        if out.startswith("Calxeda SoC"):
            for line in out.splitlines():
                line = line.lstrip()
                if line.startswith("Calxeda SoC"):
                    result.iana = int(line.split()[2].strip("()"), 16)
                elif line.startswith("Firmware Version"):
                    result.firmware_version = line.partition(":")[2].strip()
                elif line.startswith("SoC Version"):
                    result.ecme_version = line.partition(":")[2].strip()
                elif line.startswith("Build Number"):
                    result.ecme_build_number = line.partition(":")[2].strip()
                elif line.startswith("Timestamp"):
                    result.ecme_timestamp = int(line.split()[1].strip(":()"))
                elif line.startswith("Node EEPROM Image Version"):
                    result.node_eeprom_version = line.partition(":")[2].strip()
                elif line.startswith("Node EEPROM CFG id"):
                    result.node_eeprom_config = line.partition(":")[2].strip()
                elif line.startswith("Slot EEPROM Image Version"):
                    result.slot_eeprom_version = line.partition(":")[2].strip()
                elif line.startswith("Slot EEPROM CFG id"):
                    result.slot_eeprom_config = line.partition(":")[2].strip()
        elif err.startswith("Error: "):
            raise IpmiError(err.splitlines()[0][7:])
        else:
            raise IpmiError("Unknown Error")

        return result

class InfoCardCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem info card IPMI command
    """

    name = "Retrieve card info"

    ipmitool_args = ["cxoem", "info", "card"]

    result_type = InfoCardResult
    response_fields = {
        'Board Type' : {'attr' : 'type'},
        'Board Revision' : {'attr' : 'revision'}
    }

    def parse_results(self, out, err):
        result = ResponseParserMixIn.parse_results(self, out, err)
        if not (hasattr(result, 'type') and hasattr(result, 'revision')):
            raise IpmiError(out.strip())
        return result

info_commands = {
    "info_basic" : InfoBasicCommand,
    "info_card" : InfoCardCommand
}
