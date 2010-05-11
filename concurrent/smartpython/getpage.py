from twisted.internet import defer, reactor
from twisted.web.client import getPage
from lxml.html import fromstring


@defer.inlineCallbacks
def title(url):
    print fromstring((yield getPage(url))).xpath('/html/head/title')[0].text
    reactor.stop()

reactor.run(title('http://twistedmatrix.com'))


