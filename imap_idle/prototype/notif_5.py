
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'
    forever = True

    # Twisted callback
    def lineReceived(self, data):
        self.d.callback(data)
        
    # Internal function
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d
    
    # user API
    def waitNotif(self):
        self.d = defer.Deferred()
        return self.d            

    def random(self):
        return self.command("random?")

    def classified(self):
        return self.command("classified?")

    def notifMode(self,state=True):
        if state==True:
            return self.command("_notif_")
        elif:
            return self.command("_stop_notif_")

@defer.inlineCallbacks
def gotConnection(conn):

    print int((yield conn.random()))
    print (yield conn.classified()))        
    print (yield conn.notifMode()) 

    while conn.forever:
        notif = (yield conn.waitNotif())
        print "Hey, got a notif:", notif
        if notif=="classified":
            print "Oh an ad, not interested"
        elif notif=="random":
            print (yield conn.notifMode(False)) 
            print int((yield conn.random()))
            print (yield conn.notifMode()) 
        elif notif=="end":
            conn.forever = False
            
    reactor.stop()
        
c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()

