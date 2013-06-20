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


"""Tool-independent mix-in for parsing IPMI results"""

from pyipmi import IpmiError
import string
import inspect


def str_to_list(val, **params):
    """convert string to list of substrings (default: single words)"""
    val = val.strip()
    if val == '':
        return []

    delimiter = params.get('delimiter', " ")
    return map(string.strip, val.split(delimiter))


def str2bool(val):
    """True if val is 'true', 'yes' or 'enabled, otherwise false"""
    return val.lower() in ['true', 'yes', 'enabled']


def str_to_dict(val, **params):
    """Returns the contents of the string 'val' as a dictionary"""
    result = {}
    operator = params.get('operator', ':')
    delimiter = params.get('delimiter', '\n')
    value_parser = params.get('value_parser', str)

    params['operator'] = params.get('value_operator', None)
    params['delimiter'] = params.get('value_delimiter', None)

    entries = val.split(delimiter)
    for entry in entries:
        key, op, value = entry.partition(operator)
        result[field_to_attr(key.strip())] = value_parser(value)
    return result


def paren_pair(val):
    """Convert 'foo (bar)' to ['foo', 'bar']"""
    return [p.strip(' )') for p in val.split('(')]


def field_to_attr(field_name):
    """Convert a field name to an attribute name
    
    Make the field all lowercase and replace ' ' with '_'
    (replace space with underscore)
    """
    result = field_name.lower()
    if result[0:1].isdigit():
        result = "n_" + result
    result = result.replace(' ', '_')
    result = result.replace('/', '_')
    result = result.replace('-', '_')
    result = result.replace('.', '_')
    result = result.replace('+', '_plus')
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
        line, sep, rest = response.partition('\n')
        left_over = []
        while line != '':
            colon_index = 10000000
            if line.find(':') != -1:
                colon_index = line.index(':')
            equal_index = 10000000
            if line.find('=') != -1:
                equal_index = line.index('=')
            if colon_index == 10000000 and equal_index == 10000000:
                line, sep, rest = rest.partition('\n')
                continue

            field_seperator = min([colon_index, equal_index])
            field = line[0:field_seperator].strip()
            value = line[field_seperator + 1:].strip()

            field_info = mapping.get(field)

            if field_info == None:
                left_over.append((field, value))
                line, sep, rest = rest.partition('\n')
                continue

            lines_to_get = field_info.get('lines', 1) - 1
            while lines_to_get > 0:
                line, sep, rest = rest.partition('\n')
                value += '\n' + line
                lines_to_get -= 1

            self.field_to_objval(obj, field_info, field, value)
            line, sep, rest = rest.partition('\n')
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
            obj = self.parse_colon_record(record.strip(), err)

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
        str_func = lambda x: str(x)
        attr_name = field_info.get('attr', field_to_attr(field_name))
        attr_parser = supplied_parser = field_info.get('parser', str_func)

        args, varargs, keywords, defaults = inspect.getargspec(attr_parser)
        if keywords == None:
            attr_parser = lambda x, **y: supplied_parser(x)
        setattr(obj, attr_name, attr_parser(value, **field_info))

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
        part = err.partition(":")
        if part[1] and part[0].strip().upper() == "ERROR":
            raise IpmiError(part[2].strip())
        else:
            raise IpmiError(err.strip())

    response_parser = parse_colon_record
