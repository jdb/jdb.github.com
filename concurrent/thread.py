from threading import Thread, Lock

counter = [0]

def incr(counter):
    for i in range(1000):
        counter[0]+=1 

def execute(func, args):
    threads=[]
    for i in range(100):
        threads.append(Thread(target=incr, args=args))
    [ t.start() for t in threads]
    [ t.join()  for t in threads]

execute(incr, (counter))

print counter[0]



from threading import Lock

counter, lock =  [0], Lock()
def safe_incr(counter, lock):
    for i in range(1000):
        with lock:
            counter[0]+=1 


execute(safe_incr, (counter,lock))
print counter[0]
