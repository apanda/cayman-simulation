import sys
from numpy import arange
from random import choice, sample
from collections import defaultdict
from math import ceil
if len(sys.argv) < 4:
    print "Usage: %s filesize iterations m" % (sys.argv[0])
    sys.exit(1)
blocks = [bs for bs in xrange(0, int(sys.argv[1]))]
accessed_blocks = defaultdict(lambda: 0)
distinct_samples = defaultdict(lambda: 0)
m = int(sys.argv[3])
for it in xrange(0, int(sys.argv[2])):
    samp = sample(blocks, m)
    for s in samp:
        accessed_blocks[s] += 1
    distinct_samples[tuple(samp)] += 1
    
print "# Utilization = Baseline"
for block in xrange(0, int(sys.argv[1])):
    print "%d %f"%(block, accessed_blocks[block])
