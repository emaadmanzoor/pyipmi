#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

import subprocess, sys
from ipmi import Tool

class IpmiTool(Tool):
    """Implements interaction with impitool

    Currently only supports one off commands, persistent sessions will come.
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
            'username' : '-U',
            'authtype' : '-A',
            'level' : '-L',
            'port' : '-p'
        }

        base = []
        bmc_params = self._handle.bmc.params
        
        for param,val in bmc_params.iteritems():
            arg = params_to_args.get(param)
            if arg and val:
                base.extend([arg, str(val)])

        return base

    def _execute(self, ipmi_args):
        args = ['ipmitool']
        args.extend(ipmi_args)
        self._log('Running: ' + ' '.join(args))
        print 'Running: ' + ' '.join(args)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = proc.communicate()
        self._log(out)
        self._log(err)
        sys.stdout.write(out)
        sys.stderr.write(err)
        return out

SIMPLE_VAL      = 1
BOOL_VAL        = 2
PAREN_PAIR_VAL  = 3

class IpmitoolCommandMixIn(object):
    """Add this MixIn to a Command to enable it to work with ipmitool"""

    COLUMN_RECORD = 1
    COLUMN_RECORD_LIST = 2
    
    ipmitool_response_format = COLUMN_RECORD

    @staticmethod
    def paren_pair(v):
        return [p.strip(' )') for p in v.split('(')]

    @staticmethod
    def str2bool(v):
      return v.lower() in ["true", "yes"]

    @staticmethod
    def field_to_attr(field_name):
        return field_name.lower().replace(' ', '_')

    def field_to_objval(self, obj, field_info, field_name, value):
        attr_name = field_info.get('attr', self.field_to_attr(field_name))
        attr_conv = field_info.get('conv', SIMPLE_VAL)

        if attr_conv == SIMPLE_VAL:
            setattr(obj, attr_name, value)
        elif attr_conv == BOOL_VAL:
            setattr(obj, attr_name, self.str2bool(value))
        elif attr_conv == PAREN_PAIR_VAL:
            attr_vals = self.paren_pair(value)

            for i, v in enumerate(attr_vals):
                setattr(obj, attr_name[i], v)
        else:
            setattr(obj, attr_name, attr_conv(value))

    def parse_colon_record(self, response):
        result_type, mapping = self.ipmitool_types(response)

        if result_type == None:
            return None

        obj = result_type()
        lines = response.split("\n")
        left_over = []
        for line in lines:
            if line.find(':') == -1:
                continue

            field_seperator = line.index(":")
            field = line[0:field_seperator-1].strip()
            value = line[field_seperator+1:].strip()

            field_info = mapping.get(field)

            if field_info == None:
                left_over.append((field, value))
                continue

            self.field_to_objval(obj, field_info, field, value)

        return obj

    def ipmitool_types(self, response):
        return self.result_type, self.ipmitool_response_fields

    def parse_colon_record_list(self, response):
        results = []
        records = response.split('\n\n')
        for record in records:
            obj = self.parse_colon_record(record)

            if obj == None:
                continue

            results.append(obj)

        return results

    def parse_response(self, response):
        if self.ipmitool_response_format == self.COLUMN_RECORD:
            return self.parse_colon_record(response)
        elif self.ipmitool_response_format == self.COLUMN_RECORD_LIST:
            return self.parse_colon_record_list(response)
        else:
            raise Exception('unknown ipmitool_response_format: %d\n' % (
                ipmitool_response_format))

    def ipmitool_parse_results(self, response):
        try:
            result_type = self.result_type
        except AttributeError:
            return None

        return self.parse_response(response)
