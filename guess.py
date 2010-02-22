
coups_max, secret_max = 15, 1000

# Regle du jeu et tirage du nombre mystere
print("\nJe vais choisir un nombre entre 1 et " + str(secret_max) + ".\n...")
import random
secret = random.randint(1, secret_max)

# Partie interactive
print("Voila, c'est fait; à vous de le deviner maintenant !")
coups_joues, tentative = 0, 0
while coups_joues < coups_max and tentative!=secret:
    tentative = int( raw_input("\nProposition ?\n") )
    coups_joues += 1

    if tentative < 1 or tentative > secret_max:
        print('On a dit entre 1 et 1000 !') 

    if   tentative < secret :
        print('Trop petit.')

    elif tentative > secret :
        print('Trop grand.')

    if abs( tentative-secret )==1:
        print('Mais ca brule !')

# Fin de la partie et affichage des resultats
if coups_joues==tentative:
    print('Oui !, Bravo,  vous avez trouve en %s coups.' %  coups_joues)
    print('Le nombre etait effectivement %s.' % secret)

else:
    print("""Bon, ca va bien maintenant %s on jette l'eponge !
    J'avais choisi %s.
    Vous n'etes pas encore pret pour le Juste prix""" % secret )
  
        
