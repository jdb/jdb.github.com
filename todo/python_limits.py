
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic
from twisted.python.failure import Failure

# this short code illustrates the uselessness of several Python
# primitives in the context of asynchronous programming: 
# - for loop, yield and co
# - context manager 
# - exception

class Notif(basic.LineReceiver):
    
    def lineReceived(self, data):
        self.d.callback(data)

    def __iter__(self):
        return self

    def entercontext(self):
        self.factory.transport.write('unset notifmode')

    def exitcontext(self): # enter and exit smells like a context mangager
        self.factory.transport.write('set notifmode')

    @defer.inlineCallbacks
    def next(self):
        
        yield self.entercontext()
        self.d = defer.Deferred()
        notif = yield self.d
        self.exitcontext().addErrback(lambda _.reactor.stop())

        if notif=="stop":   # exception can't be raised in inlineCallbacks
            defer.returnValue(Failure(StopIteration()))
        else:
            defer.returnValue(notif)
            
@defer.inlineCallbacks
def gotConnection(conn):

    conn.factory.transport.write('set notifmode')
    while True:   # This loop looks almost like a for loop, but it is not
        try:
            print (yield conn.next()) 
        except StopIteration:
            break
    
    reactor.stop()
        
c = protocol.ClientCreator(reactor, Notif)
c.connectTCP("localhost", 6789).addCallback(gotConnection)
reactor.run()

