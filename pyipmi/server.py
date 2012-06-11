#Copyright 2011-2012 Calxeda, Inc.  All Rights Reserved.

"""A representation of a server.

This may go away - it doesn't do anything other than what chassis does.

Don't add to this.
"""

from chassis import Chassis

__all__ = ['Server']

class Server:
    """A server is managed over IPMI"""

    def __init__(self, bmc):
        """
        Arguments:

        bmc -- the BMC that's managing this server
        """
        self.bmc = bmc
        self._chassis = Chassis(self.bmc.handle)

    def power_off(self):
        """Power off server if it's powered on"""
        if self._chassis.is_powered:
            self._chassis.power_off()

    def power_on(self):
        """Power on server if it's powered off"""
        if not self._chassis.is_powered:
            self._chassis.power_on()

    def power_cycle(self):
        """Power cycle server"""
        self._chassis.power_cycle()

    def hard_reset(self):
        """Warm reset server"""
        self._chassis.hard_reset()

    @property
    def is_powered(self):
        """True if server is powered, otherwise false"""
        return self._chassis.is_powered
