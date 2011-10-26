"""FW records

"""

class FWInfo(object):
    """Object to hold device-reported SPI flash table"""

    def __str__(self):
        return "%s | %s | %s | %s | %s" % (self.slot, self.type, self.offset,
                                           self.size, self.flags)


class FWDownloadResult(object):
    """Object to hold firmware update results"""
    start_fw_download_failed = None


class FWUploadResult(object):
    """Object to hold firmware retrieve results"""
    pass


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
    pass


class FWCancelResult(object):
    """Object to hold firmware operation cancelation results"""
    pass


class FWCheckResult(object):
    """Object to hold firmware CRC check results"""
    pass


class FWBlowResult(object):
    """Object to hold firmware blow results"""
    pass
