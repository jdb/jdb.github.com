# imap4client_yield.py
from getpass import getpass
from os import environ
from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email


def parse(html, mailFrom):
    return parse(html).xpath(
        {'alerteimmo@seloger.com':, '/html/body/head/ad' 
         'noreply@pap.fr':'/html/body/head/ad'}[from])

import pynotify
pynotify.init( "Classified ads" )

def nice_notification(text):
    n = pynotify.Notification(
            "New Classified ads", 
            text, 
            "dialog-warning")
    n.set_urgency(pynotify.URGENCY_NORMAL)
    n.show()

class ConnectInbox(imap4.IMAP4Client):
    @defer.inlineCallbacks
    def serverGreeting(self, caps):
        yield self.login(self.factory.user, self.factory.password)
        yield self.examine(self.factory.mailbox)
        self.factory.deferred.callback(self)
        
@defer.inlineCallbacks
def getNewClassifiedAds(conn):
    pattern = 'UNSEEN (OR (FROM alerteimmo@seloger.com) (noreply@pap.fr))'
    
    messageSet = imap4.MessageSet()
    for i in (yield conn.search(pattern)):
        messageSet.add(i)

    messages = ( yield conn.fetchSpecific(
            messageSet, 
            headerType = 'HEADER.FIELDS', 'BODY'
            headerArgs = ['FROM']))

    yield conn.setFlags(messageSet, 'Seen')

    for num, ads in messages:
        nice_notification(parse(ads[0][2], ads[0][3]))


def GetMailboxConnection(user, password, mailbox="inbox", host='localhost'):

    f = protocol.ClientFactory()
    f.protocol = ConnectInbox

    f.user, f.password = user, password
    f.mailbox, f.host  = mailbox, host

    f.deferred = defer.Deferred()
    reactor.connectTCP('localhost', 143, f)

    return f.deferred


( GetMailboxConnection(environ['USER'], getpass())
  .addCallback(getNewClassifiedAds) )

reactor.run()
