


from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email


class ConnectInbox(imap4.IMAP4Client):
    
    @defer.inlineCallbacks
    def serverGreeting(self, _):
        yield self.login(self.factory.user, self.factory.password)
        yield self.select(self.factory.mailbox)
        self.factory.deferred.callback(self)

    @defer.inlineCallbacks
    def idle(self):
        """
        Request the notifications of new mails

        This command is allowed in the Authenticated and Selected states.

        @rtype C{Deferred} @return: A deferred whose callback is
        invoked when new mails have arrived. The sucessfull response
        does not invoke the callback, but a failed response does
        invoke the errback. The successful 

        Here the question is: how to make a function which makes a
        request and whose callback is actually not invoked on the
        first but on the second data?
        """
    @defer.inlineCallbacks
    def fetchAllUIDs(self):
        result = yield self.fetchUID(imap4.MessageSet(1, None), True)
        uids = [v['UID'] for v in result.values()]
        defer.returnValue(uids)

    @defer.inlineCallbacks
    def fetchMessageObject(self, uid):
        m = (yield self.fetchMessage(imap4.MessageSet(uid), True))
        msg = email.message_from_string(m.values()[0]['RFC822'])
        defer.returnValue(msg)
        
class ConnectInboxFactory(protocol.ClientFactory):
    
    protocol = ConnectInbox

    def __init__(self, user, password, mailbox):
        self.user     = user
        self.password = password
        self.mailbox  = mailbox
        self.deferred = defer.Deferred()

@defer.inlineCallbacks
def getTitles(conn): # with a pattern which matches a from
    "This function expects a IMAP connexion to a mailbox"
    for uid in (yield conn.fetchAllUIDs()):
        print (yield conn.fetchMessageObject(uid)).get('Subject')

    notify(conn, pattern)

    reactor.stop()

@defer.inlineCallbacks
def notify(conn, pattern):
    
    for uid in (yield conn.idle()):
        print (yield conn.fetchMessageObject(uid)).get('Subject')
    notify(conn, pattern)
    

# do I need a state machine (actually no, I can trust my server to be
# in the state I expect and not send me unexpected messages)?

# it is not going to be difficult to write the idle command in the
# socket, the core of our mini pb is to hack into IMAP4Client's
# gotData to call self.notification(result)

# def notification(self, data):
#    this data contains the UIDs
#    from these UIDs, I want to print the 


# what is this weird object sent by fetchMessage and fetchUid?
# how do I select message with imap4.MessageSet?
# how do I run tests?
# how do I pdb twisted?

if __name__=="__main__":

    from getpass import getpass
    from os import environ

    factory = ConnectInboxFactory(environ['USER'],
                                  getpass(),
                                  "inbox")

    factory.deferred.addCallback(getTitles)
    reactor.connectTCP('localhost', 143, factory)
    print "TCP connected"
    reactor.run()
    
