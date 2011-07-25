__all__ = ["BMC", "BMCInfo", "LanBMC"]

class BMCInfo:
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

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        
class BMC(object):
    """A BMC - what you're talking to when you're talking IPMI"""
    def __init__(self, handle_class, tool_class, command_list):
        self.handle = handle_class(self, tool_class, command_list)

    def info(self):
        return self.handle.get_device_id()

class LanBMC(BMC):
    """A BMC that's accessed over the LAN"""
    def __init__(self,
                    hostname,
                    username = None,
                    password = None,
                    port = 623,
                    **kwargs):

        self.params = {
            'username' : username,
            'hostname' : hostname,
            'password' : password,
            'port' : port
        }

        super(LanBMC, self).__init__(**kwargs)
