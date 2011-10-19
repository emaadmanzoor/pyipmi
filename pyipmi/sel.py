#!/usr/bin/env python

class SELRecord(object):
    """A class to represent a SEL event record"""

    def __init__(self, record_id=0, record_type=2, timestamp='',
                 generator_id=0, evm_rev=4, sensor_type=0,
                 sensor_num=0, event_info=0, event_data1=0,
                 event_data2=0, event_data3=0):
        self.record_id = record_id
        self.record_type = record_type
        self.timestamp = timestamp
        self.generator_id = generator_id
        self.evm_rev = evm_rev
        self.sensor_type = sensor_type
        self.sensor_num = sensor_num
        self.event_info = event_info
        self.event_data1 = event_data1
        self.event_data2 = event_data2
        self.event_data3 = event_data3

class OEMSELRecord(object):
    """A class to represent an OEM SEL record type C0h-DFh"""


class TimestampedOEMSELRecord(OEMSELRecord):
    """A class to represent an OEM SEL record type E0h-FFh"""


class SELTimestamp(object):
    """A class to represent a Timestamp"""


class SELInfo(object):
    """A class to represent SELInfo"""
