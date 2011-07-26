import json, unittest, os

from ipmi.bmc import LanBMC
from ipmi import make_bmc
from server import Server

class SingleSystemTest(unittest.TestCase):
    def __init__(self, *args):
        super(SingleSystemTest, self).__init__(*args)
        self.system_info = self.load_systems('systems.json')[self.system]
        self.bmc = make_bmc(LanBMC, **self.system_info['bmc'])
        self.server = Server(self.bmc)

    def load_systems(self, json_file):
        return json.load(open(json_file))

    def get_checks(self):
        file_name = os.path.join('system_types', self.system_info['type'] + '.json')
        return json.load(open(file_name))
