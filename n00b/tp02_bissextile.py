#!/usr/bin/env python
# -*- coding: utf-8 -*-

year = int(raw_input("Veuillez introduire une annee : "))

if year % 4 != 0:
    print("L'annee n'est pas bissextile")
else:
    if year % 400 == 0 and year % 100 != 0:
        print("L'annee est bissextile")
    else:
        print("L'annee n'est pas bissextile")
