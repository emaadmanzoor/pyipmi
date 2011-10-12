#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
"""An implementation of Tool for ipmitool support"""

import subprocess, sys
from .. import Tool

class IpmiTool(Tool):
    """Implements interaction with impitool

    Currently only supports one off commands, persistent sessions will come.
    """

    def run(self, command):
        """Run a command via ipmitool"""
        ipmi_args = self._ipmi_args(command)
        results = self._execute(ipmi_args)
        return command.ipmitool_parse_results(results)

    def _ipmi_args(self, command):
        """Return the command line arguments to ipmitool for command"""
        base = []
        base.extend(self._config_args)
        base.extend(command.ipmitool_args)
        return base

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
            'port' : '-p'
        }

        base = []
        bmc_params = self._handle.bmc.params
        
        for param, val in bmc_params.iteritems():
            arg = params_to_args.get(param)
            if arg and val:
                base.extend([arg, str(val)])

        return base

    def _execute(self, ipmi_args):
        """Execute an ipmitool command"""
        args = ['ipmitool']
        args.extend(ipmi_args)
        self._log('Running: ' + ' '.join(args))
        print 'Running: ' + ' '.join(args)
        proc = subprocess.Popen(args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
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
    def paren_pair(val):
        """Convert 'foo (bar)' to ['foo', 'bar']"""
        return [p.strip(' )') for p in val.split('(')]

    @staticmethod
    def str2bool(val):
        """True if val is 'true' or 'yes', otherwise false"""
        return val.lower() in ['true', 'yes']

    @staticmethod
    def field_to_attr(field_name):
        """Convert a field name to an attribute name
        
        Make the field all lowercase and replace ' ' with '_'
        (replace space with underscore)
        """
        return field_name.lower().replace(' ', '_')

    def field_to_objval(self, obj, field_info, field_name, value):
        """Assign a field's value to an attribute of obj
        
        Arguments:
        obj -- the object to set the attribute on. this is some record type
               object - the exact varies depending on the command being
               executed.
        field_info -- a dict describing the field. See "Field Info" below for
                      more info.
        field_name -- the name of the field as given in the ipmitool results.
                      this will be used as the name of the attribute unless a
                      'attr' key/value is given in the field_info dict.
        value -- the value of the field as given in the ipmitool results. This
                 value will be assigned to the attribute unless a 'conv'
                 key/value is specified in the field_info dict

        Field Info:
        If an 'attr' key/value is present, the value will be used for the
        attribute name of this field instead of 'field_name'. There is a
        special case when conv==PAREN_PAIR_VALUE, see below.

        If a 'conv' key/value is present, the value is either one of these:
            SIMPLE_VAL: the value is assigned directly.
            BOOL_VAL: the value is converted to True/False using the str2bool
                      method.
            PAREN_PAIR_VALUE: Value is 'like (this)' and attr must be a tuple
            containing two strings to be used as names for two attributes.
        Or, it can be a callable object, in which case value will be passed to
        it, and the result will be assigned to the attribute.
        """
        attr_name = field_info.get('attr', self.field_to_attr(field_name))
        attr_conv = field_info.get('conv', SIMPLE_VAL)

        if attr_conv == SIMPLE_VAL:
            setattr(obj, attr_name, value)
        elif attr_conv == BOOL_VAL:
            setattr(obj, attr_name, self.str2bool(value))
        elif attr_conv == PAREN_PAIR_VAL:
            attr_vals = self.paren_pair(value)

            for i, val in enumerate(attr_vals):
                setattr(obj, attr_name[i], val)
        else:
            setattr(obj, attr_name, attr_conv(value))

    def parse_colon_record(self, response):
        """Parse records of key : value separated lines

        This expects response to be a string of newline separated
        field/value pairs, with each field/value being separated by a
        colon and optional whitespace.
        
        Records this parses look like this:

        Sensor Data Type : Blah
        Somefield    :  Somevalue

        The type of the result returned and the conversion of key/values
        in the text result to attribute names/values in the returned object
        are determined by calling ipmitool_types on this command instance,
        which gives a way for the result type and mapping to change based
        on the contents of the response.
        """
        result_type, mapping = self.ipmitool_types(response)

        if result_type == None:
            return None

        obj = result_type()
        lines = response.split('\n')
        left_over = []
        for line in lines:
            if line.find(':') == -1:
                continue

            field_seperator = line.index(':')
            field = line[0:field_seperator-1].strip()
            value = line[field_seperator+1:].strip()

            field_info = mapping.get(field)

            if field_info == None:
                left_over.append((field, value))
                continue

            self.field_to_objval(obj, field_info, field, value)

        return obj

    def ipmitool_types(self, response):
        """Return the result type and field mappings

        The result type is the class of the result to be used. The field
        mappings are given in self.ipmitool_response_fields, and are a
        dict mapping field names to field info dicts. See 'field info' in
        the doc for field_to_objval above.

        Arguments:
        response -- the text of the ipmitool response. It's not used in
        this base method, but might be used in a subclass's version of
        this method to allow different result types and mappings to be
        used based on the contents of the response.
        """
        return self.result_type, self.ipmitool_response_fields

    def parse_colon_record_list(self, response):
        """Parse multiple groups of colon records
        
        Like colon records, but with multiple groups, each separted
        by a blank line (two consecutive newline characters).

        This returns a list of result objects rather than a single
        result object. The type of each result object can vary based
        on its contents, so the list isn't always of the same type
        of objects.
        """
        results = []
        records = response.split('\n\n')
        for record in records:
            obj = self.parse_colon_record(record)

            if obj == None:
                continue

            results.append(obj)

        return results

    def parse_response(self, response):
        """Parse the response to a command

        The 'ipmitool_response_format' attribute is used to determine
        what parser to use to for interpreting the results.

        The format is COLUMN_RECORD by default.
        
        Arguments:
        response -- the text response of an ipmitool command
        """
        if self.ipmitool_response_format == self.COLUMN_RECORD:
            return self.parse_colon_record(response)
        elif self.ipmitool_response_format == self.COLUMN_RECORD_LIST:
            return self.parse_colon_record_list(response)
        else:
            raise Exception('unknown ipmitool_response_format: %d\n' % (
                self.ipmitool_response_format))

    def ipmitool_parse_results(self, response):
        """Parse the results if a result type is specified
        
        If there is not 'result_type' attribute for this this command, return
        None.
        """
        try:
            result_type = self.result_type
        except AttributeError:
            return None

        return self.parse_response(response)
