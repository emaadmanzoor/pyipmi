import sys, unittest, os
import bmc_test
import power_test
from singlesystemtest import SingleSystemTest
import xmlrunner

tests = []
tests.extend(bmc_test.tests)
#tests.extend(power_test.tests)

ipmi_log = 'ipmi.log'

if (os.path.exists(ipmi_log)):
    os.remove(ipmi_log)

SingleSystemTest.logfile = open(ipmi_log, 'a+')

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        result = xmlrunner.XMLTestRunner(verbose = 1, output='test-reports').run(suite)
        if result.failures or result.errors:
            os.sys.exit(1)
