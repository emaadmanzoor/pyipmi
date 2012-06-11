#Copyright 2011-2012 Calxeda, Inc.  All Rights Reserved. 

"""An implementation of Tool for ipmi-pef-config (module of FreeIPMI) support"""

import subprocess, sys, pexpect
from pyipmi import Tool, IpmiError, InteractiveCommand

class IpmiPEFConfig(Tool):
    """Implements interaction with ipmi-pef-config

    Currently only supports one off commands, persistent sessions will come.
    """
    def __init__(self, *args, **kwargs):
        super(IpmiPEFConfig, self).__init__(*args, **kwargs)
        self._ipmi_pef_config_path = self._find_ipmi_pef_config_path()

    def _find_ipmi_pef_config_path(self):
        """Get the path to the ipmi-pef-config bin.
        
        freeipmi puts all of its binaries in /usr/sbin, which lots of
        things don't have in their default path. We hardcode the path to
        it here, but only if it can't be found in $PATH (via bash's which)."""

        try:
            found = subprocess.check_output(['which', 'ipmi-pef-config']).strip()
        except subprocess.CalledProcessError:
            return '/usr/sbin/ipmi-pef-config'

        return found

    def run(self, command):
        """Run a command via ipmi-pef-config"""
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
        """Return the command line arguments to ipmi-pef-config for command"""
        args = [self._ipmi_pef_config_path]
        args.extend(self._config_args)
        args.extend(command.ipmi_pef_config_args)
        return map(str, args)

    @property
    def _config_args(self):
        """Return the config dependent command line arguments
        
        This arguments are generated from the BMC's config, not from
        a specific command. They will be the same from command to
        command.
        """
        params_to_args = {
            'hostname' : '-h',
            'password' : '-p',
            'username' : '-u',
            'authtype' : '-a',
            'level' : '-l'
        }

        base = []
        bmc_params = self._handle.bmc.params

        for param, val in bmc_params.iteritems():
            arg = params_to_args.get(param)
            if arg and val:
                base.extend([arg, str(val)])

        return base

    def _execute(self, command, args):
        """Execute an ipmi-pef-config command"""
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
