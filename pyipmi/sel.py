#!/usr/bin/env python

from time import strptime, mktime
from pyipmi import IpmiError

TIME_FORMAT = '%m/%d/%Y %H:%M:%S'

class SEL(object):
    """A class to represent a SEL"""

    def __init__(self, bmc):
        self.bmc = bmc
        self._info = self.bmc.sel_info()

    @property
    def entries(self):
        return self.bmc.sel_info().entries

    @property
    def size(self):
        return self._info.num_alloc_units


class SELRecord(object):
    """A class to represent a SEL event record"""

    def __init__(self, record_id=0, record_type=2, timestamp='',
                 generator_id=0, evm_rev=4, sensor_type=0,
                 sensor_number=0, event_type=0, event_direction=0,
                 event_data=(0, 0, 0)):
        self.record_id = record_id
        self.record_type = record_type
        self.timestamp = timestamp
        self.generator_id = generator_id
        self.evm_rev = evm_rev
        self.sensor_type = sensor_type
        self.sensor_number = sensor_number
        self.event_type = event_type
        self.event_direction = event_direction
        self.event_data = event_data

    def __eq__(self, other):
        return (self.record_type == other.record_type and
                self.generator_id == other.generator_id and
                self.evm_rev == other.evm_rev and
                self.sensor_type == other.sensor_type and
                self.sensor_number == other.sensor_number and
                self.event_type == other.event_type and
                self.event_direction == other.event_direction and
                self.event_data == other.event_data)

    sensor_types = {'Reserved': 0}
    event_types = {'Unspecified': 0}

    def normalize(self):
        #TODO: replace this with something better
        try:
            int(self.sensor_type)
        except ValueError:
            self.sensor_type = self.sensor_types[self.sensor_type]

        try:
            int(self.event_type)
        except ValueError:
            self.event_type = self.event_types[self.event_type]


class OEMSELRecord(object):
    """A class to represent an OEM SEL record type C0h-DFh"""


class TimestampedOEMSELRecord(OEMSELRecord):
    """A class to represent an OEM SEL record type E0h-FFh"""


class SELTimestamp(object):
    """A class to represent a Timestamp"""

    def __init__(self, timestamp=''):
        self.timestamp = timestamp

    def mktime(self):
        return mktime(strptime(self.timestamp, TIME_FORMAT))

    def __str__(self):
        return self.timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        return self.timestamp != other.timestamp

    def __lt__(self, other):
        return self.mktime() < other.mktime()

    def __le__(self, other):
        return self.mktime() <= other.mktime()

    def __gt__(self, other):
        return self.mktime() > other.mktime()

    def __ge__(self, other):
        return self.mktime() >= other.mktime()


class SELInfo(object):
    """A class to represent SELInfo"""


class SELOverflowError(IpmiError):
    """An error that is thrown when the SEL is full"""
