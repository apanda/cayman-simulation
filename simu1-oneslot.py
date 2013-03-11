#! /usr/bin/env python

###########
# Implement Sim1 written by Panda
# Currently each machine has 1 slot
# TODO: 
# 1. More than 1 slots per machine
###########

import sys
from numpy import arange
from random import choice, sample, expovariate
from collections import defaultdict
from math import ceil

def alloc_blks_to_machs(N, Nm):
  Bm = N / Nm
  mach_blks = {}.fromkeys((k for k in xrange(0,Nm)))
  for k in xrange(0, Nm):
    mach_blks[k] = [v for v in xrange((k)*Bm, (k+1)*Bm)]
  left = N % Nm
  for a in xrange(0, left):
    mach_blks[a].append(Nm*Bm + a)
  return mach_blks

def possion(total_time, arrival_int, duration):
  jobs_in = []
  jobs_duration = []
  arrival_time = expovariate(1.0/arrival_int)
  while arrival_time < total_time:
    jobs_in.append(arrival_time)
    dur = expovariate(1.0/duration)
    jobs_duration.append(dur)
    intval = expovariate(1.0/arrival_int)
    arrival_time += intval 
  #print 'jobs_in', jobs_in
  #print 'duration', jobs_duration
  return (jobs_in, jobs_duration)

###############
# Main function
###############

if __name__ == '__main__':
  if len(sys.argv) < 8:
    print "Usage: %s sim_time(s) arrival_int_mean(s) job_duration_mean(s) filesize(N) machines(Nm) iter samples(M)" % (sys.argv[0])
    sys.exit(1)

  sim_time = int(sys.argv[1])
  arrival_int_mean = float(sys.argv[2])
  job_dur_mean = float(sys.argv[3])
  N = int(sys.argv[4])
  Nm = int(sys.argv[5])
  itera = int(sys.argv[6])
  M = int(sys.argv[7])

  if N < Nm:
    print "The file size should be larger than the number of servers"
    sys.exit(1)
  if M > N:
    print "The number of samples should be smaller than the number of blocks"
    sys.exit(1)

  accessed_blocks = defaultdict(lambda: 0)
  accessed_machs = defaultdict(lambda: 0)
  distinct_samples = defaultdict(lambda: 0)
  blks_sample = defaultdict(lambda: [])
  same_samples = 0
  wait_jobs = []
  
  machs_blks = alloc_blks_to_machs(N,Nm)
  #machs_state = [(k,0) for k in xrange(0,Nm)]

  for it in xrange(0, itera): #iterations
    machs_idle = machs_blks.keys()
    (jobs_in, jobs_duration) = possion(sim_time, arrival_int_mean, job_dur_mean)

    events = []
    for i in xrange(0, len(jobs_in)):
      events.append((jobs_in[i], 0, [], i))

    for e in events: #events [(time, type, machs, jobid)]
      #print 'an event', e
      if(e[1] == 0):
        job_id = e[3]
        if len(machs_idle) < M:
          machs_sample = [mach for mach in machs_idle]
          wait_jobs.append( [e[0], job_id, M-len(machs_idle)])
        else:
          machs_sample = sample(machs_idle, M)
        for mach in machs_sample:
          blk = choice(machs_blks[mach])
          blks_sample[job_id].append(blk)
          machs_idle.remove(mach); 
          accessed_machs[mach] += jobs_duration[job_id]
          accessed_blocks[blk] += jobs_duration[job_id]
        if len(machs_sample) == M:
          blks_sample[job_id].sort()
          distinct_samples[tuple(blks_sample[job_id])] += 1
        #add output events
        if len(machs_sample) > 0:
          #print 'add events (', e[0]+jobs_duration[job_id], 1, machs_sample, job_id, ')'
          events.append( (e[0]+jobs_duration[job_id], 1, machs_sample, job_id) )
          events.sort()

      elif e[1] == 1: #jobs_out
        machs_idle += e[2]
        while len(wait_jobs) > 0 and len(machs_idle) > 0:
          job_id = wait_jobs[0][1]
          machs_need = wait_jobs[0][2]
          if len(machs_idle) < machs_need:
            machs_sample = [mach for mach in  machs_idle]
            wait_jobs[0][2] -= len(machs_idle)
          else:
            machs_sample = sample(machs_idle, machs_need)
            del wait_jobs[0]
          for mach in machs_sample:
            blk = choice(machs_blks[mach])
            blks_sample[job_id].append(blk)
            machs_idle.remove(mach)  
            accessed_machs[mach] += jobs_duration[job_id]
            accessed_blocks[blk] += jobs_duration[job_id]
          if len(machs_sample) == machs_need:
            blks_sample[job_id].sort()
            distinct_samples[tuple(blks_sample[job_id])] += 1
          #add output events
          if len(machs_sample) > 0:
            #print 'add events (', e[0]+jobs_duration[job_id], 1, machs_sample, job_id, ')'
            events.append( (e[0]+jobs_duration[job_id], 1, machs_sample, job_id) )
            events.sort()
          
    #print 'distinct_samples', distinct_samples
    for v in distinct_samples.itervalues():
      if v > 1:
        same_samples += (v-1)
  
     
    print "#Iteration : ", it
    print "# Blocks Util"
    for block in xrange(0, N):
      print "%d %f"%(block, accessed_blocks[block])
    print "# Machines Util"
    for mach in xrange(0, Nm):
      print "%d %f"%(mach, accessed_machs[mach])
    print 'Number of times that two jobs select identical blks', same_samples
