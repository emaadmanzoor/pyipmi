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
        self._add_command_stubs(command_list)

    def _add_command_stubs(self, command_list):
        for command in command_list:
            self._add_command_stub(command)

    def _add_command_stub(self, command):
        def _cmd(*args, **kwargs):
            tm = getattr(self._tool, command)
            return tm(*args, **kwargs)

        setattr(self, command, _cmd)

class Tool:
    """A tool implements communications with a BMC"""
    def __init__(self, handle, command_list):
        self._handle = handle
        self._add_command_stubs(command_list)
        self._command_list = command_list

    def _add_command_stubs(self, command_list):
        for command in command_list:
            self._add_command_stub(command)

    def _add_command_stub(self, command):
        def _cmd(*args, **kwargs):
            inst = self._command_list[command](self, *args, **kwargs)
            return self.run(inst)

        setattr(self, command, _cmd)

class Command:
    """A Command describes a specific IPMI command"""
    def __init__(self, tool, **params):
        self._tool = tool
        self._params = params
