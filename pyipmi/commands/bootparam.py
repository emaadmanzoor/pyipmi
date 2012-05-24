#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.bootparam import *

class BootParamGetCommand(Command, ResponseParserMixIn):
    """ Get Boot Parameters using ipmitool chassis bootparam #  """
    
    name = "Get Boot Device"
    result_type = BootParamGetResult
    
    def parse_response(self, out, err):
        """ Output is a number of lines with some info
        """
        result = {}
        delimiter = [':','is','to']
        for line in out.strip().split('\n'):
            key, value = line, ""
            for x in delimiter:
                if x in line: 
                    info = line.split(x)
                    key, value = info[0], info[1]
                    break             
            key = key.strip(' -')
            value = value.strip(' -')
            result[key] = value             
        return result

    """ get #param from bootparam """
    @property
    def ipmitool_args(self):
        return ["chassis", "bootparam", "get",self._params['param']]

bootparam_commands = {
    "bootparam_get" : BootParamGetCommand
}
