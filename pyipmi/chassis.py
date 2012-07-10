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


"""Generic stuff about IPMI chassis

A chassis in IPMI isn't necessarily the same as a physical chassis. Logically,
it's closer to a server. For example, the chassis's power status refers to
whether or not the server's application processor has power supplied to it
so it can run, and the hard reset command resets the application processor,
not the entire chassis.
"""

import time

class ChassisStatus:
    """The response to a ChassisStatus command

    TODO: This is currently an odd mix of types.. there must be a better way
    """

    def __init__(self):
        self.power_restore_policy = None
        self.power_control_fault = None
        self.power_fault = None
        self.power_interlock = None
        self.power_overload = None
        self.power_on = None 
        self.last_power_event = None
        self.misc_chassis_state = None

class Chassis:
    """Represents a single chassis.

    This gives convenience methods for issuing chassis related commands.
    """

    def wait_after(func):
        """Decorator for delaying after a command is issue
        
        A lot of the chassis related commands need a while to take effect - the
        @wait_after decorator is provided here as a way to provide a common way
        to delay after executing a chassis command.

        The chassis's wait attribute defines how long the delay after issuing
        a command is."""

        def sleeper(self):
            """sleeps after calling func"""
            ret = func(self)
            time.sleep(self.wait)
            return ret

        return sleeper

    def __init__(self, handle):
        """
        Arguments:
        handle -- a Handle object to use to talk to a chassis
        """
        self._handle = handle
        self.wait = 10
       
    def status(self):
        """Get the chassis's status"""
        return self._handle.chassis_status()

    @wait_after
    def power_off(self):
        """Turn the chassis off"""
        self._handle.chassis_control(mode="off")

    @wait_after
    def power_on(self):
        """Turn the chassis on"""
        self._handle.chassis_control(mode="on")

    @wait_after
    def power_cycle(self):
        """Power cycle the chassis"""
        self._handle.chassis_control(mode="cycle")

    @wait_after
    def hard_reset(self):
        """Reset the chassis"""
        self._handle.chassis_control(mode="reset")

    @property
    def is_powered(self):
        """True if the chassis is powered"""
        return self._handle.chassis_status().power_on
