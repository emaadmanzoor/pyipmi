from ipmi import BMC

class LanBMC(BMC):
    """A BMC that's accessed over the LAN"""
    def __init__(self, hostname, password = None, port = 623):
        self.params = {
            'hostname' : hostname,
            'password' : password,
            'port' : port
        }
