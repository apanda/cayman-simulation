import sys
from numpy import arange
from random import choice
import random
from collections import defaultdict
from math import ceil
if len(sys.argv) < 7:
    print "Usage: %s servers filesize utilization iterations m picking_strategy" % (sys.argv[0])
    sys.exit(1)
servers = int(sys.argv[1])
filesize = int(sys.argv[2])
utilization = eval(sys.argv[3])
def GetNextOrderedOffer(availableMachines):
    return sorted(availableMachines)[0]
def GetNextRandomOffer(availableMachines):
    return choice(availableMachines)
iterations = int(sys.argv[4])
blocks_picked = defaultdict(lambda: 0)
m = int(sys.argv[5])
machines = [mac for mac in xrange(0, servers)]
picking_strategy = eval(sys.argv[6])
for util in utilization:
    samples_picked = defaultdict(lambda: 0)
    for i in xrange(0, iterations):
        sample = []
        for j in xrange(0, m):
            free = random.sample(machines, max(int(ceil(float(servers)*(1.0 - util))), m))
            mac = picking_strategy(free)
            free.remove(mac)
            blocks_per_machine = filesize/servers
            left_over = filesize % servers
            if mac < left_over:
                blocks_per_machine += 1
            blocks = [b * servers + mac for b in xrange(0, blocks_per_machine)]
            block = choice(filter(lambda b: b not in sample, blocks))
            blocks_picked[block] += 1
            sample.append(block)
        samples_picked[tuple(sorted(sample))] += 1
    print "# Utilization = %f"%(util)
    uniques = 0
    for sample, value in samples_picked.iteritems():
        uniques+=1 
        print "%d %f"%(uniques,value)
    print
    print
