#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from .. tools.ipmidcmi import IpmiDcmiCommandMixIn
from pyipmi.dcmi import *

class DCMICommandWithErrors(Command, IpmiDcmiCommandMixIn):

    # TODO: Generalize this to base class?  Better way to include
    # error output in parsing?
    def parse_response(self, out, err):
        """Parse the response to a command

        The 'ipmitool_response_format' attribute is used to determine
        what parser to use to for interpreting the results.

        Arguments:
        out -- the text response of an ipmitool command from stdout
        err -- the text response of an ipmitool command from stderr
        """

        out = out + err
        return self.ipmidcmi_parse_response(out, err)

class DCMIGetCapabilitiesCommand(DCMICommandWithErrors):
    """Describes the cxoem fw download IPMI command

    """

    name = "Update a Firmware Image"
    result_type = DCMIGetCapabilitiesResult

    ipmidcmi_response_fields = {
        'DCMI Specification Conformance' : {},
        'Identification Support' : {},
        'SEL logging' : {},
        'Chassis Power' : {},
        'Temperature Monitor' : {},
        'Power Management / Monitoring Support' : {},
        'In-band System Interface Channel' : {},
        'Serial TMODE' : {},
        'Out-Of-Band Secondary LAN Channel' : {},
        'Out-Of-Band Primary LAN Channel' : {},
        'SOL' : {},
        'VLAN' : {},
        'Number of SEL entries' : {},
        'SEL automatic rollover' : {},
        'GUID' : {},
        'DHCP Host Name' : {},
        'Asset Tag' : {},
        'Inlet temperature' : {},
        'Processors temperature' : {},
        'Baseboard temperature' : {},
        'Power Management Device Slave Address' : {},
        'Power Management Controller Device Revision' : {},
        'Power Management Controller Channel Number' : {},
        'Primary LAN Out-of-band Channel Number' : {},
        'Secondary LAN Out-of-band Channel Number' : {},
        'Serial Out-of-band TMODE Capability Channel Number' : {}
    }

    ipmidcmi_args = ["--get-dcmi-capability-info"]

class DCMISetAssetTagCommand(DCMICommandWithErrors):
    """Describes the cxoem fw download IPMI command

    """

    name = "Update a Firmware Image"
    result_type = DCMISetAssetTagResult

    # No response -- Have to do a get to confirm
    ipmidcmi_response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """
        """
        return ["--set-asset-tag", self._params['tag']]

class DCMIGetAssetTagCommand(DCMICommandWithErrors):
    """Describes the cxoem fw download IPMI command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Update a Firmware Image"
    result_type = DCMIGetAssetTagResult

    ipmidcmi_response_fields = {
        'attr' : 'tag'
    }

    ipmidcmi_args = ["--get-asset-tag"]

dcmi_commands = {
    "dcmi_get_capabilities"   : DCMIGetCapabilitiesCommand,
    "dcmi_set_asset_tag"      : DCMISetAssetTagCommand,
    "dcmi_get_asset_tag"      : DCMIGetAssetTagCommand
}
