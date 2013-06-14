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


from .. import Command, IpmiError
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.fw import *


class FWDownloadCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw download IPMI command

    """

    name = "Update a Firmware Image"
    result_type = FWDownloadResult

    response_fields = {
        'File Name' : {},
        'Partition' : {},
        'Slot' : {'attr': 'partition'},
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
                self._params['partition'], self._params['image_type'],
                "tftp", self._params['tftp_addr']]


class FWUploadCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw upload IPMI command

    """

    name = "Retrieve Firmware From Device"
    result_type = FWUploadResult

    response_fields = {
        'File Name' : {},
        'Partition' : {},
        'Slot' : {'attr': 'partition'},
        'Type' : {},
        'IP' : {},
        'TFTP Handle ID' : {},
        'Start FW download failed' : {'attr': 'fw_error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "upload", self._params['partition'],
                self._params['filename'], self._params['image_type'],
                "tftp", self._params['tftp_addr']]


class FWRegisterReadCommand(Command, ResponseParserMixIn):
    """ cxoem fw register read command """
    name = "Register Firmware Read"
    result_type = FWRegisterReadResult
    
    response_fields = {
        'File Name' : {},
        'Partition' : {},
        'Type' : {},
        'Error' : {}
    }
    
    def parse_response(self, out, err):
        result = super(FWRegisterReadCommand, self).parse_response(out, err)
        if hasattr(result, "error"):
            raise IpmiError(result.error)
    
    @property
    def ipmitool_args(self):
        return ["cxoem", "fw", "register", "read", self._params['partition'],
                self._params['filename'], self._params['image_type']]


class FWRegisterWriteCommand(Command, ResponseParserMixIn):
    """ cxoem fw register write command """
    name = "Register Firmware Write"
    result_type = FWRegisterWriteResult
    
    response_fields = {
        'File Name' : {},
        'Partition' : {},
        'Type' : {},
        'Error' : {}
    }
    
    def parse_response(self, out, err):
        result = super(FWRegisterWriteCommand, self).parse_response(out, err)
        if hasattr(result, "error"):
            raise IpmiError(result.error)
    
    @property
    def ipmitool_args(self):
        return ["cxoem", "fw", "register", "write", self._params['partition'],
                self._params['filename'], self._params['image_type']]


class FWActivateCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw activate IPMI command

    """

    name = "Mark A Firmware Image As Active"
    result_type = FWActivateResult

    response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "activate", self._params['partition']]


class FWInvalidateCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw deactivate IPMI command

    """

    name = "Mark A Firmware Image As Inactive"
    result_type = FWDeactivateResult

    response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "invalidate", self._params['partition']]


class FWFlagsCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw flags IPMI command

    """

    name = "Set Flags For a Firmware Image"
    result_type = FWFlagsResult

    response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "flags", self._params['partition'],
                self._params['flags']]


class FWStatusCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw status IPMI command

    """

    name = "Check Status of Most Recent Upload or Download"
    result_type = FWStatus

    response_fields = {
        'Status' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "status", self._params['tftp_handle']]


class FWCheckCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw check IPMI command

    """

    name = "Perform CRC of a Firmware Image"
    result_type = FWCheckResult

    response_fields = {
        'Partition' : {},
        'Slot' : {'attr': 'partition'},
        'CRC32' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "check", self._params['partition']]


class FWCancelCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw cancel IPMI command

    """

    name = "Cancel an In-Progress Upload or Download"
    result_type = FWCancelResult

    response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "cancel", self._params['job_id']]


class FWInfoCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw info IPMI command

    """

    name = "Request Firmware Information"
    result_type = FWInfo
    response_parser = ResponseParserMixIn.parse_colon_record_list

    response_fields = {
        "Partition" : {},
        "Slot" : {"attr": "partition"},
        "Type" : {},
        "Offset" : {},
        "Size" : {},
        "Priority" : {},
        "Daddr" : {},
        "Flags" : {},
        "In Use" : {},
        "Version" : {},
        "Error" : {}
    }

    ipmitool_args = ["cxoem", "fw", "info"]


class FWGetCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw get IPMI command

    """

    name = "Retrieve Raw Firmware From Device"
    result_type = FWGetResult

    response_fields = {
        'File Name' : {},
        'Address' : {},
        'Size' : {},
        'IP' : {},
        'TFTP Handle ID' : {},
        'Start raw transfer failed' : {'attr': 'fw_error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "get", self._params['filename'],
                self._params['offset'], self._params['size'],
                "tftp", self._params['tftp_addr']]


class FWPutCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw put IPMI command

    """

    name = "Update Raw Firmware To Device"
    result_type = FWPutResult

    response_fields = {
        'File Name' : {},
        'Address' : {},
        'TSize' : {},
        'IP' : {},
        'TFTP Handle ID' : {},
        'Start raw transfer failed' : {'attr': 'fw_error'}
    }

    @property
    def ipmitool_args(self):
        """
        """
        return ["cxoem", "fw", "put", self._params['filename'],
                self._params['offset'], self._params['size'],
                "tftp", self._params['tftp_addr']]


class FWResetCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw reset IPMI command

    """

    name = "Reset to factory default"
    result_type = FWResetResult

    response_fields = {
        "Error" : {}
    }

    ipmitool_args = ["cxoem", "fw", "reset"]



class FWVersionCommand(Command, ResponseParserMixIn):
    """Describes the cxoem fw version IPMI command

    """

    name = "Set the firmware version"
    result_type = FWVersionResult

    response_fields = {
        "Error" : {}
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fw", "version", self._params['version']]


fw_commands = {
    "fw_download"       : FWDownloadCommand,
    "fw_upload"         : FWUploadCommand,
    "fw_register_read"  : FWRegisterReadCommand,
    "fw_register_write" : FWRegisterWriteCommand,
    "fw_activate"       : FWActivateCommand,
    "fw_invalidate"     : FWInvalidateCommand,
    "fw_flags"          : FWFlagsCommand,
    "fw_status"         : FWStatusCommand,
    "fw_check"          : FWCheckCommand,
    "fw_cancel"         : FWCancelCommand,
    "fw_info"           : FWInfoCommand,
    "fw_get"            : FWGetCommand,
    "fw_put"            : FWPutCommand,
    "fw_reset"          : FWResetCommand,
    "fw_version"        : FWVersionCommand
}
