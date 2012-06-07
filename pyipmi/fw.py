"""FW records

"""

class FWInfo(object):
    """Object to hold device-reported SPI flash table"""
    error = None

    def __str__(self):
        return "%s | %s | %s | %s | %s" % (self.slot, self.type, self.offset,
                                           self.size, self.flags)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.slot == other.slot and
                   self.type == other.type and
                   self.offset == other.offset and
                   self.size == other.size and
                   self.flags == other.flags and
                   self.version == other.version and
                   self.daddr == other.daddr)
        else:
            return False


class FWDownloadResult(object):
    """Object to hold firmware update results"""
    fw_error = None


class FWUploadResult(object):
    """Object to hold firmware retrieve results"""
    fw_error = None


class FWActivateResult(object):
    """Object to hold firmware activate results"""
    pass


class FWDeactivateResult(object):
    """Object to hold firmware deactivate results"""
    pass


class FWFlagsResult(object):
    """Object to hold firmware flag command results"""
    pass


class FWStatus(object):
    """Object to hold firmware operation status"""
    error = None


class FWCancelResult(object):
    """Object to hold firmware operation cancelation results"""
    pass


class FWCheckResult(object):
    """Object to hold firmware CRC check results"""
    error = None


class FWGetResult(object):
    """Object to hold firmware get results"""
    fw_error = None


class FWPutResult(object):
    """Object to hold firmware put results"""
    fw_error = None

