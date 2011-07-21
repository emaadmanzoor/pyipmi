#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from ipmi import Handle
from ipmitool import IpmiTool
from commands import ipmi_commands
from chassis import Chassis

class Server:
    """A server is managed over IPMI"""

    def __init__(self, bmc):
        self.bmc = bmc
        self._handle = bmc.handle(Handle, IpmiTool, ipmi_commands)
        self._chassis = Chassis(self._handle)

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
