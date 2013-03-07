from collections import defaultdict
import sys
import os
if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s file"%(sys.argv[0])
f = open(sys.argv[1])
hist = defaultdict(lambda: 0)
prevutil = None
other = None
for l in f:
    if l.strip() == "":
        continue
    if "Utilization " in l:
        if prevutil != None:
            other.close()
        prevutil = l.strip().split('=')[1].strip()
        other = open("%s-%s"%(os.path.basename(sys.argv[1]), prevutil), 'w')
        print "Opening"
        continue
    p = l.strip()
    print >>other, p
if prevutil != None:
    other.close()
