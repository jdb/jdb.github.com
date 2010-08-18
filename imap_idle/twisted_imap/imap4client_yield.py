from getpass import getpass
from os import environ
from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email

def GetMailboxConnection(user, password, mailbox="inbox"):

    f = protocol.ClientFactory()
    f.user     = user
    f.password = password
    f.mailbox  = mailbox 

    class ConnectInbox(imap4.IMAP4Client):
        @defer.inlineCallbacks
        def serverGreeting(self, caps):

            del caps['STARTTLS'] # This is insecure, this is for debug
                                 # purpose: the password is sent in
                                 # plain text. Comment it in real use!

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

if __name__=="__main__":

    GetMailboxConnection(environ['USER'], getpass()
           ).addCallback(getSubjects)

    reactor.run()
