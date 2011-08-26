import sys, unittest, os
import bmc_test
import power_test
from singlesystemtest import SingleSystemTest
import xmlrunner
import argparse

tests = []
tests.extend(bmc_test.tests)
#tests.extend(power_test.tests)

parser = argparse.ArgumentParser(description = 'Run all single system tests')

parser.add_argument('--system', required = True,
                        help=('system to test (from systems.json)'))

parser.add_argument('-p', action='store_true',
                help=('send some pings to the system during testing'))

args = parser.parse_args()

if args.p:
    SingleSystemTest.do_pings = True

ipmi_log = 'ipmi.log'

if (os.path.exists(ipmi_log)):
    os.remove(ipmi_log)

SingleSystemTest.logfile = open(ipmi_log, 'a+')

for test in tests:
    test.system = args.system
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    result = xmlrunner.XMLTestRunner(verbose = 1, output='test-reports').run(suite)
    if result.failures or result.errors:
        os.sys.exit(1)
