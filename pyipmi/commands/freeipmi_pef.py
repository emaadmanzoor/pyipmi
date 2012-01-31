#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
"""PEF related commands"""

from .. import Command
from pyipmi.freeipmi_pef import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class FreeIPMIPEFInfoCommand(Command, ResponseParserMixIn):
    """Describes the get PEF info IPMI command

    This is "--info" to ipmi-pef-config
    """
    name = "Get PEF Info and Capabilities"
    result_type = FreeIPMIPEFInfoResult

    ipmi_pef_config_response_fields = {
        'PEF version' : {},
        'Alert action' : {},
        'Power down action' : {},
        'Power reset action' : {},
        'Power cycle action' : {},
        'OEM action' : {},
        'Diagnostic interrupt action' : {},
        'OEM event record filtering' : {},
        'Number of Event Filter Table entries' : {},
        'Number of Event Filters' : {},
        'Number of Alert Policy entries' : {},
        'Number of Alert Strings' : {}
    }

    ipmi_pef_config_args = ['--info']


class FreeIPMIPEFCheckout(Command, ResponseParserMixIn):
    """Retrieve platform event filtering configuration

    """
    name = "Checkout PEF Configuration"
    result_type = FreeIPMIPEFCheckoutResult

    ipmi_pef_config_response_fields = {
    }

    @property
    def ipmi_pef_config_args(self):
        """
        """
        section = ""
        if self._params.get("section"):
            section = "--section=%s" % self._params.get("section")

        filename = self._params.get('filename')

        if filename:
            return ["--checkout", "--filename=" + filename, section]

        key_value_pair = self._params.get('key_value_pair')
        if key_value_pair:
            return ["--checkout", "--key-pair=" + key_value_pair, section]

        return ["--checkout", section]


class FreeIPMIPEFCommit(Command, ResponseParserMixIn):

    """Update PEF configuration from file or key-value pair

    """
    name = "Update PEF Configuration"
    result_type = FreeIPMIPEFCommitResult

    ipmi_pef_config_response_fields = {
    }

    @property
    def ipmi_pef_config_args(self):
        """
        """
        filename = self._params.get('filename')

        if filename:
            return ["--commit", "--filename=" + filename]

        key_value_pair = self._params.get('key_value_pair')
        if key_value_pair:
            return ["--commit", "--key-pair=" + key_value_pair]

        raise Exception("Command pef-config --commit requires either filename or key-value pair")


class FreeIPMIPEFDiff(Command, IpmiPEFConfigCommandMixIn):
    """ Command to diff current PEF configuration against a file or key-value pair
    
    """
    name = "PEF Diff"
    result_type = FreeIPMIDiffResult

    ipmi_pef_config_response_fields = {
    }

    @property
    def ipmi_pef_config_args(self):
        """
        """
        filename = self._params.get('filename')

        if filename:
            return ["--diff", "--filename=" + filename]

        key_value_pair = self._params.get('key_value_pair')
        if key_value_pair:
            return ["--diff", "--key-pair=" + key_value_pair]

        raise Exception("Command pef-config --diff requires either filename or key-value pair")


class FreeIPMIPEFListSections(Command, ResponseParserMixIn):
    """Describes the get PEF list sections command

    """
    name = "List PEF Table Sections"
    result_type = FreeIPMIPEFListSectionsResult

    ipmi_pef_config_response_fields = {
    }

    ipmi_pef_config_args = ["--listsections"]


pef_commands = {
    'pef_config_info'   : FreeIPMIPEFInfoCommand,
    'pef_checkout'      : FreeIPMIPEFCheckout,
    'pef_commit'        : FreeIPMIPEFCommit,
    'pef_diff'          : FreeIPMIPEFDiff,
    'pef_list_sections' : FreeIPMIPEFListSections
}
