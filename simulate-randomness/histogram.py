from collections import defaultdict
import sys
if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s file"%(sys.argv[0])
f = open(sys.argv[1])
hist = defaultdict(lambda: 0)
prevutil = None
for l in f:
    if l.strip() == "":
        continue
    if "Utilization " in l:
        if prevutil != None:
            print prevutil
            for k in sorted(hist.keys()):
                print "%f %d"%(k, hist[k])
            print
            print
        prevutil = l.strip()
        hist.clear()
        continue
    p = l.strip().split()
    count = float(p[1])
    hist[count] += 1
if prevutil != None:
    print prevutil
    for k in sorted(hist.keys()):
        print "%f %d"%(k, hist[k])
