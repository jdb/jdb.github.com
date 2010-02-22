
Hello,

Dans le but de reduire les couts, je presente l'idee de reduire notre
effort de developpement et d'accelerer la livraison de fonctionnalites
en remplacant certaine de nos realisations interne par des logiciels
disponible. Certains projets ont une avance techonologique, d'autres
sont mieux documentes, d'autres plus matures et merite d'etre evalue
serieusement en interne.

Le besoin de nos client n'est pas d'etre le createur et auteur des
briques logicielles, par contre, ils nous demandent des solutions
fonctionnelles avecles briques que nous avons choisi et que nous
supportons.

L'exemple de Mac OS X est parlant, les créateurs d'un système
d'exploitation ont remplacé une brique centrale de leur technologie -
le noyau - par un système d'exploitation à la licence BSD très
libérale. Personne ne considère pour autant Apple comme un simple
intégrateur, l'entreprise est très profitable a l'heure actuelle et
leur coeur de métier qui reste secret, se place par dessus
le projet FreeBSD qu'il ont décidé d'adapter.

Je liste d'abord plusieurs technologies disponibles, dans la deuxieme
partie de ce mail sont presente les difficultes de cette approche.


Technologie disponible
======================


Gstreamer
---------

Gstreamer est un framework multimédia LGPL à base de plugins, initiée
en 2003 par une entreprise de Barcelone dont le coeur de métier est de
vendre des services de streaming web hostés sur leur propre datacenter
pour les sites web des chaines de télé espagnole. Leur streaming
server est open source et leur architecture logicielle est robuste.

Leur plateforme de CDN et de transcodage, supportant le telephone mobile,
fait bonne impression: http://bit.ly/12x0m.

La créativité des hackers autour de ces outils est un signe de la
flexibilité et de l'adoption du framework: bit.ly/1aZWfv .

Gstreamer fait aussi partie de l'installation minimale des
distribution linux depuis plusieurs années: Debian, Ubuntu, Fedora,
Red Hat, c'est à dire quelque millions d'utilisateurs et pas mal
d'entreprises.  Gstreamer est la pile multimedia des smartphones Nokia
(maemo.nokia.com). Plusieurs formats et codecs sont supportes (h264,
aac, flash, Apple streaming, ogg etc), et des tutoriels de
developpement de plugins sont disponibles pour la plupart des
langages. Cet été, des étudiants ont bossé, rémunérés par Google, pour
faire un plugin proche d'un circular buffer.


Deploiement logiciel Debian
---------------------------

La construction de firmware n'est pas aisee chez Anevia, un
developpeur peut difficilement recreer un environement de
developpement ou un firmware sans l'aide de l'integration. Les
instructions de compilation sont echangees de maniere informelle entre
equipe de developpement et integration. Les conflits de versions et
compatibilites logicielles ne sont pas sous controles.

Les outils de build, de packaging, de deploiement logiciels et de
construction de firmware du projet Debian sont assez flexibles pour
avoir permis a plusieurs projets dont Ubuntu ou Mint de re-utiliser
une chaine adaptee a leur besoins sans avoir a re implementer les
outils.

Pacemaker
---------

Projet de failover initié avec le projet Heartbeat il y a plus de six
ans, et maintenu par Novell. Pacemaker a plusieurs moyens pour
detecter et décider qu'un noeud ne répond plus. Un script aux
interfaces claires sont appelés pour effectuer la migration du service
vers un autre noeud.

Pacemaker fait partie de l'offre server de Red Hat, Ubuntu et
Suse.


AMQP et Thrift
--------------

AMQP est un protocol de communication entre serveurs, un peu comme
AIPC ou Corba. Par exemple, AMQP assure que des messages de
configuration de serveurs soient bien livrés a l'ensemble des VoDs, même
si ceux si sont éteints et allumés plus tards.

Thrift propose un format simple de contenu de message et de fonctions
appelables a travers le réseau et génère les stubs pour Java, C++,
Python, Ruby etc. AMQP s'occupait de livraison de messages, Thrift
s'occupe du format des messages et rends les messages intéropérables
entre différents languages de programmation. 

AMQP et Thrift constituent deux layers qu'implémentent les couches
basses de AIPC, ses bindings, et ALLP sans les efforts de maintenance.

Développé pour JP Morgan Chase en 2005 pour des communications fiables
et performantes au sein des salles de marché, adopté par des gros
vendeurs comme par des startups. Les implémentations sont disponibles
sous license LGPL dans la plupart des langages. Red Hat, en
particulier, distribue supporte officiellement ce projet dans leur
offre entreprise. Thrift est un projet open source realise et maintenu
par Facebook est en production pour des millions d'utilisateurs.


CouchDB
-------

Base de donnee legere, dont les access en simple HTTP peuvent etre
scriptes en mode texte si besoins est. Des librairies existent dans la
plupart des langages. Plutot que la sophistication du langage SQL,
cette base propose un acces comparable a celui d'un dictionnaire (tres
pratique, comme une hashmap ou tableau associatif). Cet usage est
adapte a la persistence de session ou a la configuration
distribuee. Ce projet est concu pour offrir les fonctionalites de
synchronization et de redondance entre serveurs.

Ce projet est integre a la prochaine version stable de Ubuntu pour
fournir une sauvegarde distante simplifie des profils utilisateurs et
donnees personnelles. Il est integre au kit de developpement rapide de
Canonical pour guider les developeurs d'applications et leur eviter de
concevoir leur propre persistence.

Le message encore n'est pas de tout changer et recommencer mais
d'evaluer et de choisir les technologies qui conviennent.

Comment determiner les projets professionels des projets moins serieux
======================================================================

L'idee ici est de se poser les bonnes questions avant d'engager des
ressources sur une technologie:

#. la technologie est elle adaptée a notre besoins? Quelle est la licence?

#. la technologie est elle mature, documentée, déployée? si la
   technologie est complexe, existe t'il une communauté professionelle
   capable de fournir des prestations de support ou de formation?

#. la gestion du projet est elle transparente? sont t'ils engages
   regulierement?

Pour répondre à ces questions, un projet open source présente souvent
des éléments tangibles.

#. La *gestion de sources* et le *suivi de bug* sont publics et
   fournissent la fréquence, le volume et la diversité des auteurs des
   contributions,

#. La *documentation* donne vite une idée des priorités et de
   l'expérience du projet. Les *tutoriaux* permettent de mesurer si la
   techno est pratique pour nous, bien conçue,

#. La *régularité des releases* et la *couverture des tests*
   permettent de mesurer leur organisation,

#. Sur les *mailings lists* ou sur les *salons IRC*, on évalue la
   disponibilité et la pertinence des interlocuteurs.

#. Les technos importantes sont régulièrement couvertes par des
   conférences, ou par des articles dans des revues de référence comme
   linux weekly news ou arstechnica. Elles sont reprises par des
   entreprises comme IBM, Google et autres Apple.

#. Les blogs de nombreux hackers peuvent démontrer un enthousiasme
   super productif et les innovations de ces produits.



Difficulte de la collaboration externe
======================================

Il faudra évaluer et faire confiance à des communautés externes à
l'entreprise sur lesquelles nous aurons peu de contrôle et peu de
liens contractuelles, a priori. C'est toujours plus simple de gérer un
problème de A à Z dans la même équipe lorsque l'on en a la
capacité. Pour que ça fonctionne avec des communautés distribuées dans
plusieurs pays, il faudra s'adapter à leur organisation et à leur
méthode de communication.

Prendre l'initiative de s'adresser a un média public comme des mailing
listes ou un salon IRC demande un peu d'expérience.  Arriver à
synthétiser le contexte dans une forme qui facilite la réponse prend
du temps, requiert de l'autonomie et un peu d'humilité. 

Ces modalités de communication peuvent laisser sceptique mais
plusieurs expériences professionnelles en travaillant au jour le jour
avec des specialistes de Postgresql, de MySQL cluster ou de la
virtualisation par exemple, m'ont convaincu de leur efficacité même si
ce sont des méthodes différentes des méthodes de communication
professionelles traditionelles.


Conclusion
==========

Des projets open source avancés offrent les fonctionnalités que nous
pouvons intégrer, vendre et supporter. L'evaluation d'un projet open
source peux s'effectuer de manière assez rationnelle.

