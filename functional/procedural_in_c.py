#!/usr/bin/env python
# procedural_with_processes_in_c.py


import sys 
from multiprocessing import Process, Queue

n = int( sys.argv[1] )
numproc = 4

def processpool(func, *args):
    q = Queue()
    processes = [ Process(target=lambda _:q.put(func(_)),args=args) 
                  for i in range(numproc) ]

    for p in processes: p.start()
    for p in processes: p.join()  
    return [ q.get() for _ in range(q.qsize())]

from pi import pi

subprocess_results = processpool(pi,n/numproc)

print "An approximation of Pi with 4 processes: %s" %(
    sum(subprocess_results)/len(subprocess_results))
