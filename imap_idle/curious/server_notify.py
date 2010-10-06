from twisted.internet import reactor, protocol
from twisted.protocols import basic
from random import randint

class NotifyProtocol(basic.LineReceiver):
    
    notifMode = False

    def lineReceived(self, line):
        print line
        if line == "random?":
            self.sendLine(str(randint(0, 1000)))
        if line == "classified?":
            self.sendLine("Flat to rent in the %se" % str(randint(1, 20)))
        elif line == "notif":
            self.sendLine("OK")
            self.notifMode = reactor.callLater(randint(1,5),self.notifs)
        elif line == "stop_notif":
            self.notifMode.cancel()
            self.notifMode = False
            self.sendLine("OK")

    def notifs(self):
        print "send a notif"
        self.sendLine("notif: random")
        self.notifMode = reactor.callLater(randint(1,5), self.notifs)

f = protocol.ServerFactory()
f.protocol = NotifyProtocol
reactor.listenTCP(6789, f)
reactor.run()
