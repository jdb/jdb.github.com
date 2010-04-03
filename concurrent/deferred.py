# deferred.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList
from twisted.web.client import getPage
from lxml.html import fromstring

def first_url( url ): # returns the first href of the page at this url

    d = getPage( url )

    def format_firsturl( html ):        
        articles = fromstring( html ).xpath( '//h3/a/@href' )
        return articles[0] if articles else None
    
    d.addCallback( format_firsturl )
    return d

def title( url ): # return the title of the page at this url
    
    d = getPage( url )

    def format_title( html ):
        titles = fromstring( html ).xpath( '/html/head/title' )
        clean = lambda s: s.strip().split('\n')[0]
        return clean( titles[0].text ) if titles else None
    
    d.addCallback( format_title )
    return d

def show( title ):
    print title

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

DeferredList( [ first_url( p
                     ).addCallback( title 
                     ).addCallback( show)
                for p in planets]
     ).addCallback( lambda _: reactor.stop())

reactor.run()
