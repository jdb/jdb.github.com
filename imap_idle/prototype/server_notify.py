from twisted.internet import reactor, protocol
from twisted.protocols import basic
from random import randint

class NotifyProtocol(basic.LineReceiver):
    
    delimiter = '\n'

    def lineReceived(self, line):
        if line == "random":
            self.sendLine(str(randint(0, 1000)))
        elif line == "notify":
            self.sendLine("OK")
        elif line == "stop_notify":
            self.sendLine("OK")

f = protocol.ServerFactory()
f.protocol = NotifyProtocol
reactor.listenTCP(56789, f)
reactor.run()
