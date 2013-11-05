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
from event import event_commands
from watchdog import watchdog_commands
from fru import fru_commands
from lan import lan_commands
from channel import channel_commands
from user import user_commands
from fabric import fabric_commands
from fabric_config import fabric_config_commands
from bootdev import bootdev_commands
from bootparam import bootparam_commands
from mc import mc_commands
from data import data_commands
from info import info_commands
from pmic import pmic_commands

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
ipmi_commands.update(event_commands)
ipmi_commands.update(watchdog_commands)
ipmi_commands.update(fru_commands)
ipmi_commands.update(lan_commands)
ipmi_commands.update(channel_commands)
ipmi_commands.update(user_commands)
ipmi_commands.update(fabric_commands)
ipmi_commands.update(fabric_config_commands)
ipmi_commands.update(bootdev_commands)
ipmi_commands.update(bootparam_commands)
ipmi_commands.update(mc_commands)
ipmi_commands.update(data_commands)
ipmi_commands.update(info_commands)
ipmi_commands.update(pmic_commands)
