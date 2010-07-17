
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'
    forever = True

    def lineReceived(self, data):
        self.d.callback(data)
        
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d
    
    def waitNotif(self):
        self.d = defer.Deferred()
        return self.d            

@defer.inlineCallbacks
def gotConnection(conn):

    print int((yield conn.command("random?")))
    print (yield conn.command("classified?"))        
    print (yield conn.command("_notif_")) 

    while conn.forever:
        notif = (yield conn.waitNotif())
        print "Hey, got a notif:", notif
        if notif=="classified":
            print "Oh an ad, not interested"
        elif notif=="random":
            print (yield conn.command("_stop_notif_")) 
            print int((yield conn.command("random?")))
            print (yield conn.command("_notif_")) 
        elif notif=="end":
            conn.forever = False

    reactor.stop()
        
c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()

