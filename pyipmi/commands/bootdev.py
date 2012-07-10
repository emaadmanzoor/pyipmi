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
