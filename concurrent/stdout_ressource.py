#from multiprocessing import Process as Task, Lock
from threading import Thread as Task, Lock
import sys

lock = Lock()

def incr():
    for i in xrange(1000):
        with lock:
            print "Hello world"


tasks = [ Task(target=incr) for i in range(100) ]

for t in tasks: t.start() 
for t in tasks: t.join()  


