# sequential.py
from lxml.html import parse
from urllib2 import urlopen
from threading import Thread


def title(planet):
    # first Xpath pattern matches articles links, second pattern: html titles
    article = parse(urlopen(planet )).xpath('//h3/a/@href'    )[0]
    title   = parse(urlopen(article)).xpath('/html/head/title')[0].text

    print "first article on %s : \n%s\n%s\n\n" % (planet, article, title )

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

threads = [ Thread(target=title, args=(p,))for p in planets ]
for t in threads: t.start()
for t in threads: t.join()
