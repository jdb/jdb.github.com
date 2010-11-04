#!/usr/bin/env python
# -*- coding: utf-8 -*-

# l'idee c'est de separer les donnees du code qui va s'en
# servir. Cette separation sert a pouvoir mettre a jour les donnees
# sans toucher au code. Ca sert aussi a pouvoir tester le code avec
# toute sorte d'autre donnees.

# c'est un peu la base des modeles des three tiers, et du model-view-controller.


class Part:

    partchoice = dict((
        (1,"  si célibataire"),
        (2," si couple"),
        (2.5," si couple avec 1 enfant"),
        (3," si couple avec 2 enfants"),
        (4," si couple avec 3 enfants"),
        (5," si couple avec 4 enfants"),
        ))

    def __init__(self, part):
        if float(part) in self.partchoice:
            self.value = float(part)
        else:
            raise Exception,"Value error : Une part doit etre parmi les valeurs %s " % (
                ' '.join( [ str(p) for p in sorted(self.partchoice)]))

    @classmethod   
    def menu( obj ):
        return  "Voici comment se repartisse les parts :\n" + \
               '\n'.join( [ str(part) + text for part, text in partchoice.items() ] )
    

class Impot:
    _coeff = dict((
        # ( quotient familial, ( coefficient du revenu imposable , coefficient de la part))
        (0, (None, None)),
        (25610, (0, 0)),
        (50380, (0.105, 2689)),
        (88670, (0.24, 9490)),
        (143580, (0.33, 17470)),
        (233620, (0.43, 31828)),
        (288100, (0.48, 43509)),
        (10**12, (0.54,60795)),
        ))

    def __init__(self, mi, part):
        self.montant_imposable, self.part = montant_imposable, part.value

    def coeff(self):
        """Retourne les coefficients necessaire au calcul de l'impot
        adapte au quotient familial.
        """
        my_qf=self.quotient_familial()
        minimum = min( self._coeff )
        for qf in sorted(self._coeff)[1:]:
            if minimum <= my_qf and my_qf< qf:
                return self._coeff[qf]
            else:
                minimum = qf
                
    def revenu_imposable(self): return self.montant_imposable * 0.9 * 0.8

    def quotient_familial(self): return self.revenu_imposable() / self.part

    def calcule(self):
        ri_coeff, part_coeff = self.coeff()
        return self.revenu_imposable() * ri_coeff - self.part * part_coeff
            
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1 :

        usage = """
usage : ./tp03_impot_l33t.py montant_imposable nb_part
./tp03_impot_l33t.py calcule l'impot a partir du montant imposable et du nombre de part.
ex: ./tp03_impot_l33t.py 33000 1\
%s""" % Part.menu()
        
        print( usage)

    else:
        montant_imposable, part = sys.argv[1:2]
        print Impot( montant_imposable, Part(part) ).calcule()
