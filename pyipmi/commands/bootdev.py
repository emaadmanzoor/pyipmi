#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.bootdev import *
from pyipmi.commands.bootparam import *

class BootDevSetCommand(Command, ResponseParserMixIn):
    """ Set Boot Device using ipmitool chassis bootdev  """

    name = "Set Boot Device"
    result_type = BootDevSetResult
    
    response_fields = {
        'Boot Device' : {}
    }

    @property
    def ipmitool_args(self):
        if self._params['options'] != None:
            options = "options=" + str(self._params['options'])
            return ["chassis", "bootdev", self._params['device'],options]
        return ["chassis", "bootdev", self._params['device']]

class BootDevGetCommand(Command, ResponseParserMixIn):
    """ Get Boot Device using ipmitool chassis bootdev  """
    
    name = "Get Boot Device"
    result_type = BootDevGetResult
    """ parse the output into a nice harsh"""
    
    def parse_response(self, out, err):
        """ Use bootParam parse method to do the job of parsing output into a nice harsh  """
        boot_param = BootParamGetCommand(self._tool)
        all_info = boot_param.parse_response(out=out,err=err)
        bool2str = {True:'Yes',False:'No'}
        
        """ Only interested in Device and Persistent (Y/N)"""
        device = all_info['Boot Device Selector']
        persistent = (all_info['Options apply'] == 'all future boots')
        return {'device':device, 'persistent':bool2str[persistent]}
    
    """Get 5 from bootparam provides the status of bootdev"""    
    @property    
    def ipmitool_args(self):
        return ["chassis", "bootparam", "get", "5"]

bootdev_commands = {
    "bootdev_get" : BootDevGetCommand,
    "bootdev_set" : BootDevSetCommand
}
