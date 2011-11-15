#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
"""IPMI commands that are implemented

These don't always map directly to IPMI requests, although sometimes
they do. Sometimes, they map to higher level commands provided by
ipmitool. It's more convenient (and closer to real world use) to use
these higher level commands than to break stuff down.
"""
from _chassis import chassis_commands
from _bmc import bmc_commands
from _sdr import sdr_commands
from _fw import fw_commands
from _sel import sel_commands

ipmi_commands = {}

ipmi_commands.update(bmc_commands)
ipmi_commands.update(chassis_commands)
ipmi_commands.update(sdr_commands)
ipmi_commands.update(fw_commands)
ipmi_commands.update(sel_commands)
