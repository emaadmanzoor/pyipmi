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


from datetime import datetime
import re

from pyipmi import IpmiError

TIME_FORMAT = '%m/%d/%Y %H:%M:%S'

class SEL(object):
    """A class to represent a SEL"""

    def __init__(self, bmc):
        self.bmc = bmc
        self._info = self.bmc.sel_info()
        self._alloc_info = self.bmc.sel_alloc_info()

    @property
    def entries(self):
        return self.bmc.sel_info().entries

    @property
    def size(self):
        return self._alloc_info.num_alloc_units

    @property
    def size_bytes(self):
        return self.size * self._alloc_info.alloc_unit_size


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

    parser = re.compile('%s/%s/%s %s:%s:%s' % (
                        '(?P<mon>\d{2})', '(?P<day>\d{2})', '(?P<year>\d{4})',
                        '(?P<hour>\d{2})', '(?P<min>\d{2})', '(?P<sec>\d{2})'))
    default_time = parser.match('01/01/1970 00:00:00')

    def __init__(self, timestamp=''):
        match = self.parser.match(timestamp)
        if match is None:
            match = self.default_time

        mdict = dict((k, int(v)) for k, v in match.groupdict().iteritems())
        self.time = datetime(mdict['year'], mdict['mon'], mdict['day'],
                             mdict['hour'], mdict['min'], mdict['sec'])

    @property
    def timestamp(self):
        return repr(self)

    def __repr__(self):
        return self.time.strftime(TIME_FORMAT)

    def __str__(self):
        return str(self.time)

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return self.time != other.time

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time


class SELInfo(object):
    """A class to represent SEL info"""


class SELAllocInfo(object):
    """A class to represent SEL allocation info"""


class SELOverflowError(IpmiError):
    """An error that is thrown when the SEL is full"""


class SELTimestampError(IpmiError):
    """An error thrown with invalid timestamps"""
