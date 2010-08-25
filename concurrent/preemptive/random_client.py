#!/usr/bin/env python

import socket, struct

s=socket.socket()
s.connect(('localhost',5000))
response = s.recv(128)

# transforms a so called *unsigned integer* (between 0 and 2**32-1) to
# a decimal between -1 and 1
proportionality = lambda integer: integer * 2.0 / (2**32-1) - 1
coords = map( proportionality, struct.unpack('IIII',response[34:50]))

print( "First point:  A ( %s, %s )" % (coords[0], coords[1]) )
print( "Second point: B ( %s, %s )" % (coords[2], coords[3]) )
