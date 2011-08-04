import sys, unittest

from singlesystemtest import SingleSystemTest

class TestBmcInfo(SingleSystemTest):
    def test_bmc_info(self):
        """BMC info provides expected results"""
        info = self.bmc.info()
        check_items = self.get_checks()['BMCInfo']

        for item,expected in check_items.iteritems():
            self.assertEqual(expected, getattr(info, item))

tests = [TestBmcInfo]

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=5).run(suite)
