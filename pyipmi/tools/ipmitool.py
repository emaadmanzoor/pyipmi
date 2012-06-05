#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
"""An implementation of Tool for ipmitool support"""

import subprocess, sys, pexpect
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
        print arg_str

        if isinstance(command, InteractiveCommand):
            command = ipmi_args[0]
            args = ipmi_args[1:]
            proc = self._start_command(command, args)
            return proc

        out, err = self._execute(command, ipmi_args)
        return command.parse_results(out, err)

    def _ipmi_args(self, command):
        """Return the command line arguments to ipmitool for command"""
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
        sys.stdout.write(out)
        sys.stderr.write(err)
        if proc.returncode != 0:
            command.handle_command_error(out, err)
        return out, err

    def _start_command(self, command, args, timeout=5):
        return pexpect.spawn(command, args, timeout=timeout,
                             logfile=self._handle._log_file)
