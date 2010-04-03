# sequential.py
from lxml.html import parse
from urllib2 import urlopen

clean = lambda s: s.strip().split('\n')[0]
# strip unneeded spaces and linefeeds

for planet in ["http://planet.debian.net",
               "http://planetzope.org",
               "http://planet.gnome.org",
               "http://gstreamer.freedesktop.org/planet/"]:

    # first Xpath pattern matches articles links, second pattern: html titles
    articles = parse( urlopen( planet      )).xpath( '//h3/a/@href'     )
    titles   = parse( urlopen( articles[0] )).xpath( '/html/head/title' )

    print "first article on %s : \n%s\n%s\n\n" % (
        planet,
        articles[0],
        clean( titles[0].text ) )
