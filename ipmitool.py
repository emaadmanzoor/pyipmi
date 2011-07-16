#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

from ipmi import Tool
import subprocess

class IpmiTool(Tool):
    """Implements interaction with impitool

    Currently only supports one off commands, persistent sessions will come..
    """

    def run(self, command):
        ipmi_args = self._ipmi_args(command)
        results = self._execute(ipmi_args)
        return command.ipmitool_parse_results(results)

    def _ipmi_args(self, command):
        base = []
        base.extend(self._config_args())
        base.extend(command.ipmitool_args())
        return base

    def _config_args(self):
        params_to_args = {
            'hostname' : '-H',
            'password' : '-P',
            'port' : '-p'
        }

        base = []
        bmc_params = self._handle.bmc.params
        
        for param,val in bmc_params.iteritems():
            arg = params_to_args.get(param)
            if arg:
                base.extend([arg, str(val)])

        return base

    def _execute(self, ipmi_args):
        args = ["ipmitool"]
        args.extend(ipmi_args)
        print "Running: " + " ".join(args)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        return out
