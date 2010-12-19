#!/usr/bin/env python
# procedural_with_processes.py

from random import uniform
from math import sqrt
import sys 

def pi(n):
    somme=0
    for i in xrange(n):
        if sqrt( uniform(-1,1)**2 + uniform(-1,1)**2 ) < 1:
            somme+=1
    return 4*float(somme)/n 

n = int( sys.argv[1] )

from multiprocessing import Process, Queue
processes, q, numproc = (), Queue(), 4
for _ in range(numproc):
    processes.append(Process(target = lambda n:q.put(pi(n)),
                             args   = (n/numproc,))) 

for p in processes: p.start()
for p in processes: p.join()  
subprocess_results = [ q.get() for _ in range(q.qsize())]

print "with 4 processes, Pi = %s" %(
    sum(subprocess_results)/len(subprocess_results))
