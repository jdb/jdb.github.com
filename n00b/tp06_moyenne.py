#!/usr/bin/env python

from os.path import exists
from cPickle import load, dump

class Etudiant:
    nom, prenom, notes = '', '', []
    
dbfile='etudiants.db'

def saisir_etudiant():
    """Renvoie un tableau de 'struct' Etudiants.

    Charge la base si elle existe, puis demande a l'utilisateur de
    saisir les informations eventuelles concernant de nouveaux
    etudiants, et sauve le tableau mis a jour"""
    
    if exists(dbfile):
        classe = load( file( dbfile )  )
    else: classe = []
    
    nom = raw_input("Veuillez saisir le nom de l'tudiant ($ pour quitter): ")
    while nom != '$':
        e = Etudiant()
        e.nom = nom
        e.prenom = raw_input("prenom nom de l'etudiant: ")
        for i in range(3):
            e.notes.append(float(raw_input("Note :")))
        classe.append(e)
        nom = raw_input("Veuillez saisir le nom de l'tudiant ($ pour quitter): ")

    dump( classe, file( dbfile, 'w' ) )
    return classe

def calcul(notes):
    return sum(notes)/len(notes)

# Main

classe = saisir_etudiant()

for etudiant in classe:
    if calcul( etudiant.notes )>=10:
        print etudiant.nom, etudiant.prenom
