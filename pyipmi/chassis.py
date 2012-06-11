#Copyright 2011-2012 Calxeda, Inc.  All Rights Reserved.

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
