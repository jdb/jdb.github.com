#!/usr/bin/env python

a=int(raw_input('Introduisez a : '))
b=int(raw_input('Introduisez b : '))
c=int(raw_input('Introduisez c : '))

if a==0:
    if b==0:
        print("L'equation n'admet pas de racine")
    else:
        print("L'equation est du premier degre et admet une racine: ")
        print("x = %s" % -c/b)

else :
    from cmath import sqrt
    print("x1 = %s " % ( -b/( 2*a ) + sqrt( -b ** 2 + a*c )/( 2*a ) ) )
    print("x2 = %s " % ( -b/( 2*a ) - sqrt( -b ** 2 + a*c )/( 2*a ) ) )
