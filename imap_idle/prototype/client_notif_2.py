
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    # Internal
    def lineReceived(self, data):
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

    waiting_notif = False

    def waitNotif(self):
        def cbWaitNotif(data):
            self.waitingNotif = False if data == 'OK' else True
            self.d.callback(data)
            
        self.notif_d = defer.Deferred()
        self.waitingNotif =True
        return self.notif_d

    def notify(self, notifCallback):
        def _cbNotify(data, notifCallback ):
            notifCallback(data)
        self.waiting
        return self.command("notif").addCallback(_cbNotify, notifCallback)

    def stopNotify(self, _):
        return self.command("stop_notif")

    # User code, this is actually the main()
    @defer.inlineCallbacks
    def gotConnection(self):
        print (yield self.random())
        print (yield self.classified())        
        print (yield self.notify(gotNotification))
        gotNotification((yield self.waitNotif()))
        gotNotification((yield self.waitNotif()))
        gotNotification((yield self.waitNotif()))

    def gotNotification(notif):
        print "a notif:", notif

factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()
