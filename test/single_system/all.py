import sys, unittest, os
import bmc_test
import power_test
from singlesystemtest import SingleSystemTest
import xmlrunner

tests = []
tests.extend(bmc_test.tests)
#tests.extend(power_test.tests)

os.remove('ipmi.log')
SingleSystemTest.logfile = open('ipmi.log', 'a+')

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        result = xmlrunner.XMLTestRunner(verbose = 1, output='test-reports').run(suite)
        if result.failures or result.errors:
            os.sys.exit(1)
