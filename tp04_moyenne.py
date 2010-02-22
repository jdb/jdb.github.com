#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle
from os.path import isfile
from os import remove
from optparse import OptionParser

# Declaration des constantes
dbfile = 'etudiant.db'

# Declaration des fonctions
def load():
    """Returns the database loaded from disk. The db format is
    specific of python and is useful for simple data storage"""
    if isfile(dbfile):
        return  cPickle.load( file(dbfile) )
    else:
        # If the database do not exists, return an empty data structure
        return {}

def save(db):
    """Writes the database to the disk"""
    cPickle.dump(etudiant, file(db, 'w'))
        
def moyenne(db, nom):
    """Renvoie la moyenne de 'nom' pris dans la base de donnee 'db'"""
    return reduce( lambda x,y: x+y, db[ nom ] ) / 4

# Declaration des options de la ligne de commande, generation de l'aide
def parse_args():
    usage = "Permet de rentre des notes pour chaque etudiant et de calculer des moyennes"
    p = OptionParser( usage=usage )
    p.add_option('-l', '--liste', action='store_true')
    p.add_option('-s', '--supprime', action='store_true', help="supprime la base de donnee")
    p.add_option('-n', '--note', metavar='tom,2')
    p.add_option('-e', '--enregistre', metavar='tom,15,9,12')
    p.add_option('-m', '--moyenne', metavar='tom')
    return p.parse_args()


# Chargement de la "base de donnees"
etudiants = load()

# Traitement des options de la ligne de commande
o, args = parse_args()


if o.liste and etudiant:
    print '\n'.join(sorted(etudiants))

elif o.supprime and isfile(dbfile):
    remove(dbfile)

elif o.note:
    nom, numero = o.note.split(',')
    print etudiants[nom][int(numero)]

elif o.moyenne:
    if o.moyenne in etudiants:
        print moyenne(etudiant, o.moyenne)

elif o.enregistre:
    name = o.enregistre.split(',')[0]
    etudiants[name] = [float(n) for n in o.note.split(',')[1:]]
    save()
    
