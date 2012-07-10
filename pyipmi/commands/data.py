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
