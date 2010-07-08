
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

    def ackNotif(self):
        return self.sendLine("got_notif")

    # public API
    # ----------
    def plizRandom(self,_): 
        def gotRandom(data):
            return int(data)
        return self.command("random").addCallback(gotRandom)

    # @defer.inlineCallbacks
    # def plizRandom(self): 
    #     returnValue(int((yield self.command("random"))))

    # notification methods
    # --------------------
    def notifyMe(self,_): 
        def _notifyMe(_):
            self.d = defer.Deferred().addCallback(self.gotNotification)
            self.notifDeferred = defer.Deferred()
        # self.timeout = reactor.callLater(29*60, self.notifyTimeout)
        return self.command("notify").addCallback(_notifyMe)

    def stopNotify(self): 
        def gotStopNotif(data):
            pass
        self.d = None
        return self.command("stop_notify").addCallback(gotStopNotif)

    def gotNotification(self, notif):
        self.ackNotif()
        self.d = None
        self.notifDeferred.callback(notif)

    @defer.inlineCallbacks
    def notifyTimeout(self): 
        yield self.stopNotify(None)
        yield self.notifyMe(None)

#### End of the API
#### Beginning of the user code

def notificationLoop(conn):
    # the notification loop, should be given a callback 
    return conn.stopNotify(
        ).addCallback( conn.
        ).addCallback( conn.notifyMe)


@defer.inlineCallbacks
def gotConnection(conn):
    print (yield conn.plizRandom(None))
    for i in conn.notification():
        print (yield conn.plizRandom(None)) 

c = protocol.ClientCreator(reactor, Client)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()
