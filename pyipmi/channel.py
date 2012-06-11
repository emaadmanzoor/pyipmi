#Copyright 2011-2012 Calxeda, Inc.  All Rights Reserved.

"""ipmitool channel Results"""

class ChannelInfoResult(object):
    """Object to hold channel info results"""
    pass

class ChannelGetAccessResult(object):
    """Object to hold channel get access results"""
    pass

class ChannelSetAccessResult(object):
    """Object to hold channel set access results"""
    pass

class ChannelGetCiphersResult(object):
    """Object to hold get channel cipher suites results"""
    iana = None
    auth_alg = None
    integrity_alg = None
    confidentiality_alg = None
