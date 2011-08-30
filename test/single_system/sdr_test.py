import sys, unittest

from singlesystemtest import SingleSystemTest

class TestSdrList(SingleSystemTest):
    def test_sdr_list(self):
        sdr_list = self.bmc.sdr_list()
        for sdr in sdr_list:
            try:
                sys.stderr.write(sdr.entity_id + '\n')
            except:
                pass

tests = [TestSdrList]

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=5).run(suite)
