
from getpass import getpass
from os import environ
from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email

class IMAP4ClientWithIDLE(imap4.IMAP4Client):
    """
    Extension to the imap4.IMAP4Client class with support for the IDLE
    command. Code meant to be merge to in twisted.mail.imap4.IMAP4Client

    """
    
    # TODO: virer le callback pour lapremiere notif
    # regarder les caps

    self.idling = None

    def _defaultHandler(self, tag, rest):
        if tag == '*' or tag == '+':
            if not self.waiting or self.idling:
                self._extraInfo([parseNestedParens(rest)])
            else:
                cmd = self.tags[self.waiting]
                if tag == '+':
                    cmd.continuation(rest)
                else:
                    cmd.lines.append(rest)
        else:
            try:
                cmd = self.tags[tag]
            except KeyError:
                # XXX - This is rude.
                self.transport.loseConnection()
                raise IllegalServerResponse(tag + ' ' + rest)
            else:
                status, line = rest.split(None, 1)
                if status == 'OK':
                    # Give them this last line, too
                    cmd.finish(rest, self._extraInfo)
                else:
                    cmd.defer.errback(IMAP4Exception(line))
                del self.tags[tag]
                self.waiting = None
                self._flushQueue()


    def idle(self, ):

        self.idling = True

        resp = ('EXISTS', 'EXPUNGE')
        noop = lambda _: None
        cmd = Command('IDLE', None, wantResponse=resp, continuation=noop)
        return ( self.sendCommand(cmd)
                 .addCallback(self._cbIdle) )

    def _cbIdle(self, (lines, last)):
        self.idling = None

    def done(self):
        self.sendLine('DONE')
        return self._lastCmd.defer


class ConnectInbox(imap4.IMAP4ClientWithNotif):
    @defer.inlineCallbacks
    def serverGreeting(self, caps):

        yield self.login(self.factory.user, self.factory.password)
        yield self.examine(self.factory.mailbox)
        self.idle()         


def GetMailboxConnection(user=environ['USER'], mailbox="inbox", host='localhost'):

    f = protocol.ClientFactory()
    f.user     = user
    f.password = getpass()
    f.mailbox  = mailbox 
    f.host     = host


    f.protocol = ConnectInbox
    reactor.connectTCP(host, 143, f)
    # reactor.connectSSL('localhost', 143, f, ssl.ClientContextFactory())

    f.deferred = defer.Deferred()
    return f.deferred
        

# User code
@defer.inlineCallbacks
def getNewApparts(conn):

    messages = ( yield conn.fetchSpecific('1:*', 
                                          headerType = 'HEADER.FIELDS',
                                          headerArgs = ['SUBJECT']))

    new_apparts = [ num for num, msg in messages.items() 
                    if msg[0][2] == 'PAP' or msg[0][2] == 'seloger.com' ]

    msgSet = MessageSet()
    for num in new_apparts:
        msgSet.add(num)

    
    messages = ( yield conn.fetchSpecific(msgSet,  
                                          headerType = 'HEADER.FIELDS',
                                          headerArgs = ['SUBJECT']))

    # Needs the body and the function that parses PAP and seloger.com
            
    notify(messages)
        
    def newMessages(self, exists, recent):
        
        conn

    defer.returnValue(conn)

# J'ai besoin d'une fonction qui prend une connexion en entree et
# check les unread mail pour voir si il n'y a pas de nouveaux mails de pap et se loger
# si oui, alors il 


# J'ai besoin d'une autre fonction qui prend une connexion en Idle et quand 


def getReceivedNewAppartsOnIdle(conn):
    yield conn.done()
    yield getNewClassifiedAds(conn)
    yield conn.idle()
    

@defer.inlineCallbacks
def getReceivedNewApparts(conn):
    pass
            
( GetMailboxConnection(newMessages = getReceivedNewAppartsOnIdle)
  .addCallback(getNewClassifiedAds)
  .addCallback(lambda conn:conn.idle()))

reactor.run()
