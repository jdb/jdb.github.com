
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):

    d = None

    def lineReceived(self, data):
        if data.startswith('notif:'):
            prefix, command = data.split()
            if command == 'random' and hasattr(self, 'randomAvailable'):
                self.randomAvailable()
            elif command == 'classified' and hasattr( 
                self, 'classifiedAvailable'):
                self.classifiedAvailable()
        else:
            if self.d is None:
                return 
            d, self.d = self.d, None
            d.callback(data)
        
    def command(self, cmd):
        assert self.d is None
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    # public API
    def random(self): 
        def gotRandom(number):
            return int(number)
        return self.command("random?").addCallback(gotRandom)

    def classified(self): 
        return self.command("classified?")

    def notify(self):
        return self.command("notif").addCallback(self.cbNotify)

    def cbNotify(self, response):
        assert response == 'OK'

    def stopNotify(self):
        return self.command("stop_notif").addCallback(self.cbNotify)

class HigherLevelClient(Client):
    @defer.inlineCallbacks
    def connectionMade(self):
        yield self.notify()

    @defer.inlineCallbacks
    def randomAvailable(self): 
        if not hasattr(self, 'randomReceived'):
            return

        yield self.stopNotify()
        self.randomReceived((yield self.random()))
        yield self.notify()

# End of the official upstream API

# Client script using the API
class MyClient(HigherLevelClient):
    def randomReceived(self, random): 
        print "Here is a random number", random
        
factory = protocol.ClientFactory()
factory.protocol = MyClient
reactor.connectTCP("localhost", 6789, factory)
reactor.run()
