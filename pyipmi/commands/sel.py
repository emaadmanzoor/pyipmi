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


"""This module contains a series of wrappers
   around SEL commands for ipmitool
"""

import os
import re
import tempfile
import string
from pyipmi import Command, IpmiError
from pyipmi.tools.responseparser import ResponseParserMixIn, str2bool
from pyipmi.sel import (SELTimestamp, SELInfo, SELAllocInfo, SELRecord,
                        SELOverflowError, SELTimestampError)


class SELTimeSetCommand(Command, ResponseParserMixIn):
    """Describes the Set SEL Time command"""

    name = "Set SEL Time"
    # TODO: get response data from ipmitool

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "time", "set", self._params["time"].timestamp]

    def handle_command_error(self, resp, err):
        raise SELTimestampError(err)


class SELTimeGetCommand(Command, ResponseParserMixIn):
    """Describes the Get SEL Time command"""

    def response_parser(self, resp, err):
        """A helper function to parse a timestamp returned from 
        an 'sel time get' command
        """

        return SELTimestamp(resp.strip())

    name = "Get SEL Time"
    result_type = SELTimestamp
    ipmitool_args = ["sel", "time", "get"]


class SELInfoCommand(Command, ResponseParserMixIn):
    """Describes the Get SEL Info command"""

    def version_parser(string):
        vdict = {}
        vregex = '(?P<number>[12]\.[05]) \((?P<compliant>.+) compliant\)'
        match = re.match(vregex, string)
        vdict['number'] = match.group('number')
        vdict['compliant'] = match.group('compliant').split(', ')
        return vdict

    name = "SEL Info"
    ipmitool_args = ["sel", "info"]
    result_type = SELInfo

    response_fields = {
        'Version' : {'parser': version_parser},
        'Entries' : {'parser': lambda s: int(s)},
        'Free Space' : {'parser': lambda s: int(s[:-6])}, #removes ' bytes'
        'Last Add Time' : {'parser': lambda ts: SELTimestamp(ts)},
        'Last Del Time' : {'parser': lambda ts: SELTimestamp(ts)},
        'Overflow' : {'parser': str2bool},
        'Supported Cmds' : {'parser': lambda s: re.findall("\w[ \w]+", s)}
    }


class SELAllocInfoCommand(Command, ResponseParserMixIn):
    """Describes the sel alloc info command"""

    name = "SEL Alloc Info"
    ipmitool_args = ["sel", "info"]
    result_type = SELAllocInfo

    response_fields = {
        '# of Alloc Units' : {'attr': 'num_alloc_units', 'parser': lambda s: int(s)},
        'Alloc Unit Size' : {'parser': lambda s: int(s)},
        '# Free Units' : {'attr': 'num_free_units', 'parser': lambda s: int(s)},
        'Largest Free Blk' : {'parser': lambda s: int(s)},
        'Max Record Size' : {'parser': lambda s: int(s)}
    }


class SELAddCommand(Command, ResponseParserMixIn):
    """Describes the sel add command"""

    #TODO: get response data from ipmitool

    name = "SEL Add"

    def __init__(self, *args, **kwargs):
        super(SELAddCommand, self).__init__(*args, **kwargs)
        self._tmpfile = tempfile.NamedTemporaryFile(delete=False)

        for e in self._params['records']:
            # TODO: handle other types of SEL Records
            # TODO: allow for malformed SEL entries
            entry = ('%s %s %s %s %s %s %s' %
                     (hex(e.evm_rev), hex(e.sensor_type), hex(e.sensor_number),
                      hex((e.event_direction << 7) | e.event_type),
                      hex(e.event_data[0]), hex(e.event_data[1]), hex(e.event_data[2])))
            self._tmpfile.write(str(entry) + '\n')
        self._tmpfile.flush()

    def __del__(self):
        os.remove(self._tmpfile.name)

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "add", self._tmpfile.name]

    def handle_command_error(self, resp, err):
        if err.find('Out of space') > 0:
            raise SELOverflowError(err)

        raise IpmiError(err)


class SELGetCommand(Command, ResponseParserMixIn):
    """Describes the sel get command"""

    def event_data_parser(string):
        data = int(string, 16)
        return (data >> 16, (data >> 8) & 0xff, data & 0xff)

    def response_parser(self, response, err):
        if err.find("command failed") > 0:
            return None

        entry = self.parse_colon_record(response, err)
        entry.normalize()
        return entry


    direction_parser = lambda d: 0 if d == 'Assertion Event' else 1
    hex_parser = lambda x: int(x, 16)

    name = "SEL Get"
    result_type = SELRecord

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "get"] + list(self._params['record_ids'])

    # TODO: add support for oem records
    response_fields = {
        'SEL Record ID': {'parser': hex_parser, 'attr': 'record_id'},
        'Record Type' : {'parser': hex_parser},
        'Timestamp': {},
        'Generator ID': {'parser': hex_parser},
        'EvM Revision': {'parser': hex_parser},
        'Sensor Type': {}, #TODO: covert to hex code
        'Sensor Number': {'parser': hex_parser},
        'Event Type': {}, #TODO: convert to hex code
        'Event Direction': {'parser': direction_parser},
        'Event Data': {'parser': event_data_parser},
        'Description': {}
    }


class SELClearCommand(Command, ResponseParserMixIn):
    """Describes the Clear SEL command"""

    name = "Clear SEL"
    ipmitool_args = ["sel", "clear"]
    # TODO: get response data from ipmitool


class SELListCommand(Command, ResponseParserMixIn):
    """Describes SEL List command
       note: this command is non-standard
    """

    def response_parser(self, resp, err):
        sel_list = resp.strip().split('\n')
        sel_list = map(string.strip, sel_list)
        return filter(lambda s: s != '', sel_list) # remove blank entries

    name = "List SEL"
    ipmitool_args = ["sel", "list"]
    result_type = list


class SELElistCommand(Command, ResponseParserMixIn):
    """ Describes the SEL Elist command """
    name = "SEL elist"
    ipmitool_args = ["sel", "elist"]
    result_type = list

    def response_parser(self, resp, err):
        entries = [x.strip() for x in resp.splitlines()]
        entries = [x for x in entries if x != '']
        return entries


sel_commands = {
    "set_sel_time" : SELTimeSetCommand,
    "get_sel_time" : SELTimeGetCommand,
    "sel_info" : SELInfoCommand,
    "sel_alloc_info" : SELAllocInfoCommand,
    "sel_add" : SELAddCommand,
    "sel_get" : SELGetCommand,
    "sel_clear" : SELClearCommand,
    "sel_list" : SELListCommand,
    "sel_elist" : SELElistCommand
}
