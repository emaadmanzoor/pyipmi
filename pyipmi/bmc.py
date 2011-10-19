"""Stuff about BMC's"""

__all__ = ['BMC', 'BMCInfo', 'BMCGuid', 'BMCEnables', 'LanBMC']

class BMCResult(object):
    """superclass for BMC result objects
    
    Sets attribute names from a dict passed to init, and allows comparison
    with other results based on dict equality.
    """
    def __init__(self, **entries):
        """each kwarg's value to an attribute of the same name"""
        self.__dict__.update(entries)

    def __eq__(self, other):
        """BMCInfo's are equivalent if their attributes are the same"""
        return self.__dict__ == other.__dict__


class BMCInfo(BMCResult):
    """Describes a BMC info record result
    
    "bmc info" is just the ipmitool name - this is really "get device id"
    """
    device_id = None
    device_revision = None
    firmware_revision = None
    ipmi_version = None
    is_chassis_device = None
    is_bridge = None
    is_ipmb_event_generator = None
    is_ipmb_event_receiver = None
    is_fru_inventory_device = None
    is_sel_device = None
    is_sdr_repository_device = None
    is_sensor_device = None
    manufacturer_id = None
    product_id = None
    device_available = None
    aux_firmware_revision_info = None

class BMCGuid(BMCResult):
    """Result record for bmc guid command

    this is really "get device guid" - bmc guid is the ipmitool command name.
    """
    system_guid = None
    time_stamp = None

class BMCEnables(BMCResult):
    """Result record for get command enables

    The names for the attributes here come from the command line syntax for ipmitool
    """
    recv_msg_intr = None
    event_msg_intr = None
    event_msg = None
    system_event_log = None
    oem0 = None
    oem1 = None
    oem2 = None

class BMC(object):
    """A BMC - what you're talking to when you're talking IPMI
    
    I think this should ultimately be the interface for all commands issued
    from IPMI.. or maybe just commands "about the bmc". This needs to be
    resolved!
    """
    def __init__(self, handle_class, tool_class, command_list):
        """
        Arguments:
        handle_class -- class to use for Handles created
        tool_class -- class to use for the Tool for each handle
        command_list -- the list of commands available for this BMC
        """
        self.handle = handle_class(self, tool_class, command_list)

    def info(self):
        """Get the BMC's info"""
        return self.handle.get_device_id()

    def guid(self):
        """Get the BMC's guid"""
        return self.handle.get_system_guid()

    def sdr_list(self):
        """Get a list of SDR's for the BMC"""
        return self.handle.get_sdr_list()

    def enables(self):
        """Return a BMCEnables object for the BMC"""
        return self.handle.get_command_enables()

    def update_socman(self, filename, slot, tftp_addr):
        return self.update_firmware(filename, slot, '3', tftp_addr)

    def update_firmware(self, filename, slot, image_type, tftp_addr):
        return self.handle.fw_download(filename=filename, slot=slot,
                                       image_type=image_type,
                                       tftp_addr=tftp_addr)

class LanBMC(BMC):
    """A BMC that's accessed over the LAN"""
    def __init__(self,
                    hostname,
                    username=None,
                    password=None,
                    authtype=None,
                    level=None,
                    port=623,
                    **kwargs):

        self.params = {
            'hostname' : hostname,
            'username' : username,
            'password' : password,
            'authtype' : authtype,
            'level'    : level,
            'port'     : port
        }

        super(LanBMC, self).__init__(**kwargs)
