#Copyright 2012 Calxeda, Inc.  All Rights Reserved. 
"""Tool-independent mix-in for parsing IPMI results"""

from pyipmi import IpmiError


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


class ResponseParserMixIn(object):
    """Add this MixIn to a Command to enable it to parse response strings into
    response data structures"""

    """ 
    Supplied parse methods are parse_colon_record() (the default) and 
    parse_colon_record_list().  Override the default in a derived class
    by setting the "response_parser" field to the name of the desired
    method.
    """

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
        are determined by calling get_response_types on this command instance,
        which gives a way for the result type and mapping to change based
        on the contents of the response.
        """
        result_type, mapping = self.get_response_types(response)

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


    def parse_colon_record_list(self, response, err):
        """Parse multiple groups of colon records
        
        Like colon records, but with multiple groups, each separated
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


    def parse_single_line(self, response, err):
        obj = self.result_type()
        attr_name = self.response_fields['attr']
        setattr(obj, attr_name, response.strip())
        return obj


    def field_to_objval(self, obj, field_info, field_name, value):
        """Assign a field's value to an attribute of obj
        
        Arguments:
        obj -- the object to set the attribute on. this is some record type
               object - the exact varies depending on the command being
               executed.
        field_info -- a dict describing the field. See "Field Info" below for
                      more info.
        field_name -- the name of the field as given in the IPMI results.
                      this will be used as the name of the attribute unless a
                      'attr' key/value is given in the field_info dict.
        value -- the value of the field as given in the IPMI results. This
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

    def get_response_types(self, response):
        """Return the result type and field mappings

        The result type is the class of the result to be used. The field
        mappings are given in self.response_fields, and are a
        dict mapping field names to field info dicts. See 'field info' in
        the doc for field_to_objval above.

        Arguments:
        response -- the text of the command response. It's not used in
        this base method, but might be used in a subclass's version of
        this method to allow different result types and mappings to be
        used based on the contents of the response.
        """
        return self.result_type, self.response_fields

    def parse_response(self, out, err):
        """Parse the response to a command
        
        Arguments:
        out -- the text response of an IPMI command from stdout
        err -- the text response of an IPMI command from stderr
        """
        return self.response_parser(out, err)

    def parse_results(self, out, err):
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

    response_parser = parse_colon_record
