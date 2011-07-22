__all__ = ["Handle", "Tool", "Command"]

class Handle:
    """A handle to speak with a BMC

    Handles use a Tool to speak with a BMC.

    Handles may or may not use a single ipmi session for their duration,
    depending on their implementation.
    """

    def __init__(self, bmc, tool_class, command_list):
        self.bmc = bmc
        self._tool = tool_class(self, command_list)

    """TODO: find a better home for command stubs"""
    def chassis_status(self):
        return self._tool.chassis_status()

    def chassis_control(self, mode):
        return self._tool.chassis_control(mode)

    def get_device_id(self):
        return self._tool.get_device_id()

class Tool:
    """A tool implements communications with a BMC"""
    def __init__(self, handle, command_list):
        self._handle = handle
        self._command_list = command_list

    """TODO: find a better home for command stubs."""
    def chassis_status(self):
        command = self._command_list["chassis_status"](self)
        return self.run(command)

    def chassis_control(self, mode):
        command = self._command_list["chassis_control"](self, mode=mode)
        return self.run(command)

    def get_device_id(self):
        command = self._command_list["get_device_id"](self)
        return self.run(command)

class Command:
    """A Command describes a specific IPMI command"""
    def __init__(self, tool, **params):
        self._tool = tool
        self._params = params
