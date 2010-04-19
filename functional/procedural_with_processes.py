#!/usr/bin/env python
# procedural_with_processes.py

from random import uniform
from math import sqrt
import sys 
from multiprocessing import Process, Queue

n = int( sys.argv[1] )
numproc = 4

def pi(n):
    somme=0
    for i in xrange(n):
        if sqrt( uniform(-1,1)**2 + uniform(-1,1)**2 ) < 1:
            somme+=1
    return 4*float(somme)/n 


def processpool(func, *args):
    q = Queue()
    processes = [ Process(target=lambda _:q.put(func(_)),args=args) 
                  for i in range(numproc) ]

    for p in processes: p.start()
    for p in processes: p.join()  
    return [ q.get() for _ in range(q.qsize())]

subprocess_results = processpool(pi,n/numproc)

print "An approximation of Pi with 4 processes: %s" %(
    sum(subprocess_results)/len(subprocess_results))
