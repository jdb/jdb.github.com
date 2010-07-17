
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class Client(basic.LineReceiver):
    
    delimiter = '\n'

    @defer.inlineCallbacks
    def connectionMade(self):
        print (yield self.plizRandom(None))
        print (yield self.plizClassified(None))        
        notifs = ( yield self.notifyMe(None) )
        for notif in (yield notifs )

            
# quelle est methode la plus claire pour appeler passer en mode notif?
# on ne peut pas le faire en mode bloquant: c'est le callback de la
# requete de notif qui doit creer un deferred et qui doit attacher le
# code dessus => il faut passer le callback de notif a la requete de
# notif pour qu'elle le passe a son callback pour qu'il le sette.

# ce callback recoit la notif, decide s'il doit 

# Imaginons les conditions initiales gerees



    # Internal
    def lineReceived(self, data):
        self.d.callback(data)
        
    def command(self, cmd):
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

    # API
    def plizRandom(self,_): 
        def gotRandom(number):
            return int(number)
        return self.command("random?").addCallback(gotRandom)

    def plizClassified(self,_): 
        return self.command("classified?")


    def notifyMe(self,_, notifCallback=self.gotNotification):
        def _notifyMe(response, notifCallback):
            print "about the notification request, server said ", response
            self.d = defer.Deferred().addCallback(notifCallback)
            return self.d
            
        return self.command("_notif_").addCallback(_notifyMe, notifCallback)

    def stopNotify(self, _):
        def _stopNotify(_):
            self.d = None
        return self.command("_stop_notif_").addCallback(_stopNotify)

    def gotNotification(self,notif):
        print "a notif:", notif
        self.d = defer.Deferred().addCallback(self.gotNotification)
        print "ready for a new notif" 
        return self.d

    class notifGen(object):

        forever = True
        p = self
        
        def __iter__(self, notifcb = self.gotNotification):
            return self

        def next(self):
            if forever:
                self.p.d = defer.Deferred()
                return self.p.d
            else: 
                raise StopIteration
            
factory = protocol.ClientFactory()
factory.protocol = Client
reactor.connectTCP("localhost", 6789, factory)
reactor.run()

