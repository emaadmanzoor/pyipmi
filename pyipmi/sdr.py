"""SDR records

These are really bare right now - look at the SDR commands to see
how they actually get filled out.
"""

class Sdr(object):
    """Base SDR record type for others to inherit"""
    pass

class AnalogSdr(Sdr):
    """An analog SDR record"""
    pass

class DiscreteSdr(Sdr):
    """A discrete SDR record"""
    pass
