
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

def map_blk_to_mach(blk, machs_blks):
  res = [mach for mach, blks in machs_blks.items() if blk in blks]
  return res[0]

def alloc_slots_to_machs(Ns, Nm):
  return alloc_blks_to_machs(Ns, Nm)

def map_slot_to_mach(slot, machs_slots):
  return map_blk_to_mach(slot, machs_slots)

def select_block(mach_blocks, blks_sampled, N):
  non_local = 0
  local_blks_free = filter(lambda x: x not in blks_sampled, mach_blocks)
  if len(local_blks_free) > 0:
    blk = choice(local_blks_free)
  else: #Find a blk on the other mechs
    print 'NON Access'
    global_blks_free = filter(lambda x: x not in blks_sampled, xrange(0, N))
    non_local = 1
    blk = choice(global_blks_free)
  
  return (blk, non_local)  
    

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
  print 'jobs_in', jobs_in
  print 'duration', jobs_duration
  return (jobs_in, jobs_duration)

