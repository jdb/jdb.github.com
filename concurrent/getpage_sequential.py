# getpage_sequential.py
from lxml.html import parse
from urllib2 import urlopen

getpage = lambda url : parse( urlopen( url ) )

# strip unneeded spaces and linefeeds
clean   = lambda s   : s.strip().split('\n')[0]

for planet in ["http://planet.debian.net",
               "http://planetzope.org",
               "http://planet.gnome.org",
               "http://gstreamer.freedesktop.org/planet/"]:

    # first pattern matches articles links, second pattern: html titles
    articles = getpage( planet      ).xpath( '//h3/a/@href'     )
    titles   = getpage( articles[0] ).xpath( '/html/head/title' )

    print "first article on %s : \n%s\n%s\n\n" % (
        planet,
        articles[0],
        clean( titles[0].text ) )
