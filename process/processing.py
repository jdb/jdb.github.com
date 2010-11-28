
from multiprocessing import Process
from threading import Thread, Lock
from time import sleep
import sys

# bien comprendre:
#   difference entre thread et process
#   threaded cannot be terminated
#   difference entre C et Python (Exception !, and jvm)
#   test driven development
#   difference entre procedural et event driven
# should rewrite in C

# est-ce qu'un process termine si l' un des threads reste. En Python,
# c' est sur que thread qui reste pas bloquer la terminaison jusqu'a
# la terminaison du thread et son gc

# had to use the Popen instead of the more friendly multiprocessing
# because a multiprocessing does not crash, and the exception gets
# migrated accross virtual machines

# with multiprocessing, the namespaces spans the process/gets migrated
# accross virtual machines

# except: and except Exception: are not the same, the former gets
# executed in case of a sys.exit().

# sys.exit gets trapped by an except but not by a except Exception:
# sys.exit raises a kind of exception which is not an Exception

def terminate_on_timeout(p, delay=2):
    sleep(delay)
    if p.exitcode is None:
        p.terminate()

def clarify_exit_code(test):
    try:
        sys.exit(0 if test() else 2)
    except Exception:
        sys.exit(1)

if __name__=="__main__" and len(sys.argv)>1:

    mod = __import__(sys.argv[1])
    
    for test in mod.testfuns:
        print "Executing test: %20s \t" % (test.__name__,),

        p = Process(target=clarify_exit_code,    args=(test,))
        p.start()
    
        t = Thread( target=terminate_on_timeout, args=(p,))
        t.start()

        p.join()

        with Lock():
            if t.isAlive():
                del t   # hoping the prog can stop even though the thread
                        # is not terminated. A thread can not be stopped
                        # from outside without an inter thread communication

        if   p.exitcode==2:   print "unexpected"
        elif p.exitcode==0:   print "OK"       
        elif p.exitcode==1:   print "crashed"
        elif p.exitcode==-15: print "terminated"

 

