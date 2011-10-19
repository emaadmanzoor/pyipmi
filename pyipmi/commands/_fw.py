#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

from .. import Command
from .. tools.ipmitool import IpmitoolCommandMixIn

class FWDownloadCommand(Command, IpmitoolCommandMixIn):
    """Describes the update_cdb_entry IPMI command

    """

    name = "Update SOCMananager"
    result_type = None

    ipmitool_response_fields = {
        "" : {}
    }

    @property
    def ipmitool_args(self):
        """The chassis control command takes a 'mode' parameter

        Look at ipmitool's manpage for more info.
        """
        return ["cxoem", "fw", "download", self._params['filename'],
                self._params['slot'], self._params['image_type'],
                "tftp", self._params['tftp_addr']]

fw_commands = {
    "fw_download" : FWDownloadCommand
}
