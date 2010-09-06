#!/usr/bin/python

from StringIO import StringIO
import sys, os
from twisted.internet import reactor, protocol, defer
from twisted.mail import smtp, relaymanager
from twisted.python import usage

class SMTPClient(smtp.ESMTPClient):

    def getMailFrom(self):
        return self.factory.mailFrom

    def getMailTo(self):
        return [self.factory.to]

    def getMailData(self):
        return self.factory.data

    def sentMail(self, code, resp, numOk, addresses, log):
        print 'Sent', numOk, 'messages'

        from twisted.internet import reactor
        reactor.stop()

class SMTPClientFactory(protocol.ClientFactory):

    def __init__(self, mailFrom, to, data):
        self.mailFrom = mailFrom
        self.to = to
        self.data = data

    def buildProtocol(self, addr):
        self.protocol = SMTPClient(secret=None, identity='example.com')
        self.protocol.factory = self
        return self.protocol


@defer.inlineCallbacks
def sendmail(mailFrom, to, data):
    host = to.split('@')[1]
    mx_record = yield relaymanager.MXCalculator().getMX(host)
    exchange = str(mx_record.exchange)
    factory = SMTPClientFactory(mailFrom, to, data)
    reactor.connectTCP(exchange, 25, factory)


### The SMTP client really stop here, below is the definition and
### parsing of the command line options and the call to sendmail()

class Options(usage.Options):

    example = """\
Date: Fri, 6 Feb 2004 10:14:39 -0800
From:  Guy <tutorial_sender@example.com>
To:  Gal <tutorial_recipient@example.net>
Subject: Tutorate!

Hello, how are you, goodbye."""    

    optParameters = [
        ["to"  , "t", os.environ['USER']+'@localhost',    "The mail recipient"],
        ["from", "f", os.environ['USER']+'@localhost',    "The sender"],
        ["data", "d", StringIO(example), "The mail data", 
         os.path.exists]]

    def postOptions(self):
        if isinstance(self['data'],basestring):
            self['data'] = open(self['data'])

if __name__=='__main__':

    try:
        print Options.example
        o = Options()
        o.parseOptions()
    except usage.UsageError, errortext:
        print '%s: %s' % (sys.argv[0], errortext)
        print '%s: Try --help for usage details.' % (sys.argv[0])
        sys.exit(1)

    sendmail(o['from'], o['to'], o['data'])

    reactor.run()

