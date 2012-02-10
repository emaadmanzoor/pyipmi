#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
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
        return ["fru", "ekanalyzer", 'frushow',
                'oc=%s' % self._params['filename']]


fru_commands = {
    'fru_print'                 : FRUPrintCommand,
    'fru_read'                  : FRUReadCommand,
    'fru_write'                 : FRUWriteCommand,
    'fru_upg_e_key'             : FRUUpgEKeyCommand
}
