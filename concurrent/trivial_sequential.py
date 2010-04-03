# trivial_sequential.py
from lxml.html import parse
from urllib2 import urlopen

url = 'http://twistedmatrix.com' 

def title( url ):
    print parse( urlopen( url )).xpath( '/html/head/title' )[0].text

[ title(url) for _ in range(30) ]
