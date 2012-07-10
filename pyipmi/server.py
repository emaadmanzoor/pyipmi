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


"""A representation of a server.

This may go away - it doesn't do anything other than what chassis does.

Don't add to this.
"""

from chassis import Chassis

__all__ = ['Server']

class Server:
    """A server is managed over IPMI"""

    def __init__(self, bmc):
        """
        Arguments:

        bmc -- the BMC that's managing this server
        """
        self.bmc = bmc
        self._chassis = Chassis(self.bmc.handle)

    def power_off(self):
        """Power off server if it's powered on"""
        if self._chassis.is_powered:
            self._chassis.power_off()

    def power_on(self):
        """Power on server if it's powered off"""
        if not self._chassis.is_powered:
            self._chassis.power_on()

    def power_cycle(self):
        """Power cycle server"""
        self._chassis.power_cycle()

    def hard_reset(self):
        """Warm reset server"""
        self._chassis.hard_reset()

    @property
    def is_powered(self):
        """True if server is powered, otherwise false"""
        return self._chassis.is_powered
