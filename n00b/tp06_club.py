#!/usr/bin env
# -*- coding: utf-8 -*-

class membre:
    prenom = "Zoé"
    nom = "Dupont"
    address = "10, downing street"

liste_de_membres = []

def saisir_donnee():
    
    prenom = raw_input("Veuillez entrer un prenom (ou '$' pour arreter la saisie): ")
    while prenom != '$':
        nom = raw_input("Veuillez entrer un nom : ")

        m = membre()
        m.prenom = prenom
        m.nom = nom

        liste_de_membres.append(m)
        prenom = raw_input("Veuillez entrer un prenom (ou '$' pour arreter la saisie): ")


def index_prenom(prenom, reverse=False):
    
    if reverse:
        r=range( len(liste_de_membres) )
    else:
        r=range( len(liste_de_membres)-1, 0, -1)

    for i in r:
        if liste_de_membres[i].prenom==prenom:
            return i+1
    return 0


def index_prenom(prenom, reverse=False):
    for i in range( len(liste_de_membres) ):
        if liste_de_membres[i].prenom==prenom:
            print i+1


def print_index_prenom(prenom, reverse=False):
    for i in range( len(liste_de_membres) ):
        if liste_de_membres[i].prenom==prenom:
            print i+1

def print_index_prenom(prenom, reverse=False):
    for m in liste_de_membres:
        if m.prenom==prenom:
            print m.address, m.nom


# c'est une mauvaise habitude que de raisonner sur les positions des objets dans la collection
# c'est une mauvaise séparation des rôles de faire des fonctions qui acquiert les données et qui en même 
# temps, affiche le resultat de ces données. C'est un couplage fort (see wikipedia)

