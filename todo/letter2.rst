Réflexion sur nos propres produits
==================================

Si l'on évalue des technologies, c'est que l'on questionne le devenir
de projets internes: faut t'il dire aux équipes qui développent ces
applis depuis 2 ans que le choix n'était pas le bon?

Ce n'est pas un aveu d'échec, c'est une inflexion de cap avisée. La
décision de produire AIPC, par exemple, était la bonne au moment ou
elle a été prise. La question se pose à la lumière de deux ans
d'expérience, cela nous coute t'il plus cher de continuer a maintenir
ce logiciel ou d'autres logiciels présente plus d'avantages? Si on
prend l'exemple d'Etienne, ou de Sylvain, ils sont conscient (et
parfois inquiets) des forces et des faiblesses des applis qu'ils
maintiennent. Si ils croient dans leur logiciel, c'est un élément
important pour le faire évoluer, par contre si eux mêmes ne sont pas
convaincu, c'est peut être qu'ils se rendent compte qu'il y a des
alternatives plus avancées.

Ce n'est pas une pilule amère que l'on fait avaler aux développeurs,
c'est un caramel qu'on leur propose! Si ce sont des technologies
largement utilisées par l'industrie, ils gagnent en reconnaissance sur
le marché du travail. Ils sont opérationels immédiatement au lieu
d'être experts sur des applications inconnues en dehors de
l'entreprise. Elles sont mieux documentées et sont plus simples à
installer lorsqu'elles sont disponible chez les distributions
populaires, ce qui facilite le travail au jour le jour.

#. donner une visibilité aux équipes de dev Sylvain et Etienne  

#. y a un enthousiasme de hacker qui font des prodiges alors que nos
   équipes sont au 35 effectives !

#. Culture de la collaboration qui nous manque 

Avons nous les moyens de nous reposer uniquement sur une debian et un
compilateur C++ pour construires seuls la pile logicielle de nos
produits?  Nous ne sommes pas "intégrateur" dans la
mesure ou nous sommes à même de modifier directement les briques du
produit que l'on vend. Pourquoi ne pas partir du point de vue inverse
qui est de dire qu'un client peut s'étonner s'il sait l'on a
redéveloppé en interne les protocoles, la persistence, la redondance,
etc.

installer la dernière techno a la mode s'oppose à assembler des
briques innovantes disponibles.

problèmes des vieux langages: 

- buffer overflow and memory leak is one thing, really quickly you get
  to think the structure of a process, with its sections bss etc,

- simplification des APIs, par exemple, ces trois fonctions permettent
  d'éviter des logs pourris. On y a bien réfléchis, et au bout du
  compte, quand nous étions satisfait, j'ai fait le rapide exercice de
  traduire l'API en python, et en fait les trois fonctions
  disparaissent. On exprime cette logique particulière avec les
  éléments du langage sans utiliser une librairie ou module
  particulière.


there is no need to create object if you just need encapsulation, do
it if you want destructors, inheritance



Si ça vous intéresse toujours, et que vous avez des remarques...


Récentes success story
======================

*Cela n'a pas beaucoup sens de vouloir faire du business sur de l'open
source*

KVM a créé un module pour le noyau linux, un produit et une entreprise
autour, est une startup de qui été rachetées par Red Hat pour
plusieurs dizaine de millions de dollars. JBoss qui a été rachetée
pour à peu près la même somme que Netcentrex, la Berkeley DB rachetée
par Oracle, ou MySQL rachetée pour presque un milliard de dollars par
Sun.

Canonical ou Rpath qui sont des experts du déploiement logiciel, ou
Suse et Red Hat qui proposent des solutions de haute disponibilité
flexible. Google et Canonical proposent chacun un Chief Open Source
Officer qui présente la position officielle de l'entreprise et une
interface pour la communauté.

Parmi les grosses entreprises de logiciel IBM, Oracle, Intel, Sun,
Google, Yahoo, Facebook, Second Life, tous utilisent et développent
beaucoup de projets open source au sein de leur infrastructure et se
innovent sur leur coeur de métier.


Crédibilité auprès des clients
==============================

*Sera t'on crédible auprès des clients si l'on ne cree plus nous meme
les logiciels et que nous sommes intégrateur?*

Je n'en vois pas d'implications entre des décisions circonscrites à la
R&D et le business model ne change pas. Par exemple, il n'y a aucun
besoin de modifier les plaquettes commerciales.


#. le libre le libre, tu nous emmerdes avec le libre. Avant que l'on
   me mette dans une petite boite sur la croisade du logiciel libre,
   je voulais bien ecrire clairement que c'est trois points que nous
   avons pas et 

#. on évalue pas le libre, on s'inspire de ce qui existe. Partir de la
   techno pour faire un produit, Certaines briques technos sont 

#. attention au contexte et aux gens a qui je l'envoie,

#. Pour monter un escalier, faire la première marche.

Chacun à son idée sur la raison pour laquelle Anevia n'est pas encore
le prochain Apple ou Youtube, il n'y a donc pas de raison que je n'ai
pas moi même la solution à tout nos problèmes.
