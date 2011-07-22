import sys

from ipmi import make_bmc
from ipmi.bmc import LanBMC

bmc = make_bmc(LanBMC, hostname = sys.argv[1], password = "admin")

info = bmc.info()

print info.firmware_revision
