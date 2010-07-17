
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

    def waitNotif(self):
        self.notif_d = defer.Deferred()
        return self.notif_d            

    def notify(self,notifCallback):
        self.waitNotif().addCallback(notifCallback)

        def _cbNotify(_):
            print "Notification mode completed, back to client/server"
        return self.command("notif").addCallback(_cbNotify)

    def stopNotify(self, _):
        self.d_notif = None
        self.sendLine("stop_notif")
        return self.d

    # User code, this is actually the main()
    @defer.inlfineCallbacks
    def gotConnection(self):
        print (yield self.random())
        print (yield self.classified())        
        print (yield self.notify(gotNotification))

    @defer.inlineCallbacks
    def gotNotification(notif, conn):
        print "a notif:", notif
        if notif=='notif: random':
            yield self.stopNotify()
            print (yield self.random())
            yield self.notify()

        self.d_notif.addCallback(gotNotification)
        print "ready for a new notif" 

factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()
