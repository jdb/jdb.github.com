#!/usr/bin/env python
from random import uniform
from math import sqrt
import sys 

n = int( sys.argv[1] )
somme=0
for i in xrange(n):
    if sqrt( uniform(-1,1)**2 + uniform(-1,1)**2 ) < 1:
        somme+=1

print("An approximation of Pi is : %s " % (somme * 4.0 / n ))
