#Copyright 2012 Calxeda, Inc.  All Rights Reserved.
"""PEF related commands"""

from .. import Command
from pyipmi.pet import *
from pyipmi.tools.responseparser import ResponseParserMixIn


class PETAcknowledgeCommand(Command, ResponseParserMixIn):
    """Describes the PET Acknowledge command

    This is "--pet-acknowledge" to ipmi-pet
    """
    name = "Send a PET Acknowledge"
    result_type = PETAcknowledgeResult

    response_fields = {
    }

    ipmi_pet_args = ['--pet-acknowledge']


pet_commands = {
    'pet_acknowledge'   : PETAcknowledgeCommand
}
