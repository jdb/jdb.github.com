#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import isfile
from os import remove
from optparse import OptionParser

# storm permet de manipuler des objets dans une base de donnee
# sans avoir a utiliser le langage special SQL
from storm.locals import *
# La base de donnee SQL est une alternative souvent pratique que les
# fichiers sur disque pour le stockage des donnees. C'est souvent un
# peu plus complique mais ce module rend les manipulations assez
# transparente

dbfile = 'store.db'

def initialise_database():
   """Renvoie une connexion sur une base de donnee relationnelle. Cree
   la base au preable si elle n'existe pas"""

   if isfile(dbfile):
      store = Store( create_database("sqlite:%s" % dbfile) )
   else: 
      store = Store( create_database("sqlite:%s" % dbfile) )
      store.execute("CREATE TABLE article "
                    "(nom VARCHAR PRIMARY KEY, marge FLOAT, prix FLOAT)")
      store.commit()
   return store


class Article(object):
   """L'article contient son nom, sa marge, son prix et sait calculer
   son prix affiche. L'article peux aussi etre range tel quel dans une
   base de donnees."""
   
   __storm_table__ = "article"

   # Les types de base utilises en dessous proviennent de Storm
   nom, prix, marge = RawStr(primary=True), Float(), Float()
   
   def __init__(self, nom, prix, marge):
      self.nom, self.marge, self.prix = nom, prix, marge
      
   def prix_affiche(self):
      return self.prix * ( 100 + self.marge ) / 100


def parse_args(): 
   """Options disponible sur la ligne de commande"""
   usage = "Permet d'enregistrer, supprimer, lister des articles du supermarche"
   p = OptionParser( usage=usage )

   p.add_option('-l', '--liste', action='store_true')
   p.add_option('-s', '--supprime', action='store_true')
   p.add_option('-e', '--enregistre', metavar='article,prix,marge')

   return p.parse_args()

(o, args) = parse_args()
# o contient des attributs qui sont les different options, si cet
# attribut est non vide, alors l'option a ete utilisee sur la ligne de
# commande et l'attribut contient la valeur passe en parametre

store = initialise_database()

if o.enregistre:
   nom, marge, prix = o.enregistre.split(',')
   store.add( Article(nom, float(prix), float(marge) ) )
   store.commit()

elif o.liste:
   print 'Article\tMarge\tPrix Affiche'
   for a in store.find(Article):
      print "%s\t%s\t%.2f" % (a.nom, a.prix, a.prix_affiche())

elif o.supprime and isfile(dbfile):
   remove(dbfile)
