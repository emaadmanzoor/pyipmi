#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from .. tools.ipmitool import IpmitoolCommandMixIn
from pyipmi.fw import *

class CommandWithErrors(Command, IpmitoolCommandMixIn):

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
        return self.ipmitool_parse_response(out, err)

class FWDownloadCommand(CommandWithErrors):
    """Describes the cxoem fw download IPMI command

    """

    name = "Update a Firmware Image"
    result_type = FWDownloadResult

    ipmitool_response_fields = {
        'File Name' : {},
        'Slot' : {},
        'Type' : {},
        'IP' : {},
        'TFTP Handle ID' : {},
        'Start FW download failed' : {'attr': 'fw_error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "download", self._params['filename'],
                self._params['slot'], self._params['image_type'],
                "tftp", self._params['tftp_addr']]


class FWUploadCommand(CommandWithErrors):
    """Describes the cxoem fw upload IPMI command

    """

    name = "Retrieve Firmware From Device"
    result_type = FWUploadResult

    ipmitool_response_fields = {
        'File Name' : {},
        'Slot' : {},
        'Type' : {},
        'IP' : {},
        'TFTP Handle ID' : {},
        'Start FW download failed' : {'attr': 'fw_error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "upload", self._params['slot'],
                self._params['filename'], self._params['image_type'],
                "tftp", self._params['tftp_addr']]


class FWActivateCommand(CommandWithErrors):
    """Describes the cxoem fw activate IPMI command

    """

    name = "Mark A Firmware Image As Active"
    result_type = FWActivateResult

    ipmitool_response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "activate", self._params['slot']]


class FWInvalidateCommand(CommandWithErrors):
    """Describes the cxoem fw deactivate IPMI command

    """

    name = "Mark A Firmware Image As Inactive"
    result_type = FWDeactivateResult

    ipmitool_response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "invalidate", self._params['slot']]


class FWFlagsCommand(CommandWithErrors):
    """Describes the cxoem fw flags IPMI command

    """

    name = "Set Flags For a Firmware Image"
    result_type = FWFlagsResult

    ipmitool_response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "flags", self._params['slot'],
                self._params['flags']]


class FWStatusCommand(CommandWithErrors):
    """Describes the cxoem fw status IPMI command

    """

    name = "Check Status of Most Recent Upload or Download"
    result_type = FWStatus

    ipmitool_response_fields = {
        'Status' : {},
        'Error' : {'attr': 'error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "status", self._params['tftp_handle']]


class FWCheckCommand(CommandWithErrors):
    """Describes the cxoem fw check IPMI command

    """

    name = "Perform CRC of a Firmware Image"
    result_type = FWCheckResult

    ipmitool_response_fields = {
        'Slot' : {},
        'CRC32' : {},
        'Error' : {'attr': 'error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "check", self._params['slot']]


class FWCancelCommand(CommandWithErrors):
    """Describes the cxoem fw cancel IPMI command

    """

    name = "Cancel an In-Progress Upload or Download"
    result_type = FWCancelResult

    ipmitool_response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "cancel", self._params['job_id']]


class FWInfoCommand(CommandWithErrors):
    """Describes the cxoem fw info IPMI command

    """

    name = "Request Firmware Information"
    result_type = FWInfo
    ipmitool_parse_response = IpmitoolCommandMixIn.parse_colon_record_list

    ipmitool_response_fields = {
        "Slot" : {},
        "Type" : {},
        "Offset" : {},
        "Size" : {},
        "Flags" : {}
    }

    ipmitool_args = ["cxoem", "fw", "info"]


class FWBlowCommand(CommandWithErrors):
    """Describes the cxoem fw blow IPMI command

    """

    name = "Write a Whole Flash Image"
    result_type = FWBlowResult

    ipmitool_response_fields = {
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "blow", self._params['filename']]


fw_commands = {
    "fw_download"   : FWDownloadCommand,
    "fw_upload"     : FWUploadCommand,
    "fw_activate"   : FWActivateCommand,
    "fw_invalidate" : FWInvalidateCommand,
    "fw_flags"      : FWFlagsCommand,
    "fw_status"     : FWStatusCommand,
    "fw_check"      : FWCheckCommand,
    "fw_cancel"     : FWCancelCommand,
    "fw_info"       : FWInfoCommand,
    "fw_blow"       : FWBlowCommand
}
