# concurrent.py 
from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

@inlineCallbacks
def first_title(url):

    dig = lambda html,pattern: fromstring(html).xpath(pattern)[0]

    article = dig( (yield getPage(url)), '//h3/a/@href')
    title =   dig( (yield getPage(article)), '/html/head/title').text

    print "first article on %s : \n%s\n%s\n\n" % (url, article, title)


d = DeferredList([first_title( p ) for p in planets])
d.addCallback(lambda _:reactor.stop())

reactor.run() 
