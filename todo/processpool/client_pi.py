#!/usr/bin/env python

import pi
from twisted.internet.protocol import ClientCreator
from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks

import sys

def accumulate_pi( p ):
    accumulate_pi.pi = (accumulate_pi.pi*accumulate_pi.n + p['pi'] )/(accumulate_pi.n+1)
    accumulate_pi.n += 1

accumulate_pi.n = 0
accumulate_pi.pi = 0


@inlineCallbacks
def client( port ):
    p = yield ClientCreator(reactor, pi.PiApproximation).connectTCP(
        '127.0.0.1', port )
    approx = yield p.callRemote( pi.Pi, n=int(sys.argv[1])/2)
    p.transport.loseConnection()
    accumulate_pi( approx )

@inlineCallbacks
def barrier():
     yield DeferredList( [ client(5000), client(5001)]  )  # 5 
     print accumulate_pi.pi
     reactor.stop()

reactor.run(barrier())
