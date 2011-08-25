import sys, unittest

from singlesystemtest import SingleSystemTest

class TestBmcInfo(SingleSystemTest):
    def test_bmc_info(self):
        """BMC info provides expected results"""
        info = self.bmc.info()
        check_items = self.get_checks()['BMCInfo']

        for item,expected in check_items.iteritems():
            self.assertEqual(expected, getattr(info, item))

#    def test_bmc_info_eleven_times(self):
#        """BMC info provides expected results 11 times in a row"""
#        for i in range(0, 11):
#            info = self.bmc.info()
#            check_items = self.get_checks()['BMCInfo']
#
#            for item,expected in check_items.iteritems():
#                self.assertEqual(expected, getattr(info, item))

class TestBmcGuid(SingleSystemTest):
    def test_bmc_guid(self):
        """BMC GUID provides expected results"""
        guid = self.bmc.guid()
        check_items = self.get_checks()['BMCGuid']

        for item,expected in check_items.iteritems():
            self.assertEqual(expected, getattr(guid, item))

tests = [TestBmcInfo, TestBmcGuid]

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=5).run(suite)
