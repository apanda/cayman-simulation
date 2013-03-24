#! /usr/bin/env python

###########
# Implement Sim1 written by Panda
# TODO: 
# Simu II - blocks are not evenly placed on machines
###########

import sys
from numpy import arange
from random import choice, sample, expovariate
from collections import defaultdict
from math import ceil

from utils import *

###############
# Main function
###############

if __name__ == '__main__':
  if len(sys.argv) < 9:
    print "Usage: %s sim_time(s) arrival_int_mean(s) job_duration_mean(s) filesize(N) machines(Nm) slots(Ns) iter samples(M)" % (sys.argv[0])
    sys.exit(1)

  sim_time = int(sys.argv[1])
  arrival_int_mean = float(sys.argv[2])
  job_dur_mean = float(sys.argv[3])
  N = int(sys.argv[4])
  Nm = int(sys.argv[5])
  Ns = int(sys.argv[6])
  itera = int(sys.argv[7])
  M = int(sys.argv[8])

  if N < Nm:
    print "The file size should be larger than the number of servers"
    sys.exit(1)
  if M > N:
    print "The number of samples should be smaller than the number of blocks"
    sys.exit(1)


  
  #machs_blks = alloc_blks_to_machs(N,Nm)
  machs_blks = random_alloc_blks_to_machs(N,Nm)
  machs_slots = alloc_slots_to_machs(Ns,Nm)

  for it in xrange(0, itera): #iterations
    accessed_blocks = defaultdict(lambda: 0)
    accessed_slots = defaultdict(lambda: 0)
    distinct_samples = defaultdict(lambda: 0)
    blks_sample = defaultdict(lambda: [])
    same_samples = 0
    non_local_access = 0
    wait_jobs = []
    
    slots_idle = [s for s in xrange(0, Ns)]
    (jobs_in, jobs_duration) = possion(sim_time, arrival_int_mean, job_dur_mean)

    events = []
    for i in xrange(0, len(jobs_in)):
      events.append((jobs_in[i], 0, [], i))
 #TODO: change type to be "in" or "out"

    for e in events: #events [(time, type, slots, jobid)]
      #print 'an event', e
      if(e[1] == 0):
        job_id = e[3]
        if len(slots_idle) < M:
          slots_sample = [slot for slot in slots_idle]
          wait_jobs.append( [e[0], job_id, M-len(slots_idle)])
        else:
          slots_sample = sample(slots_idle, M)
        for slot in slots_sample:
          mach = map_slot_to_mach(slot, machs_slots)
          (blk, non_local) = select_block(machs_blks[mach], blks_sample[job_id], N)
          non_local_access += non_local
          blks_sample[job_id].append(blk)
          slots_idle.remove(slot); 
          accessed_slots[slot] += jobs_duration[job_id]
          accessed_blocks[blk] += jobs_duration[job_id]
        if len(slots_sample) == M:
          blks_sample[job_id].sort()
          distinct_samples[tuple(blks_sample[job_id])] += 1
        #add output events
        if len(slots_sample) > 0:
          #print 'add events (', e[0]+jobs_duration[job_id], 1, slots_sample, job_id, ')'
          events.append( (e[0]+jobs_duration[job_id], 1, slots_sample, job_id) )
          events.sort()

      elif e[1] == 1: #jobs_out
        slots_idle += e[2]
        while len(wait_jobs) > 0 and len(slots_idle) > 0:
          job_id = wait_jobs[0][1]
          slots_need = wait_jobs[0][2]
          if len(slots_idle) < slots_need:
            slots_sample = [slot for slot in slots_idle]
            wait_jobs[0][2] -= len(slots_idle)
          else:
            slots_sample = sample(slots_idle, slots_need)
            del wait_jobs[0]
          for slot in slots_sample:
            mach = map_slot_to_mach(slot, machs_slots)
            (blk, non_local) = select_block(machs_blks[mach], blks_sample[job_id], N)
            non_local_access += non_local
            blks_sample[job_id].append(blk)
            slots_idle.remove(slot); 
            accessed_slots[slot] += jobs_duration[job_id]
            accessed_blocks[blk] += jobs_duration[job_id]
          if len(slots_sample) == slots_need:
            blks_sample[job_id].sort()
            distinct_samples[tuple(blks_sample[job_id])] += 1
          #add output events
          if len(slots_sample) > 0: #TODO: do not need?
            #print 'add events (', e[0]+jobs_duration[job_id], 1, slots_sample, job_id, ')'
            events.append( (e[0]+jobs_duration[job_id], 1, slots_sample, job_id) )
            events.sort()
          
    #print 'distinct_samples', distinct_samples
    for v in distinct_samples.itervalues():
      if v > 1:
        same_samples += (v-1)
  
     
    print "#Iteration : ", it
    print "# Blocks Util"
    for block in xrange(0, N):
      print "%d %f"%(block, accessed_blocks[block])
    print "# Slots Util"
    for slot in xrange(0, Ns):
      print "%d %f"%(slot, accessed_slots[slot])
    print 'Number of times that two jobs select identical blks', same_samples
    print 'Number of Non-local access', non_local_access
