#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
"""IPMI commands that are implemented

These don't always map directly to IPMI requests, although sometimes
they do. Sometimes, they map to higher level commands provided by
ipmitool. It's more convenient (and closer to real world use) to use
these higher level commands than to break stuff down.
"""
from chassis import chassis_commands
from bmc import bmc_commands
from sdr import sdr_commands
from fw import fw_commands
from sel import sel_commands
from sol import sol_commands
from payload import payload_commands
from dcmi import dcmi_commands
from pef import pef_commands
from freeipmi_pef import freeipmi_pef_commands
from pet import pet_commands

ipmi_commands = {}

ipmi_commands.update(bmc_commands)
ipmi_commands.update(chassis_commands)
ipmi_commands.update(sdr_commands)
ipmi_commands.update(fw_commands)
ipmi_commands.update(sel_commands)
ipmi_commands.update(sol_commands)
ipmi_commands.update(payload_commands)
ipmi_commands.update(dcmi_commands)
ipmi_commands.update(pef_commands)
ipmi_commands.update(freeipmi_pef_commands)
ipmi_commands.update(pet_commands)
