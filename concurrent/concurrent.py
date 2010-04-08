# concurrent.py 
from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

@inlineCallbacks
def first_title( url ):

    html = yield getPage( url )
    article = fromstring( html ).xpath( '//h3/a/@href' )[0]

    html = yield getPage( article )
    title = fromstring( html ).xpath( '/html/head/title' )[0].text

    print "first article on %s : \n%s\n%s\n\n" % (
            url, article, title )

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

DeferredList( [ first_title( p ) for _ in planets ] )
d.addCallback( lambda _:reactor.stop() )

reactor.run() 

