# sequential.py
from lxml.html import parse
from urllib2 import urlopen

for i in xrange( 30 ):
    fd = urlopen( 'http://twistedmatrix.com' )
    print parse( fd ).xpath( '/html/head/title' )[0].text


