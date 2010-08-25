# trivial_deferred.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.web.client import getPage
from lxml.html import fromstring

url= 'http://twistedmatrix.com'

def getpage_callback(html):
    print fromstring(html).xpath( '/html/head/title' )[0].text

# 30 pending asynchronous network calls, and attachment of the callback
for i in range(30):
    getPage(url).addCallback(getpage_callback)


reactor.run()     # open the network connections, and fires the callbacks
                  # as soon as the replies are available

# Use Ctrl-C to terminate the script
