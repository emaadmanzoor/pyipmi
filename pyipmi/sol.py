#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

"""Helper objects for various SOL-related commands"""

import pexpect
from pyipmi import IpmiError

ESCAPE_SEQUENCES = {
    "IpmiTool" : {
        "terminate" : "~.",
        "list_escapes" : "~?",
        "escape_char" : "~~"
    }
}

TOOL_RESPONSES = {
    "IpmiTool" : {
        "open" : "[SOL Session operational.  Use ~? for help]",
        "close" : "[terminated ipmitool]"
    }
}

class SOLConsole(object):
    """Create and control an SOL session"""

    def __init__(self, bmc, hostname, username, password):
        self._bmc = bmc
        self._toolname = bmc.handle._tool.__class__.__name__
        self.escapes = ESCAPE_SEQUENCES[self._toolname]
        self.responses = TOOL_RESPONSES[self._toolname]

        # activate SOL session
        self._proc = self._bmc.activate_payload()
        self.expect_exact(self.responses['open'])

        try:
            self._login(hostname, username, password)
        except IpmiError:
            self.close()
            raise

        self.isopen = True

    def __del__(self):
        if self.isopen:
            self.close()

    def close(self):
        self._logout()
        self.sendline(self.escapes['terminate'])
        try:
            self.expect_exact(self.responses['close'])
        except pexpect.TIMEOUT, pexpect.EOF:
            self._bmc.deactivate_payload()

        if self.isalive():
            self._proc.close()

        self.isopen = False

    def _login(self, hostname, username, password):
        self.prompt = '%s@%s:~[$#] ' % (username, hostname)

        # once we've activated a session, either we're logged in,
        # we need to log in, or we're not getting any data back
        self.sendline()
        index = self.expect(['%s login: ' % hostname,
                                         self.prompt, pexpect.TIMEOUT,
                                         pexpect.EOF])

        if index == 1: # we're already logged in
            return

        if index > 1: # check if we're hosed
            #TODO: check if we're hosed
            raise IpmiError('SOL session unresponsive')

        # otherwise: send username/password
        try:
            self.sendline(username)
            self.expect_exact('Password: ')
            self.sendline(password)
            self.expect(self.prompt)
        except pexpect.TIMEOUT:
            raise IpmiError('%s@%s: failed login' % (username, hostname))

        # make the prompt more predictable
        self.sendline('export PS1="\u@\h:~\$ "')
        self.expect(self.prompt)

    def _logout(self):
        self.sendline()
        self._proc.sendline('logout')

    ######################################
    #                                    #
    # Wrappers for pexpect functionality #
    #                                    #
    ######################################

    def expect(self, pattern, timeout=-1, searchwindowsize=None):
        return self._proc.expect(pattern, timeout, searchwindowsize)

    def expect_exact(self, pattern, timeout=-1, searchwindowsize=None):
        return self._proc.expect_exact(pattern, timeout, searchwindowsize)

    def isalive(self):
        return self._proc.isalive()

    def read(self, size=-1):
        # pexpect implements this function by expecting the delimiter
        # the default delimiter is EOF, which for our purposes, is
        # unlikely to be reached. So instead, use pexpect.TIMEOUT
        # as the delimiter for now
        prev_delimiter = self._proc.delimiter
        self._proc.delimiter = pexpect.TIMEOUT
        data = self._proc.read(size)
        self._proc.delimiter = prev_delimiter
        return data

    def readline(self, size=-1):
        return self._proc.readline(size)

    def send(self, s):
        return self._proc.send(s)

    def sendline(self, s=""):
        return self._proc.sendline(s)


class SOLConfigurationParameters(object):
    pass
