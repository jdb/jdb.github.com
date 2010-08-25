# threaded.py
from lxml.html import parse
from urllib2 import urlopen
from threading import Thread

dig = lambda html,pattern: parse(html).xpath(pattern)[0]

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

def first_title(url):

    # first Xpath pattern matches articles links, second pattern: html titles
    article = dig( urlopen(url ), '//h3/a/@href'    )
    title   = dig( urlopen(article), '/html/head/title').text

    print "first article on %s : \n%s\n%s\n\n" % (url, article, title )


threads = [ Thread(target=first_title, args=(p,)) for p in planets ]
for t in threads: t.start()
for t in threads: t.join()
