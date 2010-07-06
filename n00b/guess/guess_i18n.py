

import gettext
_ = gettext.gettext

gettext.bindtextdomain( "guess", "language.d")
gettext.textdomain("guess")
gettext.install("guess")


coups_max, secret_max = 15, 100

# Regle du jeu et tirage du nombre mystere
import random
secret = random.randint(1, secret_max)

# Partie interactive
print( _("J'ai choisi un nombre mystere entre 1 et %s ; a vous de jouer !") % secret_max )
coups_joues, tentative = 0, 0
while coups_joues < coups_max and tentative!=secret:
    tentative = int( raw_input( _("\nProposition ?\n")) )
    coups_joues += 1

    if tentative < 1 or tentative > secret_max:
        print( _('On a dit entre 1 et 1000 !') ) 

    if   tentative < secret :
        print( _('Trop petit.') )

    elif tentative > secret :
        print( _('Trop grand.') )

    if abs( tentative-secret )==1:
        print( _('Mais ca brule !') )

# Fin de la partie et affichage des resultats
if tentative==secret:
    print( _('Oui !, Bravo, vous avez trouve le nombre %s en %s coups.')
           %  (secret, coups_joues))

else:
    print( _("Bon, ca va bien maintenant. C'etait %s" ) % secret ) 
  
