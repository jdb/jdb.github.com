# concurrent.py 
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

planets = ["http://planet.debian.net",
           "http://planetzope.org",
           "http://planet.gnome.org",
           "http://gstreamer.freedesktop.org/planet/"]

@inlineCallbacks
def first_title(url):

    html = yield getPage(url)
    article = fromstring(html).xpath('//h3/a/@href')[0]

    html = yield getPage(article)
    title = fromstring(html).xpath('/html/head/title')[0].text

    print "first article on %s : \n%s\n%s\n\n" % (url, article, title)

for p in planets:
    first_title(p)

reactor.run() 
# Use Ctrl-C to terminate the script
