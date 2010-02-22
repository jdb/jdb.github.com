#!/usr/bin/env python
# -*- coding: utf-8 -*-

mi = int(raw_input("Quel est le montant imposable de votre foyer ? : "))
print(""" Voici comment se repartisse les parts : 
1 si célibataire
2 si couple
2,5 si couple avec 1 enfant
3 si couple avec 2 enfants
4 si couple avec 3 enfants
5 si couple avec 4 enfants
""")
n = float(raw_input("Quel est votre nombre de parts ? : "))

ri = mi * 0.9 * 0.8

qf =  ri / n

if qf <= 25610:
    i = 0
elif qf > 25610 and qf <=50380:
    i =(ri * 0.105) - (2689 * n )
elif 50380 < qf and qf <= 88670:
    i = (ri * 0.24) - ( 9490 * n)
elif 88670 < qf and qf <= 143580:
    i = (ri * 0.33) - ( 17470 * n)
elif 143580 < qf and qf <= 233620:
    i = (ri * 0.43) - ( 31828 * n)
elif 233620 < qf and qf<= 288100:
    i = (ri * 0.48) - ( 43509 * n)
else :
    i = (ri * 0.54) - ( 60795 * n)

print("Votre revenu imposable est de : %s" % i )
