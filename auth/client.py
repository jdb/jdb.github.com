from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import defer
from twisted.internet.protocol import Protocol
from twisted.internet.ssl import ClientContextFactory
from twisted.web.iweb import IBodyProducer

class BodyProducer(object):

    def __init__(self):
        self.body = 'Username=RobWilco&Password=BoojLu6Kal'
        self.length = len(self.body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class printer(Protocol):
    _buffer = ''
    def __init__(self, d, only_headers=False):
        self._d = d

    def dataReceived(self, bytes):
        self.buffer += bytes

    def connectionLost(self, reason):
        self._d.callback(self.buffer)


@defer.inlineCallbacks
def main():

    agent = Agent(reactor) #, ClientContextFactory())

    login_response = ( yield agent.request(
            'GET', 'https://lwn.net', None, BodyProducer()))

    print login_response.headers

    # cookie = login_response.headers['Set-cookie']

    # login_response = ( yield agent.request(
    #         'GET', 'https://lwn.net/login', None, BodyProducer()))

    # p = printer(defer.Deferred())
    # print response.deliverBody(p)
    # yield p.d

    reactor.stop()

main()
reactor.run()
