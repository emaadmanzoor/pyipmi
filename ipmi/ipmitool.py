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
        base.extend(self._config_args)
        base.extend(command.ipmitool_args)
        return base

    @property
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

SIMPLE_VAL = 1
BOOL_VAL = 2

def ipmitool_command(command_class):
    def str2bool(v):
      return v.lower() == "true"

    def field_to_attr(field_name):
        return field_name.lower().replace(' ', '_')

    def field_to_objval(obj, field_info, field_name, value):
        attr_name = field_info.get('attr', field_to_attr(field_name))
        attr_conv = field_info.get('conv', SIMPLE_VAL)

        if attr_conv == SIMPLE_VAL:
            setattr(obj, attr_name, value)
        elif attr_conv == BOOL_VAL:
            setattr(obj, attr_name, str2bool(value))
        else:
            setattr(obj, attr_name, attr_conv(value))

    def parse_response(obj, response, mapping):
        lines = response.split("\n")
        left_over = []
        for line in lines:
            if line.find(':') == -1:
                continue

            field, value = [field.strip() for field in line.split(":")]

            field_info = mapping.get(field)

            if field_info == None:
                left_over.append((field, value))
                continue

            field_to_objval(obj, field_info, field, value)

    def ipmitool_parse_results(self, response):
        try:
            result = self.result_type()
        except AttributeError:
            return None

        parse_response(result, response, self.ipmitool_response_fields)
        return result

    command_class.ipmitool_parse_results = ipmitool_parse_results

    return command_class
