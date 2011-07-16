import sys

from ipmi import Handle
from ipmitool import IpmiTool
from commands import ipmi_commands
from lanbmc import LanBMC

b = LanBMC(sys.argv[1], password = "admin")
s = b.handle(Handle, IpmiTool, ipmi_commands)

chassis_status = s.chassis_status()
print "Power on: %s" % (chassis_status.power_on)
