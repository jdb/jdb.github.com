# concurrent.py 
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

dig = lambda html,pattern: fromstring(html).xpath(pattern)[0]

@inlineCallbacks
def first_title(url):
    article = dig( (yield getPage(url)),     '//h3/a/@href')
    title   = dig( (yield getPage(article)), '/html/head/title').text

    print "first article on %s : \n%s\n%s\n\n" % (url, article, title)

for planet in planets:
    first_title(planet)

reactor.run() 
# Use Ctrl-C to terminate the script
