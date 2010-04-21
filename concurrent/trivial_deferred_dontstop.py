# trivial_deferred.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.web.client import getPage
from lxml.html import fromstring

url= 'http://twistedmatrix.com'

def getpage_callback( html_string ):
    print fromstring( html_string ).xpath( '/html/head/title' )[0].text

# 30 asynchronous network calls, and attachment of the callback
[ getPage( url ).addCallback( getpage_callback ) for i in range(30) ]
                  # why a list comprehension? 
                  # this will be clarified below ...

reactor.run()     # open the network connections, and fires the callbacks
                  # as soon as the replies are available
