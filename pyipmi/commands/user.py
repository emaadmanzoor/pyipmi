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


"""user management IPMI commands"""

from .. import Command
from pyipmi.user import *
from pyipmi.tools.responseparser import (ResponseParserMixIn,
                                         str_to_list,
                                         str_to_dict)


class UserListCommand(Command, ResponseParserMixIn):
    """Describes the user list ipmitool command
    """
    name = "User List"
    result_type = UserListResults

    def parse_response(self, out, err):
        """ Output is a table with a header row:
        ID  Name         Callin  Link Auth    IPMI Msg   Channel Priv Limit
        1   anonymous    true    false        false      NO ACCESS
        """
        result = {}
        for line in out.strip().split('\n')[1:]:
            user_info = self.result_type()

            user_info_list = line.strip().split()
            if len(user_info_list) < 5:
                continue

            key = line[0:3].strip()
            user_info.name = line[4:20].strip()
            user_info.callin = line[22:28].strip()
            user_info.link_auth = line[29:39].strip()
            user_info.ipmi_msg = line[40:48].strip()
            user_info.channel_priv_limit = line[51:].strip()

            result[key] = user_info

        return result

    @property
    def ipmitool_args(self):
        channel = self._params.get('channel', '')
        return ["user", "list", channel]


class UserSetNameCommand(Command, ResponseParserMixIn):
    """Describes the user set name ipmitool command
    """
    name = "User Set Name"
    result_type = UserSetNameResults

    response_fields = {
        'Field Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["user", "set", "name", self._params['userid'],
                self._params['name']]


class UserSetPasswordCommand(Command, ResponseParserMixIn):
    """Describes the user set password ipmitool command
    """
    name = "User Set Password"
    result_type = UserSetPasswordResults

    response_fields = {
        'Field Name' : {}
    }

    @property
    def ipmitool_args(self):
        password = self._params.get('password', '')
        return ["user", "set", "password", self._params['userid'], password]


class UserDisableCommand(Command, ResponseParserMixIn):
    """Describes the user disable ipmitool command
    """
    name = "User Disable"
    result_type = UserDisableResults

    response_fields = {
        'Field Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["user", "disable", self._params['userid']]


class UserEnableCommand(Command, ResponseParserMixIn):
    """Describes the user enable ipmitool command
    """
    name = "User Enable"
    result_type = UserEnableResults

    response_fields = {
        'Field Name' : {}
    }

    @property
    def ipmitool_args(self):
        return ["user", "enable", self._params['userid']]


class UserPrivCommand(Command, ResponseParserMixIn):
    """Describes the user priv ipmitool command
    """
    name = "User Set Privileges"
    result_type = UserPrivResults

    response_fields = {
        'Field Name' : {}
    }

    @property
    def ipmitool_args(self):
        channel = self._params.get('channel', '')
        return ["user", "priv", self._params['userid'],
                self._params['priv_level'], channel]


user_commands = {
    'user_list'             : UserListCommand,
    'user_set_name'         : UserSetNameCommand,
    'user_set_password'     : UserSetPasswordCommand,
    'user_enable'           : UserEnableCommand,
    'user_disable'          : UserDisableCommand,
    'user_priv'             : UserPrivCommand
}
