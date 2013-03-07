import sys
from numpy import arange
from random import choice, sample, random
from collections import defaultdict
from math import ceil
if len(sys.argv) < 6:
    print "Usage: %s servers filesize utilization iterations m" % (sys.argv[0])
    sys.exit(1)
servers = int(sys.argv[1])
filesize = int(sys.argv[2])
utilization = eval(sys.argv[3])
def GetNextRandomOfferAccept(availableMachines):
    c = choice(availableMachines)
    return c
iterations = int(sys.argv[4])
blocks_picked = defaultdict(lambda: 0)
m = int(sys.argv[5])
machines = [mac for mac in xrange(0, servers)]
#picking_strategy = eval(sys.argv[6])
for util in utilization:
    blocks_picked.clear()
    for i in xrange(0, iterations):
        sampled = []
        for j in xrange(0, m):
            picked = False
            while not picked:
                free = sample(machines, max(int(ceil(float(servers)*(1.0 - util))), m))
                while len(free) > 0:
                    mac = GetNextRandomOfferAccept(free)
                    free.remove(mac)
                    blocks_per_machine = filesize/servers
                    left_over = filesize % servers
                    if mac < left_over:
                        blocks_per_machine += 1
                    blocks = [b * servers + mac for b in xrange(0, blocks_per_machine)]
                    blocks = filter(lambda b: b not in sampled, blocks)
                    if len(blocks) > 0:
                        if random() < (1 - util):
                            block = choice(blocks)
                            blocks_picked[block] += 1
                            sampled.append(block)
                            picked = True
                            break

    print "# Utilization = %f"%(util)
    for block in xrange(0, filesize):
        print "%d %f"%(block, blocks_picked[block])
    print
    print
