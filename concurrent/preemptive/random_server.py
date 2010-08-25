#!/usr/bin/env python

import socket, time
s=socket.socket()
s.bind(('',5000))
s.listen(1)

import os 

while True:
    transport, _ = s.accept()
    time.sleep(0.001)
    transport.send("%s\n\n%s  \n\n%s\n\n" % (
                "You requested some random bytes:",
                os.urandom(16), 
                "You want fries with that?"))

    transport.close()

