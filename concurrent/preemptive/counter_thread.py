from threading import Thread, Lock
from timeit import Timer
from time import time as now
from twisted.internet.defer import Deferred



chrono = lambda f: Timer(lambda :execute(f)).timeit(number=10)

def execute(f):
    threads = [ Thread(target=f) for i in range(100)]
    for t in threads: t.start()
    for t in threads: t.join()


def incr(_=None):
    global counter
    for i in range(10000):
        counter+=1 


def safe_incr():
    global counter, lock
    for i in range(10000):
        with lock:
            counter+=1 


counter = 0
no_lock = chrono(execute(incr))
print "threaded, no lock", no_lock, counter

counter, lock =  0, Lock()
locked = chrono(execute(safe_incr))
print "threaded, locked ", locked, counter


def request():
    return Deferred()

counter, start = 0, now()
deferreds = [request().addCallback(incr) for i in xrange(100)] 

# There is a hundred concurrent pending actions at this point ...

# ... fire NOW !
for d in deferreds:
    d.callback(None)

elapsed = now() - start 

print "deferred, locked ", 10 * elapsed, counter



