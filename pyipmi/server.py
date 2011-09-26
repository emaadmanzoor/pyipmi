#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from chassis import Chassis

__all__ = ['Server']

class Server:
    """A server is managed over IPMI"""

    def __init__(self, bmc):
        self.bmc = bmc
        self._chassis = Chassis(self.bmc.handle)

    def power_off(self):
        if self._chassis.is_powered:
            self._chassis.power_off()

    def power_on(self):
        if not self._chassis.is_powered:
            self._chassis.power_on()

    def power_cycle(self):
        self._chassis.power_cycle()

    def hard_reset(self):
        self._chassis.hard_reset()

    @property
    def is_powered(self):
        return self._chassis.is_powered
