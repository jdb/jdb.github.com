from multiprocessing import Process

def incr():
    print "Hello world"

processes = [ Process(target=incr) for i in range(100) ]

[ p.start() for p in processes]
[ p.join()  for p in processes]


