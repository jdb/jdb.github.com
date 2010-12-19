#!/usr/bin/env python
# procedural_with_processes_in_c.py


import sys 
from multiprocessing import Process, Queue
from pi import pi
n = int( sys.argv[1] )
numproc = 4

q = Queue()
processes = [Process(target=lambda n:q.put(pi(n)),args=n/4) 
             for i in range(numproc)]

for p in processes: p.start()
for p in processes: p.join()  
subprocess_results = [q.get() for _ in range(q.qsize())]

print "An approximation of Pi with 4 processes: %s" %(
    sum(subprocess_results)/len(subprocess_results))
