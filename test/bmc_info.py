import sys, json

from ipmi import make_bmc
from ipmi.bmc import LanBMC, BMCInfo

def load_systems(json_file):
    return json.load(open(json_file))

def load_bmcs(systems):
    bmcs = []
    for name,info in systems.iteritems():
        bmcs.append(make_bmc(LanBMC, **info['bmc']))
    return bmcs

def get_checks(system_type):
    file_name = system_type + '.json'
    return json.load(open(file_name))

def check_bmc_info(name, system_info):
    bmc = make_bmc(LanBMC, **system_info['bmc'])
    info = bmc.info()
    check_items = get_checks(system_info['type'])['BMCInfo']

    for item,expected in check_items.iteritems():
        if getattr(info, item) == expected:
            print 'Matched: ' + item
        else:
            print 'Missed: ' + item

systems = load_systems(sys.argv[1])

for name, info in systems.iteritems():
    check_bmc_info(name, info)
