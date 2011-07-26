#Copyright 2011 Calxeda, Inc.  All Rights Reserved.
import sys, unittest

from singlesystemtest import SingleSystemTest

class ServerPowerTest(SingleSystemTest):
    def test_power_cycle(self):
        server = self.server

        server.power_on()
        self.assertTrue(server.is_powered)
        server.power_off()
        self.assertFalse(server.is_powered)
        server.power_on()
        self.assertTrue(server.is_powered)

tests = [ServerPowerTest]

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=5).run(suite)
