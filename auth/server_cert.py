from OpenSSL import SSL
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol

class Echo(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

def verifyCallback(connection, x509, errnum, errdepth, ok):
    if not ok:
        print 'invalid cert from subject:', x509.get_subject()
        return False
    else:
        print "Certs are fine", x509
    return True

if __name__ == '__main__':
    factory = Factory()
    factory.protocol = Echo

    myContextFactory = ssl.DefaultOpenSSLContextFactory(
        'server.pem', 'server.pem'
        )

    ctx = myContextFactory.getContext()

    ctx.set_verify(
        SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
        verifyCallback
        )

    # Since we have self-signed certs we have to explicitly
    # tell the server to trust them.
    ctx.load_verify_locations("client.pem")

    reactor.listenSSL(8000, factory, myContextFactory)
    reactor.run()

    # avec ce code, j'arrive a configurer la PKI pour que le server
    # puisse verifier que le client fait partie des locations, mais en
    # boite noire, je ne peux pas demander a lire les informations
    # dans le certificat pour attribuer une liste de droits par
    # exemple.
