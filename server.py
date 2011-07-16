#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

import time

from ipmi import Handle
from ipmitool import IpmiTool
from commands import ipmi_commands

class Server:
    """A server is managed over IPMI"""
    def wait_after(f):
        def sleeper(self):
            ret = f(self)
            time.sleep(self._wait)
            return ret
        return sleeper

    def __init__(self, bmc):
        self.bmc = bmc
        self._handle = bmc.handle(Handle, IpmiTool, ipmi_commands)
        self._wait = 10

    @wait_after
    def power_off(self):
        self._handle.chassis_control(mode="off")

    @wait_after
    def power_on(self):
        self._handle.chassis_control(mode="on")

    @wait_after
    def power_cycle(self):
        self._handle.chassis_control(mode="cycle")

    @wait_after
    def hard_reset(self):
        self._handle.chassis_control(mode="reset")

    @property
    def is_powered(self):
        return self._handle.chassis_status().power_on
