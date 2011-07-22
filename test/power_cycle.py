#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

import sys
from ipmi import make_bmc
from server import Server
from ipmi.bmc import LanBMC

bmc = make_bmc(LanBMC, hostname = sys.argv[1], password = "admin")
server = Server(bmc)

print "Power on: %s" % server.is_powered

server.power_off()

print "Power on: %s" % server.is_powered

server.power_on()

print "Power on: %s" % server.is_powered
