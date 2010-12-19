#!/usr/bin/env python
from random import uniform as u
from math import sqrt
import sys 
from itertools import ifilter

nb_points = int( sys.argv[1] )

points    = lambda n: ((u(-1,1), u(-1,1)) for i in xrange(n))
in_circle = lambda point: sqrt(point[0]**2 + point[1]**2) < 1

nb_points_in_circle = sum(1 for _ in ifilter(in_circle, points(nb_points)))
print("A slightly faster implementation: %s " %
      (nb_points_in_circle * 4.0 / nb_points))
