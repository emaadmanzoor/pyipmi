#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

"""watchdog related commands"""

from .. import Command
from pyipmi.watchdog import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class WatchdogGetCommand(Command, ResponseParserMixIn):
    """Describes the watchdog get IPMI command

    This is "mc watchdog get" to ipmitool
    """
    name = "Watchdog Get"
    result_type = WatchdogGetResult

    response_fields = {
        'Watchdog Timer Use' : {},
        'Watchdog Timer Is' : {},
        'Watchdog Timer Actions' : {},
        'Pre-timeout interval' : {},
        'Timer Expiration Flags' : {},
        'Initial Countdown' : {},
        'Present Countdown' : {}
    }

    ipmitool_args = ["mc", "watchdog", "get"]


class WatchdogResetCommand(Command, ResponseParserMixIn):
    """Describes the watchdog rest IPMI command

    This is "mc watchdog reset" to ipmitool
    """
    name = "Watchdog Reset"
    result_type = WatchdogResetResult

    response_fields = {
    }

    ipmitool_args = ["mc", "watchdog", "reset"]


class WatchdogOffCommand(Command, ResponseParserMixIn):
    """Describes the watchdog off IPMI command

    This is "mc watchdog off" to ipmitool
    """
    name = "Watchdog Off"
    result_type = WatchdogOffResult

    response_fields = {
    }

    ipmitool_args = ["mc", "watchdog", "off"]


watchdog_commands = {
    'watchdog_get'            : WatchdogGetCommand,
    'watchdog_reset'          : WatchdogResetCommand,
    'watchdog_off'            : WatchdogOffCommand
}
