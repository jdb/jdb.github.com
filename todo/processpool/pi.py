
from twisted.protocols import amp
from random import uniform
from math import sqrt
from itertools import ifilter
import sys

class Pi(amp.Command):

    arguments = [('n', amp.Integer())]
    response  = [('pi', amp.Float())]

class PiApproximation( amp.AMP ):

    def run( self, n ):
        points = lambda n : ( (uniform(-1,1), uniform(-1,1)) for i in xrange(n) )
        in_circle = lambda p : sqrt( p[0]**2 + p[1]**2 ) < 1

        pi =  sum( ( 1 for _ in ifilter( in_circle, points( n ) ) ) ) * 4.0 / n 
        return {'pi': pi }
    Pi.responder(run)

if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory
    pf = Factory()
    pf.protocol = PiApproximation
    reactor.listenTCP(int(sys.argv[1]), pf)
    reactor.run()
