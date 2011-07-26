import sys, unittest
import bmc_test
import power_test
import xmlrunner

tests = []
tests.extend(bmc_test.tests)
tests.extend(power_test.tests)

if __name__ == '__main__':
    for test in tests:
        test.system = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        xmlrunner.XMLTestRunner(verbose = 1, output='test-reports').run(suite)
