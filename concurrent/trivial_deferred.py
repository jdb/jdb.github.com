# trivial_deferred.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.web.client import getPage
from lxml.html import fromstring

url= 'http://twistedmatrix.com'

def title( url ):
    d = getPage( url )

    def cbGetPage( html_string ):
        print fromstring( html_string ).xpath( '/html/head/title' )[0].text

    d.addCallback( cbGetPage )    
    return d

DeferredList( 
    [ title( url ) for _ in range(30) ]
  ).addCallback( lambda _:reactor.stop() )

reactor.run()
