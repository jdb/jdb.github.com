
Kernel
======

Cette page est censé répondre 

* Pour l'install de VMWare ou Ndiswrapper, recompiler le noyau ou
  juste installer les en-têtes?

* Quid de la pollution de /usr/lib/modules par les nouveaux noyaux?

* De l'upgrade d'un noyau à un autre (automatique ou locked)?

Install sources or just headers
-------------------------------

Installer les sources du noyaux ou juste les fichiers d'en-têtes (headers)?


En résumé ::

  sudo apt-get install linux-source-`uname -r`
  cd vmware-directory && sudo vmware-install

Maintenant, l'explication: dans plusieurs cas (install de Vmware, de
drivers Nvidia, ou de Ndiswrapper, driver de webcam), les sources du
noyaux sont nécessaires car elle contiennent des infos qui vont
permettre d'optimiser le driver/module.

Seulement, si l'on utilise tranquillement le noyau patché d'Ubuntu
2.6.10-5-386, on va chercher a installer le paquet des sources
correspondante... Que l'on ne va pas trouver. On va trouver seulement
les sources officielles (linux-source-2.6.10) et les patchs
(linux-patch-ubuntu-2.6.10) pas de paquets
linux-source-2.6.10-5-386. Et si l'on installe juste les sources
officielles, le module créé refusera de se charger ou vmware refusera
de s'installer vu qu'il n'a pas été compilé pour ce noyau précis (le
suffixe -5-386 fait toute la différence). On se retrouve donc a
compiler le noyau 2.6.10 et à utiliser ce noyau, pour pouvoir enfin
charger ce module.

Ce n'est pas super productif de compiler un nouveau noyau "pur" pour
des drivers alors qu'en plus Ubuntu s'est décarcassé pour intégrer les
meilleurs patchs.

La solution, c'est d'installer juste les fichiers d'entête (headers)
qui contiennent effectivement les infos nécessaires. Ce paquet colle
parfaitement a la version du noyau installé et donc les modules créés
se chargeront sans problèmes.

Compiler un nouveau noyau sous debian
-------------------------------------

#. D'abord, installer des paquets supplémentaires pour configurer le
   noyau l'interface gtk::

     sudo aptitude install libglib2.0-dev libgtk2.0-dev libglade2-dev

#. J'installe le paquet des sources du noyau 2.6.10, ainsi que le
   paquet de la commande make-kpkg::

     sudo aptitude install source-linux-2.6.10 kernel-package

#. Création d'un nouveau groupe src, ajout de jd, appartenance des
   sources du noyau au groupe src::

     sudo addgrp src
     sudo chgrp -R src /usr/src
     sudo adduser jd src
     newgrp src

#. Décompression des sources, création du lien pointant vers le noyau
   "de travail"::

     cd /usr/src
     tar xjf linux-source-2.6.10
     ln -s kernel-linux linux
     cd linux

#. Configuration du noyau en partant de la configuration du noyau actuelle ::

     cp /boot/config-2.6.10-5-386 .config
     sudo make-kpkg --initrd --revision=mykernel01 kernel_image
     sudo dpkg -i ../kernel*

