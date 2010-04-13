# trivial_deferred.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.web.client import getPage
from lxml.html import fromstring

url = 'http://twistedmatrix.com'

def print_title( html_string ):
    print fromstring( html_string ).xpath( '/html/head/title' )[0].text

DeferredList( 
        [ getPage( url ).addCallback(print_title) 
          for i in range(30) ]
        ).addCallback( lambda _:reactor.stop() )

reactor.run()
