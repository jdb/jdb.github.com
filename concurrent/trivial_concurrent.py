# trivial_concurrent.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

url = 'http://twistedmatrix.com'

@inlineCallbacks  
def title( url ):
     html = yield getPage( url )
     print fromstring( html ).xpath( '/html/head/title' )[0].text  

d = DeferredList([ title( url ) for i in range(30)]) 
d.addCallback( lambda _:reactor.stop() )

reactor.run()
