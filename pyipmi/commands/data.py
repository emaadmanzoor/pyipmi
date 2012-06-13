#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.data import *

class DataMemReadCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem data mem read command
    """

    name = "Read value from memory"
    result_type = DataMemReadResult

    response_fields = {
        'Length' : {},
        'Addr' : {},
        'Value' : {}
    }

    @property
    def ipmitool_args(self):
        args = ["cxoem", "data", "mem", "read",
                self._params['length'], self._params['addr']]
        if self._params['fmt']:
            args.append(self._params['fmt'])
        return args


class DataMemWriteCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem data mem write command
    """

    name = "Write value to memory"
    result_type = DataMemWriteResult

    response_fields = {
        'Length' : {},
        'Addr' : {},
        'Value' : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "data", "mem", "write", self._params['length'],
                self._params['addr'], self._params['value']]


class DataCDBReadCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem data cdb read command
    """

    name = "Read value from CDB"
    result_type = DataCDBReadResult

    response_fields = {
        'Length' : {},
        'Cid' : {},
        'Data size' : {},
        'CID size' : {},
        'Value' : {}
    }

    @property
    def ipmitool_args(self):
        args = ["cxoem", "data", "cdb", "read",
                self._params['length'], self._params['cid']]
        if self._params['fmt']:
            args.append(self._params['fmt'])
        return args


class DataCDBWriteCommand(Command, ResponseParserMixIn):
    """ Describes the cxoem data cdb write command
    """

    name = "Write value to CDB"
    result_type = DataCDBWriteResult

    response_fields = {
        'Length' : {},
        'Cid' : {},
        'Value' : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "data", "cdb", "write", self._params['length'],
                self._params['cid'], self._params['value']]


data_commands = {
    "data_memread"  : DataMemReadCommand,
    "data_memwrite" : DataMemWriteCommand,
    "data_cdbread"  : DataCDBReadCommand,
    "data_cdbwrite" : DataCDBWriteCommand
}
