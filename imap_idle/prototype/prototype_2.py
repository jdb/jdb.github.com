
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    # Internal
    def lineReceived(self, data):
        if data.startswith('notif: '):
            self.d_notif.callback(data)
        else:
            self.d.callback(data)
        
    def command(self, cmd):
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

    def notify(self,notifCallback):
        def _cbNotify(response, notifCallback):
            print "about the notification request, server said:", response
            
        self.d_notif = defer.Deferred().addCallback(notifCallback)
        return self.command("notif").addCallback(_notifyMe, notifCallback)

    def stopNotify(self, _):
        self.d_notif = None
        self.sendLine("stop_notif")
        return self.d

    # User code, this is actually the main()
    @defer.inlineCallbacks
    def gotConnection(self):
        print (yield self.random())
        print (yield self.classified())        
        print (yield self.notify(gotNotification))

    def gotNotification(notif, conn):
        print "a notif:", notif
        self.d_notif = defer.Deferred().addCallback(gotNotification)
        print "ready for a new notif" 

factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()
