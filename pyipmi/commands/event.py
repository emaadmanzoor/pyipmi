#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
"""event related commands -- for generating test events"""

from .. import Command
from pyipmi.event import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class GenerateGenericEvent(Command, ResponseParserMixIn):
    """Describes the generic event IPMI command

    This is "event <event_type>" to ipmitool
    """
    name = "Generate Generic Event"
    result_type = GenericEventResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["event", self._params['event_type']]


class AssertSensorEvent(Command, ResponseParserMixIn):
    """Describes the generic event IPMI command

    This is "event <sensorid> <state> assert" to ipmitool
    """
    name = "Assert Sensor Event"
    result_type = AssertSensorEventResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["event", self._params['sensor_id'],
                self._params['state'], 'assert']


event_commands = {
    'generic_event'            : GenerateGenericEvent,
    'assert_sensor_event'      : AssertSensorEvent
}
