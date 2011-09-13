from base import *
from commands import ipmi_commands
from tools import IpmiTool

__all__ = ['Handle', 'Tool', 'Command', 'make_bmc']


def make_bmc(bmc_class, logfile = None, **kwargs):
    bmc_kwargs = {
        "tool_class" : IpmiTool,
        "handle_class" : Handle,
        "command_list" : ipmi_commands
    }

    bmc_kwargs.update(kwargs)
    bmc_obj = bmc_class(**bmc_kwargs)
    bmc_obj.handle.set_log(logfile)

    return bmc_obj
