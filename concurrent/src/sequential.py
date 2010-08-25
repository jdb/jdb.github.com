# sequential.py
from urllib2 import urlopen
from lxml.html import parse

dig = lambda html,pattern: parse(html).xpath(pattern)[0]
"takes a html page and a xpath pattern, returns the first matching node"

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

def first_title(url):

    # first Xpath pattern matches articles links, second pattern: html titles
    article = dig( urlopen(planet ), '//h3/a/@href'    )
    title   = dig( urlopen(article), '/html/head/title').text

    print "first article on %s : \n%s\n%s\n\n" % (planet, article, title )


for planet in planets:
    first_title(planet)
