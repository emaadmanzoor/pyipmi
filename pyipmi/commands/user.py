#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
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
        result = []
        for line in out.strip().split('\n')[1:]:
            user_info = self.result_type()

            user_info_list = line.strip().split()
            print str(user_info_list)
            user_info.user_id = user_info_list[0].strip()
            user_info.name = user_info_list[1].strip()
            user_info.callin = user_info_list[2].strip()
            user_info.link_auth = user_info_list[3].strip()
            user_info.ipmi_msg = user_info_list[4].strip()
            user_info.channel_priv_limit = ' '.join(user_info_list[5:]).strip()

            result.append(user_info)

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
