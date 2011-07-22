#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

from base import *
from ipmitool import IpmiTool
from commands import ipmi_commands
from chassis import Chassis

def make_bmc(bmc_class, **kwargs):
    bmc_kwargs = {
        "tool_class" : IpmiTool,
        "handle_class" : Handle,
        "command_list" : ipmi_commands
    }

    bmc_kwargs.update(kwargs)
    return bmc_class(**bmc_kwargs)
