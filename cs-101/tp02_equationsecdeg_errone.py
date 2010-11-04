#!/usr/bin/env python
# -*- utf-8 -*-
from math import sqrt

a=int(raw_input('Introduisez a : '))
b=int(raw_input('Introduisez b : '))
c=int(raw_input('Introduisez c : '))

if a==0:
    if b==0:
        print("L'equation n'admet pas de racine")
    else:
        print("L'equation est du premier degre et admet une racine: ")
        print("x = %s" % -c/b)

else:
    delta = b ** 2 - 4 *a*c
    print("Delta = %s" % delta )

    if delta > 0:
        print("Deux racines reelles distinctes :")
        print("x1 = %s" % ((-d+sqrt(delta))/(2*a)))
        print("x2 = %s" % ((-d-sqrt(delta))/(2*a)))

    elif delta==0:
        print("Une racine relle double :")
        print("x1 = x2 = %s" % (-b/(2*a)) )

    else:
        print("Deux racines complexes conjuguees :")
        print("x1 = %s + i %s" % ( -b/(2*a), sqrt(-delta)/(2*a) ) )
        print("x2 = %s - i %s" % ( -b/(2*a), sqrt(-delta)/(2*a) ) )
