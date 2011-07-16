#Copyright 2011 Calxeda, Inc.  All Rights Reserved. 

import sys

from lanbmc import LanBMC
from server import Server

bmc = LanBMC(sys.argv[1], password = "admin")
server = Server(bmc)

print "Power on: %s" % server.is_powered

server.power_off()

print "Power on: %s" % server.is_powered

server.power_on()

print "Power on: %s" % server.is_powered
