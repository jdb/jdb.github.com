#!/usr/bin/env python

from random import uniform
from math import sqrt
import sys 
from itertools import ifilter

n = int( sys.argv[1] )

points    = lambda n : ( (uniform(-1,1), uniform(-1,1)) for i in xrange(n) )
in_circle = lambda p : sqrt( p[0]**2 + p[1]**2 ) < 1

print("A slightly faster implementation o Pi: %s " %
      ( sum( 1 for _ in ifilter( in_circle, points( n ) ) ) * 4.0 / n ))
