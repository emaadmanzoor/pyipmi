"""This module contains a series of wrappers
   around sensor commands for ipmitool
"""

from pyipmi import Command, IpmiError
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.sensor import SensorRecord

class SensorGetCommand(Command, ResponseParserMixIn):
    """Describes the sensor get command"""

    def response_parser(self, response, err):
        if err.find("not found") > 0:
            return None
        entry = self.parse_colon_record_list(response, err)
        return entry

    name = "Sensor Get"
    result_type = SensorRecord

    @property
    def ipmitool_args(self):
        """return args for ipmitool command"""
        return ["sensor", "get"] \
             + list(self._params['sensor_ids'])

    response_fields = {
        'Sensor ID': {},
        'Entity ID': {},
        'Sensor Type (Threshold)': {},
        'Sensor Type (Discrete)': {},
        'Sensor Reading': {},
        'Status': {},
        'Nominal Reading': {},
        'Normal Minimum': {},
        'Normal Maximum': {},
        'Upper critical': {},
        'Upper non-critical': {},
        'Lower critical': {},
        'Lower non-critical': {},
        'Positive Hysteresis': {},
        'Negative Hysteresis': {},
        'Minimum sensor range': {},
        'Maximum sensor range': {},
        'Event Message Control': {},
        'Readable Thresholds': {},
        'Settable Thresholds': {},
        'Threshold Read Mask': {},
        'Assertion Events': {},
        'Assertions Enabled': {},
        'Deassertions Enabled': {}
    }


class SensorListCommand(Command, ResponseParserMixIn):
    """Describes sensor list command
    """

    def response_parser(self, resp, err):
        sensor_list = [x.strip() for x in resp.splitlines()]
        sensor_list = [x for x in sensor_list if x != '']
        return sensor_list

    name = "List sensors"
    ipmitool_args = ["sensor", "list"]
    result_type = list

class SensorThreshCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool sensor thresh command
    """

    def response_parser(self, resp, err):
        return [resp]

    name = "Sensor Thresh"
    result_type = list

    @property
    def ipmitool_args(self):
        command = ["sensor", "thresh"] \
                + [self._params['sensor']] \
                + [self._params['threshold']] \
                + self._params['values']
        return command

sensor_commands = {
    "sensor_list" : SensorListCommand,
    "sensor_thresh" : SensorThreshCommand,
    "sensor_get" : SensorGetCommand
}
