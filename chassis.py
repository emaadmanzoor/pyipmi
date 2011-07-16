from ipmi import Command

def str2bool(v):
  return v.lower() == "true"

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
        
class ChassisStatusCommand(Command):
    """Describes the chassis status IPMI command"""

    name = "Chassis Status"

    def ipmitool_args(self):
        return ["chassis", "status"]

    def ipmitool_parse_results(self, response):
        status = ChassisStatus()
        lines = response.split("\n")
        for line in lines:
            if line.find(':') == -1:
                continue

            field, value = [field.strip() for field in line.split(":")]

            if field == 'System Power':
                if value == 'on':
                    status.power_on = True
                else:
                    status.power_off = True

            if field == 'Power Overload':
                status.power_fault = str2bool(value)
            
            if field == 'Power InterLock':
                status.power_interlock = value
            
            if field == 'Main Power Fault':
                status.power_fault = str2bool(value)

            if field == 'Power Control Fault':
                status.power_fault = str2bool(value)

            if field == 'Power Restore Policy':
                status.power_restore_policy = value

        return status
