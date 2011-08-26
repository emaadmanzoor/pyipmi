import json, unittest, os, shlex
from subprocess import Popen, call

from ipmi.bmc import LanBMC
from ipmi import make_bmc
from server import Server

class SingleSystemTest(unittest.TestCase):
    logfile = None
    do_pings = False

    def __init__(self, *args):
        super(SingleSystemTest, self).__init__(*args)
        self.system_info = self.load_systems('systems.json')[self.system]
        self.bmc = make_bmc(LanBMC, logfile=self.logfile, **self.system_info['bmc'])
        self.server = Server(self.bmc)

    def load_systems(self, json_file):
        return json.load(open(json_file))

    def get_checks(self):
        file_name = os.path.join('system_types', self.system_info['type'] + '.json')
        return json.load(open(file_name))

    def id(self, *args, **kwargs):
        if self.shortDescription():
            return self.shortDescription()
        else:
            return super(SingleSystemTest, self).id(*args, **kwargs)

    def run(self, *args, **kwargs):
        if self.logfile:
            out = 'STARTING TEST: ' + self.shortDescription() + '\n'
            self.logfile.write(out)

        super(SingleSystemTest, self).run(*args, **kwargs)

    def setUp(self):
        if self.do_pings:
            self.start_pings()

    def tearDown(self):
        if self.do_pings:
            self.stop_pings()

    def start_pings(self):
        cmd = 'sudo ping -c 5 -l 5 -i 0.2 %s' % (
                str(self.system_info['bmc']['hostname'])
        )

        args = shlex.split(cmd)
        self._pinger = Popen(args)

    def stop_pings(self):
        args = shlex.split('sudo kill -SIGTERM %d' % (self._pinger.pid))
        call(args)
        self._pinger.wait()
