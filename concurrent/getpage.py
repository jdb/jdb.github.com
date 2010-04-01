from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

clean = lambda s: s.strip().split('\n')[0]

@inlineCallbacks
def first_title( url ):

    html = yield getPage( url )
    articles = fromstring( html ).xpath( '//h3/a/@href' )

    html = yield getPage( articles[0] )
    titles = fromstring( html ).xpath( '/html/head/title' )

    print "first article on %s : \n%s\n%s\n\n" % (
            url,
            articles[0],
            clean ( titles[0].text ))

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

DeferredList( [ first_title(p) for p in planets] 
              ).addCallback(lambda _:reactor.stop()) 

reactor.run() 

