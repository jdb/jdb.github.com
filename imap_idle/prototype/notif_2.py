
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'

    # Internal
    def lineReceived(self, data):
        self.d.callback(data)
        
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    # API
    def plizRandom(self): 
        def gotRandom(number):
            return int(number)
        return self.command("random?").addCallback(gotRandom)

    def plizClassified(self): 
        return self.command("classified?")

    def notifyMe(self,notifCallback):
        def _notifyMe(response, notifCallback):
            print "about the notification request, server said ", response
            self.d = defer.Deferred().addCallback(notifCallback)
            return self.d
            
        return self.command("_notif_").addCallback(_notifyMe, notifCallback)

    def stopNotify(self, _):
        def _stopNotify(_):
            self.d = None
        return self.command("_stop_notif_").addCallback(_stopNotify)

def gotNotification(notif, conn):
    print "a notif:", notif
    conn.d = defer.Deferred().addCallback(gotNotification, conn)
    print "ready for a new notif" 

@defer.inlineCallbacks
def gotConnection(conn):
    print (yield conn.plizRandom())
    print (yield conn.plizClassified())        
    print (yield conn.notifyMe(conn.gotNotification) )

            
c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()

