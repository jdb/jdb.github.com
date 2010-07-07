
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'

    # called by the main loop

    @defer.inlineCallbacks
    def connectionMade(self):
        print (yield self.plizRandom())
#        print (yield self.plizRecent())
        print (yield self.notifyMe())
        
    def lineReceived(self, data):
        d, self.d = self.d, None
        d.callback(data)
        

    # called by the user
        
    def plizRandom(self): 

        def _gotRandom(data):
            return int(data)

        self.d = defer.Deferred().addCallback(_gotRandom)
        self.sendLine("random, pliz?")
        return self.d


    def notifyMe(self): 

        def _gotNotif(data):
            assert data=='OK'
            print "entering idle state"
            self.d = defer.Deferred().addCallback(self.gotNotification)

        self.sendLine("would you notify me?")
        self.d = defer.Deferred().addCallback(_gotNotif)
        return self.d

    def gotNotification(self, notif):

        def _stopNotif(data):
            assert data=='OK'
            print "exiting idle state"
            self.plizRandom()

        self.sendLine("stop notifying me, OK?")
        self.d = defer.Deferred().addCallback(_stopNotif)
    
factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()
