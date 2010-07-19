
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    def lineReceived(self, data):
        if data.startswith('notif: '):
            self.d_notif.callback(data)
        else:
            self.d.callback(data)
        
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d
    
    def waitNotif(self):
        self.notif_d = defer.Deferred()
        return self.notif_d            

@defer.inlineCallbacks
def gotConnection(conn):

    print int((yield conn.command("random?")))
    print (yield conn.command("classified?"))        
    print (yield conn.command("_notif_")) 

    while True:
        notif = (yield conn.waitNotif())
        print "Hey, got a notif:", notif
        if notif=="classified":
            print "Oh an ad, not interested"
        elif notif=="random":
            conn.sendLine("stop_notif")
            print (yield conn.d)
            print int((yield conn.command("random?")))
            print (yield conn.command("notif")) 

c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()

