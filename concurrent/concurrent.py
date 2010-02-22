# concurrent.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

@inlineCallbacks   # 1
def title(_):
     html = yield getPage( 'http://twistedmatrix.com' )            # 2 & 3 
     print fromstring( html ).xpath( '/html/head/title' )[0].text  # 4

@inlineCallbacks
def barrier():
     yield DeferredList( map( title, range(30) ) )  # 5 
     reactor.stop()                                 

reactor.run( barrier() )
