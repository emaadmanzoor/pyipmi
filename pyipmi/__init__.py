"""pyipmi provides IPMI client functionality"""
from __future__ import print_function

__all__ = ['Handle', 'Tool', 'Command', 'make_bmc', 'IpmiError']

class Handle:
    """A handle to speak with a BMC

    Handles use a Tool to speak with a BMC. It's basically a session handle
    from its user's perspective, although handles may or may not use a single
    ipmi session for their duration, depending on their implementation.

    The Handle class itself is concrete, but may become abstract in the future.
    """

    def __init__(self, bmc, tool_class, command_list):
        """
        Arguments:
        bmc -- A BMC object
        tool_class -- the class of the tool to be used for this handle,
                      for example, IpmiTool.
        command_list -- a list of Commands to be made available to this handle.
        """
        self.bmc = bmc
        self._tool = tool_class(self, command_list)
        self._add_command_stubs(command_list)
        self._log_file = None

    def _add_command_stubs(self, command_list):
        """Adds command methods to an instance of Handle
        
        Each command in the command_list supplied to init will add a method to
        this handle instance. Calling that method causes the command to be issued.
        """
        for command in command_list:
            self._add_command_stub(command)

    def _add_command_stub(self, command):
        """Add a a method for a command"""
        def _cmd(*args, **kwargs):
            """Call the method of the same name on the tool"""
            tool_method = getattr(self._tool, command)
            return tool_method(*args, **kwargs)

        setattr(self, command, _cmd)

    def set_log(self, log_file):
        """Setup a logger for the handle
        
        Arguments:
        log_file -- a file like object
        """
        self._log_file = log_file

    def log(self, string):
        """Write a string to a log

        The log is flushed after log is written

        Arguments:
        string -- the string to log."""
        if (self._log_file):
            print(string, file = self._log_file)
            self._log_file.flush()

class Tool(object):
    """A tool implements communications with a BMC
   
    Tool is an abstract class - it needs a 'run' method defined to be useful.

    Tool implementations vary in the way they implement IPMI communications.
    The IpmiTool implementation uses high level ipmitool commands executed via
    subprocesses. A freeipmi implementation could do the same using freeipmi
    commands, or there could be a RawIpmiTool implementation that used IpmiTool
    with raw commands. Another possibility is implementing IPMI natively in
    python, and having a NativeIpmi Tool implementation for that.

    Tool instances are bound to handle instances - each tool has exactly one
    handle.

    Tool instances are created with a list of commands - each command in the
    list causes a method (named after the command) to be added to the tool
    for executing the command. Commands in the list must implement support
    for the tool - each tool has 

    Concrete implementations should go in the tools directory. An example
    concrete implementation is the ImpiTool class.
    """
    def __init__(self, handle, command_list):
        """
        Arguments:
        handle -- the handle to which this command is bound
        command_list -- the list of commands the tool can execute
        """
        self._handle = handle
        self._add_command_stubs(command_list)
        self._command_list = command_list

    def _add_command_stubs(self, command_list):
        """Add command methods to this Tool instance

        Just like handles, tools get a method per command in command_list
        """
        for command in command_list:
            self._add_command_stub(command)

    def _add_command_stub(self, command):
        """Add an individual command method"""
        def _cmd(*args, **kwargs):
            """An individual command method.
            
            Uses this tool's run method to execute a command in this
            tool's special way."""
            inst = self._command_list[command](self, *args, **kwargs)
            return self.run(inst)

        setattr(self, command, _cmd)

    def _log(self, string):
        """Log a message via this tool's handle"""
        self._handle.log(string)

    def run(self, command):
        """This should be defined in a subclass of Tool"""
        pass

class Command:
    """A Command describes a specific IPMI command"""
    def __init__(self, tool, **params):
        self._tool = tool
        self._params = params

class InteractiveCommand(Command):
    """A dummy class for an interactive command"""

def make_bmc(bmc_class, logfile = None, **kwargs):
    """Returns a bmc object with 'default' settings
    
    This uses IpmiTool for the tool,the base Handle class, and
    the default "ipmi_commands" list of IPMI commands.

    kwargs is combined with those default settings into a single
    dict with its contents passed as keyword args when calling
    bmc_class.

    Arguments:
    bmc_class -- called w/ kwargs as its parameter to get the
                 object to return.

    Keyword arguments:
    logfile -- an optional file object for logging (default none)
    """

    from commands import ipmi_commands
    from tools import IpmiTool
    bmc_kwargs = {
        'tool_class' : IpmiTool,
        'handle_class' : Handle,
        'command_list' : ipmi_commands
    }

    bmc_kwargs.update(kwargs)
    bmc_obj = bmc_class(**bmc_kwargs)
    bmc_obj.handle.set_log(logfile)

    return bmc_obj


class IpmiError(Exception):
    """A wrapper for an Ipmi error"""
