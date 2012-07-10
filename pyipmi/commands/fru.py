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


"""FRU related commands"""

from .. import Command
from pyipmi.fru import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class FRUPrintCommand(Command, ResponseParserMixIn):
    """Describes the FRU get inventory area info IPMI command

    This is "fru print" to ipmitool
    """
    name = "FRU Print"
    result_type = FRUPrintResult

    response_fields = {
        'FRU Device Description' : {},
        'Board Mfg Date' : {},
        'Board Mfg' : {},
        'Board Product' : {},
        'Board Serial' : {},
        'Board Part Number' : {},
        'Product Manufacturer' : {},
        'Product Name' : {},
        'Product Part Number' : {},
        'Product Serial' : {}
    }

    ipmitool_args = ["fru", "print"]


class FRUReadCommand(Command, ResponseParserMixIn):
    """Describes the FRU read IPMI command

    This is "fru read" to ipmitool
    """
    name = "FRU Read"
    result_type = FRUReadResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["fru", "read", self._params['fru_id'],
                self._params['filename']]


class FRUWriteCommand(Command, ResponseParserMixIn):
    """Describes the FRU write IPMI command

    This is "fru write" to ipmitool
    """
    name = "FRU Write"
    result_type = FRUWriteResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["fru", "read", self._params['fru_id'],
                self._params['filename']]


class FRUUpgEKeyCommand(Command, ResponseParserMixIn):
    """Describes the FRU upgEKey ipmitool command
    """
    name = "FRU UpgEkey"
    result_type = FRUUpgEKeyResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["fru", "upgEkey", self._params['fru_id'],
                self._params['filename']]


class FRUShowCommand(Command, ResponseParserMixIn):
    """Describes the ekanalyzer frushow ipmitool command
    """
    name = "FRU Show"
    result_type = FRUShowResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["ekanalyzer", 'frushow',
                'oc=%s' % self._params['filename']]


fru_commands = {
    'fru_print'                 : FRUPrintCommand,
    'fru_read'                  : FRUReadCommand,
    'fru_write'                 : FRUWriteCommand,
    'fru_upg_e_key'             : FRUUpgEKeyCommand
}
