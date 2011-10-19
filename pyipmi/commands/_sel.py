#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

"""This module contains a series of wrappers
   around SEL commands for ipmitool
"""

import re
import tempfile
from pyipmi import Command
from pyipmi.tools.ipmitool import IpmitoolCommandMixIn, str2bool
from pyipmi.sel import SELTimestamp, SELInfo, SELRecord


class SELTimeSetCommand(Command, IpmitoolCommandMixIn):
    """Describes the Set SEL Time command"""
    
    name = "Set SEL Time"
    # TODO: get response data from ipmitool

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "time", "set", self._params["time"]]


class SELTimeGetCommand(Command, IpmitoolCommandMixIn):
    """Describes the Get SEL Time command"""
 
    def _parse_sel_timestamp(self, resp, err):
        """A helper function to parse a timestamp returned from 
        an sel time [gs]et command
        """
        timestamp = SELTimestamp()
        self.field_to_objval(timestamp, {}, 'timestamp', resp.strip())
        return timestamp

    name = "Get SEL Time"
    result_type = SELTimestamp
    ipmitool_args = ["sel", "time", "get"]
    ipmitool_parse_response = _parse_sel_timestamp


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
        'Last Add Time' : {},
        'Last Del Time' : {},
        'Overflow' : {'parser': str2bool},
        'Supported Cmds' : {'parser': lambda s: re.findall("\w[ \w]+", s)},
        '# of Alloc Units' : {'attr': 'num_alloc_units', 'parser': int},
        'Alloc Unit Size' : {'parser': int},
        '# Free Units' : {'attr': 'num_free_units', 'parser': int},
        'Largest Free Blk' : {'parser': int},
        'Max Record Size' : {'parser': int}
    }


class SELAddEntryCommand(Command, IpmitoolCommandMixIn):
    """Describes the Get SEL Entry command"""
    
    name = "Add SEL Entry"
    #TODO: get response data from ipmitool

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        print hex(self._params['entry'].evm_rev)
        tmpfile = sel_entries_to_tmpfile(self._params['entry'])
        # TODO: clean up tmpfile
        return ["sel", "add", tmpfile.name]


class SELGetEntryCommand(Command, IpmitoolCommandMixIn):
    """Describes the Get SEL Entry command"""

    name = "Get SEL Entry"
    result_type = SELRecord

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sel", "get", self._params['entry']]


class SELClearCommand(Command, IpmitoolCommandMixIn):
    """Describes the Clear SEL command"""

    name = "Clear SEL"
    ipmitool_args = ["sel", "clear"]
    # TODO: get response data from ipmitool


sel_commands = {
    "set_sel_time" : SELTimeSetCommand,
    "get_sel_time" : SELTimeGetCommand,
    "sel_info" : SELInfoCommand,
    "add_sel_entries" : SELAddEntryCommand,
    "get_sel_entry" : SELGetEntryCommand,
    "sel_clear" : SELClearCommand
}

def sel_entries_to_tmpfile(*entries):
    """Write SELEntries to a file and call ipmitool"""
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    for e in entries:
        # TODO: handle other types of SEL Records
        # TODO: allow for malformed SEL entries
        entry = ('%s %s %s %s %s %s %s' % 
            (hex(e.evm_rev), hex(e.sensor_type), hex(e.sensor_num),
             hex(e.event_info), hex(e.event_data1), hex(e.event_data2),
             hex(e.event_data3)))
        tmpfile.write(str(entry) + '\n')
    tmpfile.flush()
    return tmpfile

