# sequential.py
from lxml.html import parse
from urllib2 import urlopen

for planet in ["http://planet.debian.net",
               "http://planetzope.org",
               "http://planet.gnome.org",
               "http://gstreamer.freedesktop.org/planet/"]:

    # first Xpath pattern matches articles links, second pattern: html titles
    article = parse(urlopen(planet )).xpath('//h3/a/@href'    )[0]
    title   = parse(urlopen(article)).xpath('/html/head/title')[0].text

    print "first article on %s : \n%s\n%s\n\n" % (planet, article, title )
