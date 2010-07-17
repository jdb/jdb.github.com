
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'
    d = None

    # callback executed by Twisted
    # ----------------------------
    def lineReceived(self, data):
        if self.d is None:    # if self.d does not hold a deferred,
            return            # no command has been sent, bail out:
                              # just ignore unexpected packets
        d, self.d = self.d, None
        d.callback(data)
        
    # internal method
    # ---------------
    def command(self, cmd):
        assert self.d is None
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    # public API
    # ----------
    def plizRandom(self,_): 
        def gotRandom(data):
            return int(data)
        return self.command("random").addCallback(gotRandom)

    # @defer.inlineCallbacks   # a variant using the inlineCallbacks
    # def plizRandom(self): 
    #     returnValue(int((yield self.command("random"))))

    # notification methods
    # --------------------
    def notifyMe(self,_): 
        def _notifyMe(_):
            self.d = defer.Deferred().addCallback(self.gotNotification)
            print "server accepted the notification mode"
            
        # self.timeout = reactor.callLater(29*60, self.notifyTimeout)
        print "Yoooooo, about to ask the notification"
        return self.command("notify").addCallback(_notifyMe)

    def stopNotify(self, _): 
        self.d = None
        return self.command("stop_notify")

    def gotNotification(self, notif):
        print notif
        reactor.stop()

    @defer.inlineCallbacks
    def notifyTimeout(self): 
        yield self.stopNotify(None)
        yield self.notifyMe(None)

#### End of the API
#### Beginning of the user code

@defer.inlineCallbacks
def gotConnection(conn):
    print (yield conn.plizRandom(None))
    while True:
        yield conn.notifyMe(None)


c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()
