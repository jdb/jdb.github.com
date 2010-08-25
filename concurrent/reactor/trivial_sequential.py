# trivial_sequential.py
from lxml.html import parse
from urllib2 import urlopen

url = 'http://twistedmatrix.com' 

def title(url):
    html = urlopen(url)
    print parse(html).xpath('/html/head/title')[0].text

for i in range(30): 
    title(url) 
