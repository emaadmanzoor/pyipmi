#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
"""An implementation of Tool for ipmitool support"""

import subprocess, sys
from .. import Tool
from pyipmi import IpmiError

class IpmiTool(Tool):
    """Implements interaction with impitool

    Currently only supports one off commands, persistent sessions will come.
    """

    def run(self, command):
        """Run a command via ipmitool"""
        ipmi_args = self._ipmi_args(command)
        out, err = self._execute(command, ipmi_args)
        return command.ipmitool_parse_results(out, err)

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

    def _execute(self, command, ipmi_args):
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
        if proc.returncode != 0:
            command.handle_command_error(out, err)
        return out, err

def str2bool(val):
    """True if val is 'true', 'yes' or 'enabled, otherwise false"""
    return val.lower() in ['true', 'yes', 'enabled']

def paren_pair(val):
    """Convert 'foo (bar)' to ['foo', 'bar']"""
    return [p.strip(' )') for p in val.split('(')]

def field_to_attr(field_name):
    """Convert a field name to an attribute name
    
    Make the field all lowercase and replace ' ' with '_'
    (replace space with underscore)
    """
    return field_name.lower().replace(' ', '_')

class IpmitoolCommandMixIn(object):
    """Add this MixIn to a Command to enable it to work with ipmitool"""

    COLUMN_RECORD = 1
    COLUMN_RECORD_LIST = 2

    ipmitool_response_format = COLUMN_RECORD

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
                 value will be assigned to the attribute unless a 'parser'
                 key/value is specified in the field_info dict

        Field Info:
        If an 'attr' key/value is present, the value will be used for the
        attribute name of this field instead of 'field_name'.

        If a 'parser' key/value is present, the value will be passed to
        it, and the result will be assigned to the attribute. The default
        parser is str().
        """
        attr_name = field_info.get('attr', field_to_attr(field_name))
        attr_parser = field_info.get('parser', str)

        setattr(obj, attr_name, attr_parser(value))

    def parse_colon_record(self, response, err):
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
            field = line[0:field_seperator - 1].strip()
            value = line[field_seperator + 1:].strip()

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

    def parse_colon_record_list(self, response, err):
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
            obj = self.parse_colon_record(record, err)

            if obj == None:
                continue

            results.append(obj)

        return results

    def parse_response(self, out, err):
        """Parse the response to a command

        The 'ipmitool_response_format' attribute is used to determine
        what parser to use to for interpreting the results.
        
        Arguments:
        out -- the text response of an ipmitool command from stdout
        err -- the text response of an ipmitool command from stderr
        """
        return self.ipmitool_parse_response(out, err)

    def ipmitool_parse_results(self, out, err):
        """Parse the results if a result type is specified
        
        If there is not 'result_type' attribute for this this command, return
        None.
        """
        try:
            result_type = self.result_type
        except AttributeError:
            return None

        return self.parse_response(out, err)

    def handle_command_error(self, out, err):
        """Handle an error from running the command"""
        raise IpmiError(err)

    ipmitool_parse_response = parse_colon_record
