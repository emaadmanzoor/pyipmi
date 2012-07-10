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


"""SDR related commands"""
import re

from .. import Command
from .. sdr import Sdr, AnalogSdr
from pyipmi.tools.responseparser import ResponseParserMixIn

class SdrListCommand(Command, ResponseParserMixIn):
    """Describes the sdr list command

    This is not a single IPMI request type - it's an ipmitool
    command that's composed of multiple IPMI requests.
    """

    name = 'SDR List'
    result_type = Sdr

    response_parser = ResponseParserMixIn.parse_colon_record_list
    ipmitool_args = ['-v', 'sdr', 'list', 'all']

    def sensor_name_parser(string):
        return string.split('(')[0].strip()

    def entity_id_parser(string):
        m = re.search('(\d.\d{1,2})', string)
        return m.groups()[0]

    def get_response_types(self, record):
        """Only matches Analog sensors right now.

           There are several more types of records to match, if they
           are needed.
        """
        if re.search('Sensor Type \(Analog\)', record):
            return AnalogSdr, self.analog_response_fields
        else:
            return None, None

    """
    Unparsed fields for analog sensors:

     Readable Thresholds   : lnr lcr lnc unc ucr unr 
     Settable Thresholds   : lnr lcr lnc unc ucr unr 
     Threshold Read Mask   : lnr lcr lnc unc ucr unr 
     Assertion Events      : 
     Assertions Enabled    : unc+ ucr+ unr+ 
     Deassertions Enabled  : unc+ ucr+ unr+
    """
    analog_response_fields = {
        'Sensor ID'             : {
                'attr' : 'sensor_name',
                'parser' : sensor_name_parser
        },
        'Entity ID'             : {
                'attr' : 'entity_id',
                'parser' : entity_id_parser
        },
        'Sensor Type (Analog)'  : { 'attr' : 'sensor_type' },
        'Sensor Reading'        : {},
        'Status'                : {},
        'Nominal Reading'       : {},
        'Normal Minimum'        : {},
        'Normal Maximum'        : {},
        'Upper non-recoverable' : {},
        'Upper critical'        : {},
        'Upper non-critical'    : {},
        'Lower non-recoverable' : {},
        'Lower critical'        : {},
        'Lower non-critical'    : {},
        'Positive Hysteresis'   : {},
        'Negative Hysteresis'   : {},
        'Minimum sensor range'  : {},
        'Maximum sensor range'  : {},
        'Event Message Control' : {},
    }

sdr_commands = {
    "get_sdr_list" : SdrListCommand
}
