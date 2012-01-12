#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
"""An implementation of Tool for ipmi-dcmi (module of FreeIPMI) support"""

import subprocess, sys, pexpect
from pyipmi import Tool, IpmiError, InteractiveCommand

class IpmiDcmi(Tool):
    """Implements interaction with ipmi-dcmi

    Currently only supports one off commands, persistent sessions will come.
    """
    def __init__(self, *args, **kwargs):
        super(IpmiDcmi, self).__init__(*args, **kwargs)
        self._ipmidcmi_path = self._find_ipmidcmi_path()

    def _find_ipmidcmi_path(self):
        """Get the path to the ipmi-dcmi bin.
        
        freeipmi puts all of its binaries in /usr/sbin, which lots of
        things don't have in their default path. We hardcode the path to
        it here, but only if it can't be found in $PATH (via bash's which)."""
        
        try:
            found = subprocess.check_output(['which', 'ipmi-dcmi']).strip()
        except subprocess.CalledProcessError:
            return '/usr/sbin/ipmi-dcmi'

        return found

    def run(self, command):
        """Run a command via ipmi-dcmi"""
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
        return command.ipmidcmi_parse_results(out, err)

    def _ipmi_args(self, command):
        """Return the command line arguments to ipmi-dcmi for command"""
        args = [self._ipmidcmi_path]
        args.extend(self._config_args)
        args.extend(command.ipmidcmi_args)
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
        """Execute an ipmi-dcmi command"""
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
    result = field_name.lower()
    result = result.replace(' ', '_')
    result = result.replace('/', '_')
    result = result.replace('-', '_')
    return result

class IpmiDcmiCommandMixIn(object):
    """Add this MixIn to a Command to enable it to work with ipmi-dcmi"""

    COLUMN_RECORD = 1
    COLUMN_RECORD_LIST = 2

    ipmidcmi_response_format = COLUMN_RECORD

    def field_to_objval(self, obj, field_info, field_name, value):
        """Assign a field's value to an attribute of obj
        
        Arguments:
        obj -- the object to set the attribute on. this is some record type
               object - the exact varies depending on the command being
               executed.
        field_info -- a dict describing the field. See "Field Info" below for
                      more info.
        field_name -- the name of the field as given in the ipmidcmi results.
                      this will be used as the name of the attribute unless a
                      'attr' key/value is given in the field_info dict.
        value -- the value of the field as given in the ipmidcmi results. This
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
        are determined by calling ipmidcmi_types on this command instance,
        which gives a way for the result type and mapping to change based
        on the contents of the response.
        """
        result_type, mapping = self.ipmidcmi_types(response)

        if result_type == None:
            return None

        obj = result_type()
        lines = response.split('\n')
        left_over = []
        for line in lines:
            colon_index = 10000000
            if line.find(':') != -1:
                colon_index = line.index(':')
            equal_index = 10000000
            if line.find('=') != -1:
                equal_index = line.index('=')
            if colon_index == 10000000 and equal_index == 10000000:
                # Not a valid record -- skip line
                # Blank lines appear to be common in FreeIPMI output
                continue

            field_seperator = min([colon_index, equal_index])
            field = line[0:field_seperator].strip()
            value = line[field_seperator + 1:].strip()

            field_info = mapping.get(field)

            if field_info == None:
                left_over.append((field, value))
                continue

            self.field_to_objval(obj, field_info, field, value)

        return obj

    def parse_single_line(self, response, err):
        obj = self.result_type()
        attr_name = self.ipmidcmi_response_fields['attr']
        setattr(obj, attr_name, response.strip())
        return obj

    def ipmidcmi_types(self, response):
        """Return the result type and field mappings

        The result type is the class of the result to be used. The field
        mappings are given in self.ipmidcmi_response_fields, and are a
        dict mapping field names to field info dicts. See 'field info' in
        the doc for field_to_objval above.

        Arguments:
        response -- the text of the ipmidcmi response. It's not used in
        this base method, but might be used in a subclass's version of
        this method to allow different result types and mappings to be
        used based on the contents of the response.
        """
        return self.result_type, self.ipmidcmi_response_fields

    def parse_response(self, out, err):
        """Parse the response to a command

        The 'ipmidcmi_response_format' attribute is used to determine
        what parser to use to for interpreting the results.
        
        Arguments:
        out -- the text response of an ipmidcmi command from stdout
        err -- the text response of an ipmidcmi command from stderr
        """
        return self.ipmidcmi_parse_response(out, err)

    def ipmidcmi_parse_results(self, out, err):
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

    ipmidcmi_parse_response = parse_colon_record
