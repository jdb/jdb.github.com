from twisted.internet import reactor
from twisted.internet.defer import DeferredList,Deferred
from twisted.web.client import getPage
from lxml.html import fromstring

def first_url( url ): # returns an url

    d = getPage( url )

    def format_firsturl( html ):        
        articles = fromstring( html ).xpath( '//h3/a/@href' )
        return articles[0] if articles else None
    
    d.addCallback( format_firsturl )
    return d

def title( url ): # return a title
        
    d = getPage( url )

    def format_title( html ):
        titles = fromstring( html ).xpath( '/html/head/title' )
        clean = lambda s: s.strip().split('\n')[0]
        return clean( titles[0] ) if titles else None
    
    d.addCallback( format_title )
    return d

def chain( url ):

    """Chains the first_url and title asynchronous function, aggregate
    the results and displays the results"""

    ans = {}
    """A dictionnary which will store the information retrieved at the
    different steps of the callback chain"""

#     def memo( value, key ):
#         """the memo results in the value given as the first parameter
#         but stores the key and the value in a dictionary. It is used
#         in a callback chain to memorize the content which passes
#         through the callback chain.

#         The asynchronous functions first_url and title are *re-usable*
#         in the sense that they have no knowledge of how they are used,
#         the chain function is responsible for chaining them and for
#         displaying the result. memo is not mandatory, as title could
#         use a second argument which would be filled with the original
#         planet url and title would end up displaying the whole shebang.

#         Hurray for inlineCallbacks...
        
#         """
#         ans.set( key, value )
#         return Deferred().addCallback( lambda _: value )

    def memo(f,arg, key):
        ans.set(key,arg)
        return f, arg

    title = memo( title )

    def show( title ):
        print  "first article on %s : \n%s\n%s\n\n" % (
            url,
            ans.get( 'article', 'Not found' ),
            ans.get( 'title',   'Not found' ))

    d = first_url( url
          ).addCallback( title, 'article'
          ).addCallback( show)


    return d

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

DeferredList( map( chain, planets )).addCallback( lambda _: reactor.stop())
reactor.run()
