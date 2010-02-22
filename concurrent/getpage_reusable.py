from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallback, returnValue
from twisted.web.client import getPage
from lxml.html import fromstring

@inlineCallback
def first_url( url ): 
    html = yield getPage( url )
    articles = fromstring( html ).xpath( '//h3/a/@href' )
    returnValue( articles[0] if articles else None )

@inlineCallback
def title( url ):
    html = yield getPage( url )
    titles = fromstring( html ).xpath( '/html/head/title' )
    clean = lambda s: s.strip().split('\n')[0]
    returnValue( clean( titles[0] ) if titles else None )

@inlineCallback
def chain( url ):

    ans={}
    ans['article'] = yield first_url( url )
    ans['title']   = yield title( ans['article'] )

    print  "first article on %s : \n%s\n%s\n\n" % (
            url,
            ans.get( 'article', 'Not found' ),
            ans.get( 'title',   'Not found' ))

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

DeferredList( map( chain, planets )).addCallback( lambda _: reactor.stop())
reactor.run() 
