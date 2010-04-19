#!/usr/bin/env python
from random import uniform
from math import sqrt
import sys 

n = int( sys.argv[1] )

points    = lambda n : [ (uniform(-1,1), uniform(-1,1)) for i in range(n) ]
in_circle = lambda p : sqrt( p[0]**2 + p[1]**2 ) < 1

print("Another approximation of Pi is: %s " %
      ( len( filter( in_circle, points( n ) ) ) * 4.0 / n ))
