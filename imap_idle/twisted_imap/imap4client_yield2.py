
from getpass import getpass
from os import environ
from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email

class IMAP4ClientWithIDLE():
    
    def idle(self):
        cmd = STATUS
        args = None
        resps = ('EXISTS', 'EXPUNGE')  # any command actually

        # idle defines here (every time the command is called O_o)
        # the possible functions

        resp = ()


    def __cbIdle(self):
        pass

    # I just discovered in rfc3501 that DONE is not a 

    def done(self):
        pass

    def __cbDone(self):
        pass


def GetMailboxConnection(user=environ['USER'], mailbox="inbox"):

    f = protocol.ClientFactory()
    f.user     = user
    f.password = getpass()
    f.mailbox  = mailbox 

    class ConnectInbox(imap4.IMAP4Client):
        @defer.inlineCallbacks
        def serverGreeting(self, caps):

            del caps['STARTTLS'] # This is insecure, this is for debug purpose
                                 # password is sent in plain text. Comment it!
            yield self.login(self.factory.user, self.factory.password)
            yield self.examine(self.factory.mailbox)
            self.factory.deferred.callback(self)

    f.protocol = ConnectInbox
    reactor.connectTCP('localhost', 143, f)
    # reactor.connectSSL('localhost', 143, f, ssl.ClientContextFactory())

    f.deferred = defer.Deferred()
    return f.deferred
        
@defer.inlineCallbacks
def getSubjects(conn):

    messages = ( yield conn.fetchSpecific('1:*', 
                                          headerType = 'HEADER.FIELDS',
                                          headerArgs = ['SUBJECT']))
    for num, msg in messages.items():
        print num, msg[0][2]
        
    return conn

@defer.inlineCallbacks
def receiveNewMailsFrom(conn, mailFrom):
    
    yield conn.idle()
    while True:

        notif = (yield self.waitNotif())
        yield self.stopNotif()
        data = (yield getter(self))
        
        conn.idle()
        print data

# Need to set a nice sig15 handler which cancels the proto deferreds,
# logs out and stop the reactor

if __name__=="__main__":

    # configure a search pattern

    GetMailboxConnection(
        ).addCallback(getSubjects, pattern
        ).addCallback(receiveNotifs, pattern)

    reactor.run()
