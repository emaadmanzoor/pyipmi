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
    """Describes the DCMI get capabilities command

    """

    name = "Get DCMI Capabilities"
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
    """Describes the DCMI set asset tag command

    """

    name = "Set DCMI Asset Tag"
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
    """Describes the dcmi get asset tag command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Get DCMI Asset Tag"
    result_type = DCMIGetAssetTagResult

    ipmidcmi_response_fields = {
        'attr' : 'tag'
    }

    ipmidcmi_args = ["--get-asset-tag"]


class DCMIGetManagementControllerID(DCMICommandWithErrors):
    """Describes the DCMI get management controller ID string command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Get Management Controller ID String"
    result_type = DCMIGetManagementControllerIDResult

    ipmidcmi_response_fields = {
    }

    ipmidcmi_args = ["--get-management-controller-identifier-string"]


class DCMIGetSensorInfo(DCMICommandWithErrors):
    """Describes the DCMI get sensor info command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Get DCMI Sensor Info"
    result_type = DCMIGetSensorInfoResult

    ipmidcmi_response_fields = {
    }

    ipmidcmi_args = ["--get-dcmi-sensor-info"]


class DCMIGetPowerStatistics(DCMICommandWithErrors):
    """Describes the DCMI get system power statistics command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Get Power Statistics"
    result_type = DCMIGetPowerStatisticsResult

    ipmidcmi_response_fields = {
    }

    ipmidcmi_args = ["--get-system-power-statistics"]


class DCMIGetPowerLimit(DCMICommandWithErrors):
    """Describes the DCMI get power limit command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Get Power Limit"
    result_type = DCMIGetPowerLimitResult

    ipmidcmi_response_fields = {
    }

    ipmidcmi_args = ["--get-power-limit"]


class DCMISetPowerLimit(DCMICommandWithErrors):
    """Describes the DCMI set power limit command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Set Power Limit"
    result_type = DCMISetPowerLimitResult

    ipmidcmi_response_fields = {
    }

    ipmidcmi_args = ["--set-power-limit"]

class DCMIPowerLimitRequested(DCMICommandWithErrors):
    """Describes the DCMI power limit requested command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Power Limit Requested (Watts)"
    result_type = DCMIPowerLimitRequestedResult

    ipmidcmi_response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """
        """
        return ["--power-limit-requested", self._params['limit']]


class DCMIActivatePowerLimit(DCMICommandWithErrors):
    """Describes the DCMI activate/deactivate power limit command

    """

    ipmidcmi_parse_response = IpmiDcmiCommandMixIn.parse_single_line

    name = "Activate Or Deactivate Power Limit"
    result_type = DCMIActivatePowerLimitResult

    ipmidcmi_response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """
        """
        return ["--activate-deactivate-power-limit", self._params['action']]


dcmi_commands = {
    "dcmi_get_capabilities"     : DCMIGetCapabilitiesCommand,
    "dcmi_set_asset_tag"        : DCMISetAssetTagCommand,
    "dcmi_get_asset_tag"        : DCMIGetAssetTagCommand,
    "dcmi_get_controller_id"    : DCMIGetManagementControllerID,
    "dcmi_get_sensor_info"      : DCMIGetSensorInfo,
    "dcmi_get_power_statistics" : DCMIGetPowerStatistics,
    "dcmi_get_power_limit"      : DCMIGetPowerLimit,
    "dcmi_set_power_limit"      : DCMISetPowerLimit,
    "dcmi_power_limit_requested": DCMIPowerLimitRequested,
    "dcmi_activate_power_limit" : DCMIActivatePowerLimit
}
