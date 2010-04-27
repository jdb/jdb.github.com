# trivial_threaded.py
from lxml.html import parse
from urllib2 import urlopen
from threading import Thread

def title(url='http://twistedmatrix.com'):
    print parse(urlopen(url)).xpath('/html/head/title')[0].text

# let's download the page 30 times in 30 threads

threads = [ Thread(target=title) for i in range(30) ] 
for t in threads: t.start()
for t in threads: t.join()
