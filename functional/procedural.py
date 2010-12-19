#!/usr/bin/env python
from random import uniform
from math import sqrt
import sys 

nb_points = int(sys.argv[1])
nb_points_in_circle = 0
for i in xrange(nb_points):
    if sqrt(uniform(-1,1)**2 + uniform(-1,1)**2) < 1:
        nb_points_in_circle+=1

frequency = nb_points_in_circle / float(nb_points)
print("an approximation of Pi is : %s " % (frequency * 4.0))
