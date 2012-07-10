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
