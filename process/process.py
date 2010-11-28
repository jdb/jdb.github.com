
from subprocess import Popen
from threading import Thread
from time import sleep
import sys

def terminate_on_timeout_if_still_exists(sub, delay=2):
    sleep(delay)
    if sub.returncode is None:
        sub.terminate()


def sub_process_with_timeout(mod, function):

    script = """
import %s
import sys  
sys.exit(0 if int(%s.%s()) else 2)""" 

    sub = Popen([ 'python', '-c', script % (mod, mod, function)], 
                stderr=file("/dev/null"))
    
    Thread( target=terminate_on_timeout_if_still_exists, args=(sub,)
           ).start()
    
    sub.wait()
    ret = sub.returncode
    if   ret==2:   print "unexpected"
    elif ret==0:   print "OK"       
    elif ret==1:   print "crashed"
    elif ret==-15: print "terminated"


if __name__=="__main__" and len(sys.argv)>1:

    mod = __import__(sys.argv[1])
    
    for test in mod.tests:
        print "Executing test: %20s \t" % (test,),
        sub_process_with_timeout(sys.argv[1], test)
 

