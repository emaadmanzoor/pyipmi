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


from .. import Command
from pyipmi.tools.responseparser import *
from pyipmi.dcmi import *

class DCMICommandWithErrors(Command, ResponseParserMixIn):

    # TODO: Generalize this to base class?  Better way to include
    # error output in parsing?
    def parse_response(self, out, err):
        """Parse the response to a command

        The 'response_format' attribute is used to determine
        what parser to use to for interpreting the results.

        Arguments:
        out -- the text response of a command from stdout
        err -- the text response of a command from stderr
        """

        out = out + err
        return self.response_parser(out, err)

class DCMIGetCapabilitiesCommand(DCMICommandWithErrors):
    """Describes the DCMI get capabilities command

    """

    name = "Get DCMI Capabilities"
    result_type = DCMIGetCapabilitiesResult

    response_fields = {
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
    response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """
        """
        return ["--set-asset-tag", self._params['tag']]

class DCMIGetAssetTagCommand(DCMICommandWithErrors):
    """Describes the dcmi get asset tag command

    """

    response_parser = ResponseParserMixIn.parse_single_line

    name = "Get DCMI Asset Tag"
    result_type = DCMIGetAssetTagResult

    response_fields = {
        'attr' : 'tag'
    }

    ipmidcmi_args = ["--get-asset-tag"]


class DCMIGetManagementControllerID(DCMICommandWithErrors):
    """Describes the DCMI get management controller ID string command

    """

    response_parser = ResponseParserMixIn.parse_single_line

    name = "Get Management Controller ID String"
    result_type = DCMIGetManagementControllerIDResult

    response_fields = {
        'attr' : 'DCMI'
    }

    ipmidcmi_args = ["--get-management-controller-identifier-string"]

class DCMISetManagementControllerID(DCMICommandWithErrors):
    """Describes the DCMI get management controller ID string command

    """
    response_parser = ResponseParserMixIn.parse_single_line

    name = "Set Management Controller ID String"
    result_type = DCMISetManagementControllerIDResult

    response_fields = {
        'attr' : 'DCMI'
    }
    
    @property
    def ipmidcmi_args(self):
        """
        """
        return ["--set-management-controller-identifier-string",  self._params['controller']]
class DCMIGetSensorInfo(DCMICommandWithErrors):
    """Describes the DCMI get sensor info command

    """
    def parse_response(self, out, err):
        """ Output is a number of lines with some info
        """
        new_out_list = []
        expected_fields = ['Inlet Temperature','CPU Temperature','Baseboard temperature']
        for line in out.strip().split('\n'):
            for field in expected_fields:
                if field in line:
                    value = line.lstrip(field)
                    new_line = field + " : " + value
                    new_out_list.append(new_line)
        new_output= "\n".join(new_out_list)
        return self.response_parser(new_output, err)
    
    name = "Get DCMI Sensor Info"
    result_type = DCMIGetSensorInfoResult
    response_fields = {
        'Inlet Temperature':{},
        'CPU Temperature' : {},
        'Baseboard temperature' :{}                        
    }


    ipmidcmi_args = ["--get-dcmi-sensor-info"]


class DCMIGetPowerStatistics(DCMICommandWithErrors):
    """Describes the DCMI get system power statistics command

    """

    name = "Get Power Statistics"
    result_type = DCMIGetPowerStatisticsResult

    response_fields = {
        'Current Power' : {},
        'Minimum Power over sampling duration' : {},
        'Maximum Power over sampling duration' : {},
        'Average Power over sampling duration' : {},
        'Time Stamp'                           : {},
        'Statistics reporting time period'     : {},
        'Power Measurement'                    : {}        
    }

    ipmidcmi_args = ["--get-system-power-statistics"]


class DCMIGetPowerLimit(DCMICommandWithErrors):
    """Describes the DCMI get power limit command

    """
    name = "Get Power Limit"
    result_type = DCMIGetPowerLimitResult

    response_fields = {
        'Exception Actions' : {} ,
        'Power Limit Requested' : {},
        'Correction time limit' : {},
        'Management application Statistics Sampling period' :{}                       
    }

    ipmidcmi_args = ["--get-power-limit"]


class DCMISetPowerLimit(DCMICommandWithErrors):
    """Describes the DCMI set power limit command

    """

    name = "Set Power Limit"
    result_type = DCMISetPowerLimitResult

    response_fields = {
    }

    ipmidcmi_args = ["--set-power-limit"]

class DCMIPowerLimitRequested(DCMICommandWithErrors):
    """Describes the DCMI power limit requested command

    """

    name = "Power Limit Requested (Watts)"
    result_type = DCMIPowerLimitRequestedResult

    response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """ """
        if self._params['exception'] is None:
            return ["--set-power-limit","--power-limit-requested", self._params['limit']]
        else:
            return ["--set-power-limit","--power-limit-requested", self._params['limit'],
                      "--exception-actions", self._params['exception']]

class DCMICorrectionTimeLimit(DCMICommandWithErrors):
    """Describes the DCMI correction time limit command

    """

    name = "Power Correction Time Limit (Milliseconds)"
    result_type = DCMICorrectionTimeLimitResult

    response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """
        """
        if self._params['exception'] is None:
            return ["--set-power-limit","--correction-time-limit", self._params['time_limit']]
        else:
            return ["--set-power-limit","--correction-time-limit", self._params['time_limit'],
                      "--exception-actions", self._params['exception']]

class DCMIStatisticsSamplingPeriod(DCMICommandWithErrors):
    """Describes the DCMI statistics sampling period command

    """
    name = "Power Statistics Sampling Period ( seconds)"
    result_type = DCMIStatisticsSamplingPeriodResult

    response_fields = {
    }

    @property
    def ipmidcmi_args(self):
        """        """
        if self._params['exception'] is None:
            return ["--set-power-limit","--statistics-sampling-period", self._params['period']]
        else:
            return ["--set-power-limit","--statistics-sampling-period", self._params['period'],
                      "--exception-actions", self._params['exception']]


class DCMIActivatePowerLimit(DCMICommandWithErrors):
    """Describes the DCMI activate/deactivate power limit command

    """

    response_parser = ResponseParserMixIn.parse_single_line

    name = "Activate Or Deactivate Power Limit"
    result_type = DCMIActivatePowerLimitResult

    response_fields = {
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
    "dcmi_set_controller_id"    : DCMISetManagementControllerID,
    "dcmi_get_sensor_info"      : DCMIGetSensorInfo,
    "dcmi_get_power_statistics" : DCMIGetPowerStatistics,
    "dcmi_get_power_limit"      : DCMIGetPowerLimit,
    "dcmi_set_power_limit"      : DCMISetPowerLimit,
    "dcmi_power_limit_requested": DCMIPowerLimitRequested,
    "dcmi_activate_power_limit" : DCMIActivatePowerLimit,
    "dcmi_correction_time_limit" : DCMICorrectionTimeLimit,
    "dcmi_statistics_sampling_period": DCMIStatisticsSamplingPeriod
}
