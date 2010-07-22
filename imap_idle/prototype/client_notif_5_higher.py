
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

    def notify(self):
        return self.command("notif")

    def waitNotif(self):
        self.d = defer.Deferred()
        return self.d

    def stopNotify(self):
        self.sendLine("stop_notif")
        self.d = defer.Deferred()
        return self.d

    infos = {"random"     : ("notif: random",random),
             "classified" : ("notif: classified", classified)}
    
    @defer.inlineCallbacks
    def receive(self, item):

        pattern, getter = self.infos[item] 
        
        yield self.notify()
        notif = (yield self.waitNotif())
        while notif!=pattern:
            notif = (yield self.waitNotif())

        yield self.stopNotify()
        defer.returnValue((yield getter(self)))

# End of the official upstream API

# Client script using the API
@defer.inlineCallbacks
def gotConnection(conn):

    print (yield conn.random())
    print (yield conn.classified())        
    
    while True:
        print (yield conn.receive("random"))
            
c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()

