
from getpass import getpass
from os import environ
from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email


def parse(html, mailFrom):
    return parse(html).xpath(
        {'alerteimmo@seloger.com':, '/html/body/head/ad' 
         'noreply@pap.fr':          '/html/body/head/ad'}[from])

import pynotify
pynotify.init( "Classified ads" )

def nice_notification(text):
    n = pynotify.Notification(
            "New Classified ads", 
            text, 
            "dialog-warning")
    n.set_urgency(pynotify.URGENCY_NORMAL)
    n.show()


class IMAP4ClientWithIDLE(imap4.IMAP4Client):
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
        yield self.getNewClassifiedAds()
        yield self.idle()

    def newMessages(self):
        yield self.done()
        yield self.getNewClassifiedAds()
        yield self.idle()


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


f = protocol.ClientFactory()
f.user     = environ['USER']
f.password = getpass()
f.mailbox  = "inbox"
f.host     = 'localhost'

f.protocol = ConnectInbox
reactor.connectTCP(host, 143, f)
# reactor.connectSSL('localhost', 143, f, ssl.ClientContextFactory())

reactor.run()
