
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

    def idle(self, ):
        """
        Request the notifications of new mails

        This command is allowed in the Authenticated and Selected states.

        @rtype C{Deferred} @return: A deferred whose callback is
        invoked when the notification mode has been correctly set. 
        """

        self.response_AUTH = self._idleHandler

        cmd  = 'IDLE'
        args = None
        resp = ('EXISTS', 'EXPUNGE')
        return self.sendCommand(Command(cmd, args, wantResponse=resp))

    def notif(self):
        """Returns a deferred triggered when the next notification arrives. 

        Returns immediately a deferred triggering the buffered
        notifications if any, or returns a deferred triggered on the
        reception of the next notification.
        """
        if len(self._lastCmd.lines) != 0:
            lines, self._lastCmd.lines = self._lastCmd.lines[:], None
            return defer.succeed(lines)
        else:
            self._lastCmd.defer = defer.Deferred()
            return self._lastCmd.defer

    def done(self):
        """
        Sends the done continuation data and returns a deferred
        triggered on the completion of the notification mode.

        Makes sure to use the existing tagged command.
        """
        self.sendLine('DONE')
        self._lastCmd.defer = defer.Deferred()
        return self._lastCmd.defer

    def _idleHandler(self, tag, rest):
        """
        Process line received one by one: buffers the notification if
        no deferred is in place to process them, else empty the buffer
        and execute the callback with the buffer content and the
        latest notification.

        Makes sure to use the existing tagged command.
        """
        if tag == '*' or tag == '+':
            if hasattr(self._lastCmd.defer,'callback'):
                lines = self._lastCmd.lines + rest
                self._lastCmd.lines = None
                self._lastCmd.defer.callback(lines)
            else:
                self._lastCmd.lines.append(rest)
        else:
            self.response_AUTH = self._defaultHandler
            self.response_AUTH(tag, rest)


def GetMailboxConnection(user=environ['USER'], mailbox="inbox"):
    """
    Returns a deferred triggered when an IMAP connection has been set,
    when the user has been logged in and when the mailbox has been
    selected.

    The callback is called with the protocole instance on which the
    IMAP commands are available.

    Similar in spirit to the getPage web client.  Might be a candidate
    for merging in twisted.mail if there is a will to provide users of
    the API with higher level functions. 
    """

    f = protocol.ClientFactory()
    f.user     = user
    f.password = getpass()
    f.mailbox  = mailbox 

    class ConnectInbox(imap4.IMAP4ClientWithNotif):
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
        

# User code
@defer.inlineCallbacks
def getSubjects(conn):

    messages = ( yield conn.fetchSpecific('1:*', 
                                          headerType = 'HEADER.FIELDS',
                                          headerArgs = ['SUBJECT']))
    for num, msg in messages.items():
        print num, msg[0][2]
        
    return conn

# Using the notification API.
@defer.inlineCallbacks
def receiveNewMails(conn, mailFrom):
    
    while True:

        yield conn.idle()
        count, response = (yield conn.notif())
        while response != 'EXISTS':
            count, response = (yield conn.notif())

        yield conn.done()
        getSubjects(conn) # here, the idea is to display them it to the
                          # desktop notification system
            
if __name__ == "__main__":

    # configure a search pattern

    GetMailboxConnection(
        ).addCallback(getSubjects)
        ).addCallback(receiveNotifs, "alice@alice")

    reactor.run()
