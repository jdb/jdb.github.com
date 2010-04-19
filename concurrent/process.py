from multiprocessing import Process, Queue, JoinableQueue

counter, queue = Queue(), JoinableQueue()
counter.put(0)

def incr(queue):
    for i in range(100):
        queue.put(1)

def reduce(counter,queue):
    while True:
        if queue.get()==1:
            counter.put(1+counter.get())
        else:
            return
        

processes = [ Process(target=incr,args=(queue,)) for i in range(100)] 
r = Process(target=reduce,args=(counter,queue))

[ p.start() for p in processes +[r] ]
[ p.join()  for p in processes ] 
queue.join()
r.terminate()

print counter.get()

