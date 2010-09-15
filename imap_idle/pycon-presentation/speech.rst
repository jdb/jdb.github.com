
Intro a Twisted
===============

#. titre

Bonjour a tous, je suis Jean Daniel Browne, je vais passer une petite
demi heure a vous presenter une introduction a Twisted, et a expliquer
et a illustrer la programmation evenementielle.  

Cette presentation a ete realise dans le cadre de la creation d'un
patch le module IMAP de Twisted pour ajouter le Push Email mais nous
n'aborderons pas la partie IMAP qui est trop dense pour etre traiter
correctement en une demi heure, malgre ce qui etait promis sur le
programme. 

A priori, il n'y a pas de prerequis pour suivre cette presentation
sauf peut etre savoir ce qu'est un thread. Si vous avez des questions,
faite moi signe, je suis plus a l'aise dans l'echange que dans le
cours magistral.

#. plan

La presentation se deroulera de la maniere suivante avec en premiere
partie: les cles que l'on peu retenir sur Twisted et les usages pour
lesquelles Twisted est bien adapte.

La seconde partie tente d'expliquer le mecanisme au coeur de Twisted
qui rend possible la programmation reseau concurrente sans utiliser ni
process, ni thread. Si je suis assez clair sur cette partie, alors la
presentation aura atteint son but principal.

La derniere partie va presenter va illustrer les classes principales
de Twisted a travers la realisation du client d'un protocole
client/serveur tres simple, completement invente, qui permet non
seulement au client d'envoyer des requetes et de recevoir des reponses
mais aussi des notifications, non sollicitees, venant du serveur.
Cette derniere partie montrera deux version de l'api du client, l'une
synchrone et une asynchrone qui leve certaine contraintes.

#. Twisted: usages et points cless

#. Des applications multiprotocoles distribues

Un framework reseau qui offre un model mental et une boite a outils
pour concevoir et representer les echanges reseau. Twisted offre les
memes representations pour des protocoles de transfert de fichier,
d'email, de chat, pour les services de nom de domaines, par
exemple. D'une certaine maniere, Twisted offre une traduction entre un
diagramme de sequence de message et un modele objet. En fournissant
des abstractions pour les appels de procedure distance ou une
authentication assez flexible pour s'adapter a la variete de solutions
emploes sur le web et dans les entreprises.

Les methodes de developpement et de tests du projets s'insere
particulierement bien dans le cadre d'applications d'envergures. 
Un effort particulier est consacre a la resolution des regressions et
a la compatibilite ascendante a chaque nouvelle release. Les
mecanismes au coeur de Twisted peuvent tout a fait s'appliquer pour
faire des interfaces graphiques GTK mais le contexte est peut etre
plus propice aux developeurs de large applications reseau.

#. Interfaces non bloquantes

Je vais vous presenter un court code utilisant une interface bloquante
typique de la librairie standard puis vous montrer l'equivalent en
Twisted. L'idee est de recuperer sur 4 sites de blog, le titre du
premier article de chaque blog. C'est tres simple.

#. premier code

Pour fouiller le document html, je vais utiliser le nodule lxml, et je
difini un petite fonciton *dig* qui a partir d'une chaine de caractere
html et d'une expression xpath de renvoyer le text inclu dans le
premier noeud html qui correspond a l'expression xpath.

La liste de blogs est nommee *planets*, et j'ai soigneusement
selectionne des blogs qui presentent la meme sructure de html pour que
l'exemple fonctionne correctement.

La fonction bloquante est la fonction urlopen qui a partir d'une url
renvoie le contenu html de la page. La fonction first_title utilise
urlopen et affiche le premier titre d'article a partir d'une url donne
en argument.

Pour chaque blog, on execute la fonction first_title, apres que le
premier titre ait ete recu et affiche, la seconde requete est
inities. Les requetes sont successsives.

#. second code

Voici le code equivalent en Twisted qui presente une interface non
bloquante, Deux import sont necessaires: le reactor que j'explique
plus en details dans la seconde partie de cette presentation et la
fonction getPage qui est l'equivalent non-bloquant en Twisted de la
fonction urlopen.

Je pense qu'il est interessant de noter, que la partie traitemente de
la reponse est explicitement dans une fonction differente de
l'emission de la requetes, ce point est important pour la suite. Lors
de l'emission de la requete, on fournis aussi tout le materiel pour
traiter la reponses, lorsqu'elle arrivera. On dit que la fonction
print_first_title est stockee comme callback de la requete getPage.

La difference principale avec le code precedent, c'est la concurrence
des requetes. getPage retourne avant que la reponse ne soit
disponible, les quatre requetes sont toutes effectuees avant que la
premiere reponse parvienne. Ce code s'execute potentiellement 4 fois
plus vite.



#. ni thread, ni verrou

Les threads sont des primitives du systeme d'exploitation qui
permettent la programmation parallele.  Les threads posent des
contraintes. Par exemple, des risques de corruption des ressources
partages. Pour s'en proteger, la solution courrement utilisee est de
verrouiller la ressource partagee. Mais les verrous posent aussi leurs
propres contraintes. Les threads vont s'attendre voire se emttre dans
des situations d'interblocage qui peuvent bloquer l'application.

#. code

XXXXXX


Twisted s'affranchit de ses contraintes. Il n'y a pas de threads dans
Twisted, chaque fonctions qui s'execute, s'execute seule sans etre
interrompu jusqu'a ce qu'elle retourne, aucune autre fonctions ne peux
s'executer en meme temos: elle a donc un acces exclusif aux ressources
tout le long de son execution.

#. la necessite de retourner rapidement

Comme une seule fonction s'execute jusqu'a sa fin sans etre
interrompue, une contrainte importante dae la programmation avec
Twisted doit etre gardee a l'esprit: une fonction qui ne retourne pas
bloque les autres fonctions qui sont susceptibles d'etre execute et
bloque l'ensemble de l'application. Les developeurs doivent garder a
l'esprit d'ecrire des fonctions qui retourne rapidement.

Une derniere note sur les mecanisme concurrent. A l'inverse du
mecanisme de concurrence des thread et des process qui est appele
pre-emptif parce threads et process vont etre pre-empte sans qu'ils le
sollicitent, le mecanisme de concurrence de Twisted est appele
cooperatif, chaque fonction doit garder a l'esprit que d'autres
fonctions doivent potentiellement s'executer pour la bonne execution
de l'application.

#. Le interne mecanisme du reactor

Pour resumer, j'ai explique que Twisted est bien adapter programmer de
maniere concurrente des applications reseau et j'explique ensuite,
qu'une seule fonction peux seule etre execute a la fois et
bloque l'exeuction d'autres fonctions candidates a l'execution.

Cela peux sembler contradictoire, mais La partie suivante, sur le
mecanisme interne du coeur de Twisted qui s'appelle le reactor,
reconcilie ces deux affirmations qui semble contradictoire. En dehors
du contexte de Twisted, le reacteur est un modele de conception que
l'on retrouve dans d'autres projet comme Node.js en javascript, comme
EventMachine en Ruby. Ce modele de conception a ete nommee ainsi non
pour faire reference a un moteur a reaction mais bien parce qu'il
reagit aux evenements (to react en anglais), dans notre contexte,
surtout des evenements reseau.

Ce mécanisme est a comparer a n threads ayant initiée puis surveillant
son propre thread.

Si l'on reprend l'exemple des articles de blogs, l'execution se passe
de la maniere suivante: la fonction getPage est execute quatre fois,
sequentiellement sur des urls differentes. getPage ne retourne pas
quand la reponse est arrive, getPage retourne des que la requete est
emise. Ensuite les callback de traitement de la reponse sont eux aussi
execute sequentiellement.

Ce qui est possible de dire, c'est que 4 socket sont maintenues
ouvertes en parallele et les reponses sont attendue en parallele,
mais leur creation et le traitement de leur reponse sont effectue
sequentiellement.

Du point de vue du developeur, le demarrage du reactor doit etre la
derniere ligne du programme. Sans elle, aucune requete reseau n'est
effectue, les lignes precedent le demarrage du reactor correspond a
une construction de l'ecoulement du programmes, c'est la definition
des evenements et de leur callbacks. Le reactor, une fois lance n'est
arrete que pour terminer le programme. Le reactor ne retourne jamais.

#. un appel systeme

Cette appel systeme permet la supervision d'une liste de
socket. select retourne des qu'un evenement est survenu sur une socket
avec la liste des sockets sur lesquelles des donnees sont arrivees.

Pour effectuer la supervision d'une liste de socket sans select, il
est tout a fait possible de lancer autant de thread que de socket et
pour chaque thread, de surveiller sa propre socket. Ici, il y a au
moins deux avantages: la supervision est deleguee au noyau, cet effort
est decharge du developeur. L'autre bonus important pour un
developeur. c'est l'utilisation du meilleur appel systeme disponible
sur chaque platformes, select est un filet disponible sur chaque
systeme d'exploitation mais epoll sous Linux, ou kqueue sous BSD sont
bien plus efficaces. En utilisant Twisted, le developeur directement
met a profit le meilleure appel systeme present de supervision de
socket sur le system d'exploitation.

#. le Protocol

La seconde idee au coeur du reactor qui etend le service rendu de l'appel
systeme: le reactor maintient un mapping entre les sockets supervisees
et pour chaque, une instance de la classe Protocol (je simplifie un
peu en omettant la class factory de Twisted). 

Pour un developeur qui veut implementer un protocol, son role est de
creer une classe qui derive de Protocol et de surcharger la methode
dataReceived() avec le code de traitement de la reponse. La methode
dataReceived() analyse les donnees et declenche les bon callbacks. Si
l'on implementait un client HTTP, la methode dataReceived mettrait
dans un buffer les fragments de reponses et pourrait ensuite appeler
deux callbacks: headerReceived et bodyReceived.


#. des l'arrivee des donnees

Pour resumer cette courte partie sur le reactor et le protocole, a
l'arrivee des donnes dans une socket, le reactor declencle la methode
dataReceived de l'instance de Protocole associe a cette socket. Charge
au developeur de mettre son code de traitement dans ce callback.


#. Avantage d'une API asynchrone sur asynchrone

Cette derniere partie presente un court example d'un client en
Twisted, ce qui va nous permettre de fixer un peu les idees et les
classes impliquees. De plus, je vais illustrer l'idee qui n'est peut
etre pas evidente pour tout le monde qu'une API asynchrone est plus
utile pour recevoir des evenements.

Ce client implemente un protocole invente, qui permet a un client de
demander les derniers nombres aleatoires et les dernieres petites
annonces disponible sur un server. Ce protocole permet aussi au client
de demander au server de se mettre dans un mode de notification, ou le
server envoie un court message signifiant la disponibilite soit d'une
petite annonce soit d'un nombre aleatoire. La notification ne contient
pas le nombre aleatoire, mais seulement l'information qu'un nombre
aleatoire est disponible. Le client doit rentrer dans le mode de
notification jusqu'a ce qu'il recoive une notification qui
l'interesse. Et il doit en sortir pour telecharger la derniere item
disponible.



