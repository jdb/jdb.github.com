

"Push-email" dans Twisted: le making-of
---------------------------------------

Le projet Twisted est un ensemble du module, de classe et de
fonctions qui permettent de construire efficacement des applications
reseaux performantes et robustes.

Ce framework reseau couvre en particulier les protocoles d'emails:
SMTP, POP et IMAP. Par contre, Twisted ne fournit pas une extension du
standard IMAP: la commande *IDLE* qui permet le *push email*, c'est a
dire une methode d'acces aux emails plus performante: elle offre une
latence moindre, tout en diminuant la charge du serveur.

Apres une introduction sur les points cles de Twisted, cette
presentation montre les etapes d'une implementation de cette
extension d'IMAP dans Twisted :

1. la realisation d'un prototype du mecanisme de notification serveur
   vers client, avec les abstractions du framework,

2. puis l'architecture du module IMAP dans Twisted et le portage du
   prototype dans ces classes,

3. ensuite, les tests d'integration avec les serveurs largement
   utilises: Dovecot et Gmail,

4. enfin, l'adoption des methodes du projet Twisted qui conditionnent
   la revue du code et son eventuelle integration


Bio
---

Jean Daniel Browne

*Ingenieur projet* pendant deux ans chez Netcentrex qui concevait et
fournissait le coeur de reseau Voix sur IP de Orange, servant sur plus
de dix millions d'utilisateurs en France et Europe. Role de DBA, de
support, de formateur.

Ensuite, *developeur* pendant 2 ans: Bash, Python et Java au sein du
departement R&D, specialiste du deploiement et de la haute disponibilite.

Plus recemment, *architecte* chez Anevia, fournisseur de solution de
streaming. Role de conception et de specification des protocoles
internes et des elements de la plateforme logicielle.

Actuellement, travaillant sur un projet d'entreprise, et parallelement
se specialisant sur les technologies a la base des infrastructures des
systemes d'information d'envergure tels que Erlang, Twisted Python.
