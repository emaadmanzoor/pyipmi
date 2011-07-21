import time

class ChassisStatus:
    """The response to a ChassisStatus command

    TODO: This is currently an odd mix of types.. there must be a better way
    """

    def __init__(self):
        self.power_restore_policy = None
        self.power_control_fault = None
        self.power_fault = None
        self.power_interlock = None
        self.power_overload = None
        self.power_on = None 
        self.last_power_event = None
        self.misc_chassis_state = None

class Chassis:
    def wait_after(f):
        def sleeper(self):
            ret = f(self)
            time.sleep(self._wait)
            return ret
        return sleeper

    def __init__(self, handle):
        self._handle = handle
        self._wait = 10
       
    def status(self):
        return self._handle.chassis_status()

    @wait_after
    def power_off(self):
        self._handle.chassis_control(mode="off")

    @wait_after
    def power_on(self):
        self._handle.chassis_control(mode="on")

    @wait_after
    def power_cycle(self):
        self._handle.chassis_control(mode="cycle")

    @wait_after
    def hard_reset(self):
        self._handle.chassis_control(mode="reset")

    @property
    def is_powered(self):
        return self._handle.chassis_status().power_on
