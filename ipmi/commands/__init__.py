#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 
from _chassis import *
from _global import global_commands

ipmi_commands = {}

ipmi_commands.update(global_commands)
ipmi_commands.update(chassis_commands)
