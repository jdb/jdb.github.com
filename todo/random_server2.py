#!/usr/bin/env python

from twisted.internet import protocol, reactor 
import os, time

class random16bytes( protocol.Protocol ):
    def connectionMade(self):
        time.sleep(0.01)
        self.transport.write( "%s\n\n%s  \n\n%s\n\n" % (
                "You requested some random bytes:",
                os.urandom(16), 
                "You want fries with that?"))

        self.transport.loseConnection()

factory = protocol.Factory()
factory.protocol = random16bytes

reactor.listenTCP(5000, factory)
reactor.run()
