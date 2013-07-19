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


"""Fabric results"""

class FabricGetIPInfoResult(object):
    """Object to hold fabric ip list results"""
    pass

class FabricGetMACAddressesResult(object):
    """Object to hold fabric mac list results"""
    pass

class FabricUpdateConfigResult(object):
    """Object to hold update config list results"""

class FabricGetUplinkInfoResult(object):
    """Object to hold fabric uplink_info results"""
    pass

class FabricGetUplinkSpeedResult(object):
    """Object to hold fabric uplink_info results"""
    pass

class FabricGetLinkStatsResult(object):
    """Object to hold the fabric link_stats results"""
    pass

class FabricGetLinkMapResult(object):
    """Object to hold the fabric linkmap results"""
    pass

class FabricGetRoutingTableResult(object):
    """Object to hold the fabric routing_table results"""
    pass

class FabricGetDepthChartResult(object):
    """Object to hold the fabric depth_chart results"""
    pass
