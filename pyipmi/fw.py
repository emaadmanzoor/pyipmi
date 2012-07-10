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


"""FW records"""

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


class FWResetResult(object):
    """Object to hold firmware reset results"""
    pass

