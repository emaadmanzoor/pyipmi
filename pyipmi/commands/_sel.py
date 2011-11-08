#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

"""This module contains a series of wrappers
   around SEL commands for ipmitool
"""

import re
import tempfile
import string
from pyipmi import Command
from pyipmi.tools.ipmitool import IpmitoolCommandMixIn, str2bool
from pyipmi.sel import (SELTimestamp, SELInfo, SELRecord,
                        SELOverflowError, SELTimestampError)


class SELTimeSetCommand(Command, IpmitoolCommandMixIn):
    """Describes the Set SEL Time command"""
    
    name = "Set SEL Time"
    # TODO: get response data from ipmitool

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "time", "set", self._params["time"].timestamp]

    def handle_command_error(self, resp, err):
        raise SELTimestampError(err)


class SELTimeGetCommand(Command, IpmitoolCommandMixIn):
    """Describes the Get SEL Time command"""
 
    def ipmitool_parse_response(self, resp, err):
        """A helper function to parse a timestamp returned from 
        an 'sel time get' command
        """

        return SELTimestamp(resp.strip())

    name = "Get SEL Time"
    result_type = SELTimestamp
    ipmitool_args = ["sel", "time", "get"]


class SELInfoCommand(Command, IpmitoolCommandMixIn):
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

    ipmitool_response_fields = {
        'Version' : {'parser': version_parser},
        'Entries' : {'parser': int},
        'Free Space' : {},
        'Percent Used' : {},
        'Last Add Time' : {'parser': lambda ts: SELTimestamp(ts)},
        'Last Del Time' : {'parser': lambda ts: SELTimestamp(ts)},
        'Overflow' : {'parser': str2bool},
        'Supported Cmds' : {'parser': lambda s: re.findall("\w[ \w]+", s)},
        '# of Alloc Units' : {'attr': 'num_alloc_units', 'parser': int},
        'Alloc Unit Size' : {'parser': int},
        '# Free Units' : {'attr': 'num_free_units', 'parser': int},
        'Largest Free Blk' : {'parser': int},
        'Max Record Size' : {'parser': int}
    }


class SELAddCommand(Command, IpmitoolCommandMixIn):
    """Describes the sel add command"""
    
    name = "SEL Add"
    #TODO: get response data from ipmitool

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        tmpfile = sel_entries_to_tmpfile(*self._params['records'])
        # TODO: clean up tmpfile
        return ["sel", "add", tmpfile.name]

    def handle_command_error(self, resp, err):
        if err.find('Out of space') > 0:
            raise SELOverflowError(err)

        raise IpmiError(err)


class SELGetCommand(Command, IpmitoolCommandMixIn):
    """Describes the sel get command"""

    def event_data_parser(string):
        data = int(string, 16)
        return (data >> 16, (data >> 8) & 0xff, data & 0xff)

    def ipmitool_parse_response(self, response, err):
        if err.find("command failed") > 0:
            return None

        entry = self.parse_colon_record(response, err)
        entry.normalize()
        return entry


    direction_parser= lambda d: 0 if d == 'Assertion Event' else 1
    hex_parser = lambda x: int(x, 16)

    name = "SEL Get"
    result_type = SELRecord

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "get"] + list(self._params['record_ids'])

    # TODO: add support for oem records
    ipmitool_response_fields = {
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


class SELClearCommand(Command, IpmitoolCommandMixIn):
    """Describes the Clear SEL command"""

    name = "Clear SEL"
    ipmitool_args = ["sel", "clear"]
    # TODO: get response data from ipmitool


class SELListCommand(Command, IpmitoolCommandMixIn):
    """Describes SEL List command
       note: this command is non-standard
    """

    def ipmitool_parse_response(self, resp, err):
        sel_list = resp.strip().split('\n')
        sel_list =  map(string.strip, sel_list)
        return filter(lambda s: s != '', sel_list) # remove blank entries

    name = "List SEL"
    ipmitool_args = ["sel", "list"]
    result_type = list


sel_commands = {
    "set_sel_time" : SELTimeSetCommand,
    "get_sel_time" : SELTimeGetCommand,
    "sel_info" : SELInfoCommand,
    "sel_add" : SELAddCommand,
    "sel_get" : SELGetCommand,
    "sel_clear" : SELClearCommand,
    "sel_list" : SELListCommand
}

def sel_entries_to_tmpfile(*entries):
    """Write SELRecords to a file and call ipmitool"""
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    for e in entries:
        # TODO: handle other types of SEL Records
        # TODO: allow for malformed SEL entries
        entry = ('%s %s %s %s %s %s %s' % 
            (hex(e.evm_rev), hex(e.sensor_type), hex(e.sensor_number),
             hex((e.event_direction << 7) | e.event_type),
             hex(e.event_data[0]), hex(e.event_data[1]), hex(e.event_data[2])))
        tmpfile.write(str(entry) + '\n')
    tmpfile.flush()
    return tmpfile

