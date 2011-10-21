#!/usr/bin/env python

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

class OEMSELRecord(object):
    """A class to represent an OEM SEL record type C0h-DFh"""


class TimestampedOEMSELRecord(OEMSELRecord):
    """A class to represent an OEM SEL record type E0h-FFh"""


class SELTimestamp(object):
    """A class to represent a Timestamp"""


class SELInfo(object):
    """A class to represent SELInfo"""
