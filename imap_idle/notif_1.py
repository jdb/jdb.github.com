
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'

    @defer.inlineCallbacks
    def connectionMade(self):
        print (yield self.plizRandom(None))
        print (yield self.plizClassified(None))
        reactor.stop()

    def lineReceived(self, data):
        self.d.callback(data)
        
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    def plizRandom(self,_): 
        def gotRandom(number):
            return int(number)
        return self.command("random?").addCallback(gotRandom)

    def plizClassified(self,_): 
        return self.command("classified?")


factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()
