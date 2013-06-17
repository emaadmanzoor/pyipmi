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


"""An implementation of Tool for ipmitool support"""

import os, subprocess, sys
if sys.platform != 'win32':
    import pexpect
from pyipmi import Tool, InteractiveCommand

class IpmiTool(Tool):
    """Implements interaction with impitool

    Currently only supports one off commands, persistent sessions will come.
    """

    def run(self, command):
        """Run a command via ipmitool"""
        ipmi_args = self._ipmi_args(command)

        arg_str = 'Running %s' % ' '.join(ipmi_args)
        self._log(arg_str)

        if isinstance(command, InteractiveCommand):
            command = ipmi_args[0]
            args = ipmi_args[1:]
            proc = self._start_command(command, args)
            return proc

        out, err = self._execute(command, ipmi_args)
        return command.parse_results(out, err)

    def _ipmi_args(self, command):
        """Return the command line arguments to ipmitool for command"""
        if 'IPMITOOL_PATH' in os.environ:
            args = [os.environ['IPMITOOL_PATH']]
        else:
            args = ['ipmitool']
        args.extend(self._config_args)
        args.extend(command.ipmitool_args)
        return map(str, args)

    @property
    def _config_args(self):
        """Return the config dependent command line arguments

        This arguments are generated from the BMC's config, not from
        a specific command. They will be the same from command to
        command.
        """
        params_to_args = {
            'hostname' : '-H',
            'password' : '-P',
            'username' : '-U',
            'authtype' : '-A',
            'level' : '-L',
            'port' : '-p',
            'interface' : '-I'
        }

        base = []
        bmc_params = self._handle.bmc.params

        for param, val in bmc_params.iteritems():
            arg = params_to_args.get(param)
            if arg and val:
                base.extend([arg, str(val)])

        return base

    def _execute(self, command, args):
        """Execute an ipmitool command"""
        proc = subprocess.Popen(args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        self._log(out)
        self._log(err)
        if proc.returncode != 0:
            command.handle_command_error(out, err)
        return out, err

    def _start_command(self, command, args, timeout=5):
        return pexpect.spawn(command, args, timeout=timeout,
                             logfile=self._handle._log_file)
