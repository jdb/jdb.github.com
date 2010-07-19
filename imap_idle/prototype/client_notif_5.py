
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):

    # callback executed by Twisted 
    def lineReceived(self, data):
        if data.startswith(self.notifPrefix):
            data = data.strip(self.notifPrefix)
            self.notif_d.callback(data)
        else:
            self.d.callback(data)
        
    # Internal/low level functions
    notifPrefix = "notif: "

    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    @defer.inlineCallbacks
    def waitNotif(self):
        self.notif_d = defer.Deferred()
        notif = yield self.notif_d
        self.sendLine("OK")
        defer.returnValue(notif)
        
    def notif(self):
        return self.command("_notif_")

    def stopNotif(self):
        self.notif_d = None
        return self.command("_stop_notif_")

    # user API
    def random(self):
        return self.command("random?"
                  ).addCallback(lambda x:int(x))

    def classified(self):
        return self.command("classified?")

    infos = {"random":("random",random),
             "classified":("classified", classified)}
    
    @defer.inlineCallbacks
    def receive(self, item):

        pattern, getter = self.infos[item] 
        
        while True:
            notif = (yield self.waitNotif())
            print "notif:", notif
            if notif==pattern:
                break

        yield self.stopNotif()
        data = (yield getter(self))
        
        self.notif()
        defer.returnValue(data)

@defer.inlineCallbacks
def gotConnection(conn):

    print (yield conn.random())
    print (yield conn.classified())        
    
    yield conn.notif()
    while True:
        print (yield conn.receive("random"))
        
c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()



