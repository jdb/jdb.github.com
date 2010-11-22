
:author: Alexandre Rubini
:translator: Jean Daniel Browne
:copyright: Reproduit avec l'autorisation des éditions Linux Magazine Italie.

======================
 Les pseudo-terminaux
======================

Ces quelques pages expliquent ce que sont les pseudo terminaux (pty) et
décrivent les interfaces de programmation exportées par le noyau.

Les pseudo terminaux sont un composant extrêmement important des
systèmes compatibles Unix. Le pseudo-terminal est le mécanisme à la
base de xterm, kterm et des autre émulateurs de terminal mais aussi à
la base de sshd, rshd, telnetd et autres systèmes de login à
distance. C'est encore le mécanisme à la base des librairies et
applications en mode texte, comme ncurses ou ou emacs en mode console.

.. todo::

   Is it an IPC? yes, but which supports slow interactive transfer and
   control character?

Les codes présentés ont été testés sur linux-2.6.5; mais le noyau n'a
pas subi de changements important dans ce domaine depuis le noyau 2.4,
ces codes devraient fonctionner sans difficultés.

Qu'est-ce qu'un pseudo terminal?
--------------------------------

L'acronyme pty signifie *pseudo-teletype*, ce sont les
*pseudo-téléscripteurs* historique en français. Du point de vue d'un
noyau, un terminal (ou tty pour *teletype*) est un fichier spécial de
type caractère sur lequel peux être connecté soit un terminal physique
(les vt100 et vt320 étaient composés d'un clavier et écran) soit une
application qui envoie et reçoit des données de manière interactive
des utilisateurs. Le sous-système de terminal du noyau transfère les
données vers l'application vers ou depuis un interpréteur de commandes
ou d'autres programmes interactifs. Comme les vt100 ont disparus
depuis longtemps et que les vt320 sont en voie de disparition, de nos
jours quand on parle de terminal, on fait indistinctement référence
soit au fichier périphérique, soit à l'application interactive qui y
est connectée.

.. todo::

   missed a paragraph here?

.. todo::

   difference between tty and pty?

.. todo::

   represent graphically a pty /dev/tty1, a kernel and a bash and a
   keyboard (I mean the creator of the ctrl-d signal)

Un exemple de fichier périphérique terminal est le port serie
(/dev/ttyS0 ou /dev/ttyUSB0), un autre exemple est le terminal virtuel
de la console de texte (/dev/tty1, /dev/tty2 etcaetera), un autre
encore est la fenetre de xterm ou d'un autre emulateur de terminal
(/dev/ttyp0 ou /dev/pts/0).

.. todo::

   Are pseudo terminal and emulateur de terminal the same word? if
   yes, be consistent and tell everyone

Dans tout ces cas, le fichier special dans /dev offre aux processus
qui accèdent aux fonctionnalités specifique d'un terminal les
parametres *termios* (terminal input output settings), ou plus
précisement, ces paramètres ennuyeux mais important, relatifs a la
vitesse de la transmission, a la parité, aux conventions sur les
signaux de fins de fichiers et tant d'autres mais aussi l'affectation
de fonctionnalite speciale a chaque caractere. Il est possible de
simuler une fin de fichier a travers ctrl-D ou arreter un processus
par ctrl-C seulement parce que ce caractere rejoint un fichier special
associé a un terminal. Chaque utilisateur peut choisir quels sont les
caracteres speciaux et aucun de ces caractères n'a une signification
speciale en dehors du contexte du terminal.

Pour lire ou modifier la configuration termios d'un terminal, les
fonctions de la librairie *tcgetattr* et *tcsetattr* (terminal control
get/set attributes) ou les commandes *stty* (set tty), en gardant en
memoire que la commande agit seulement sur l'entrée standard::

    burla% stty
	   speed 38400 baud; line = 0; erase = ^H; -brkint -imaxbel
 
    burla% stty < /dev/ttyS0
	   speed 9600 baud; line = 0; -brkint -imaxbel

    burla% stty < /etc/passwd
	   stty: entrée standard: Ioctl() inappropré pour un périphérique

Dans les deux cas, la configuration est lue depuis le noyau ou écrite
dans le noyau au travers de l'appel systeme ioctl, avec les commandes
TCGETA, TCSETA et autres commandes de la meme famille, dont
l'implementation est dans le fichier divers/char/tty_io.c

.. todo::

   list the features of the pty, char par char, window resize, control
   resize, système d'évènement.

Lors du lancement d'une application interactive comme bash dans un
émulateur de terminal, bash est lié a la partie maitre du terminal
et

.. todo::

   missed a paragraph here?


Qu'est-ce qu'un couple de pseudo terminal
-----------------------------------------

Alors qu'un terminal comme /dev/ttyS0 est clairement associe a un
peripherique (le port serie) qui peut etre connecte a un terminal
physique, le dispositif associe a la fenetre de xterm ne permet aucun
peripherique materiel et les donnees echangee entre l'interprete de
commandes et le fichier special dans /dev/ sont gere par un autre
processus sur la meme machine, c'est xterm dans notre cas.

Dans toute les situations dans lesquelles il est necessaire d'executer
un processus a l'interieur de l'abstraction "terminal" sans faire
l;usage d'une reelle interface materielle, il est possible de
s'abonner au mecanisme des pseudo terminaux, mecanisme selon lequel a
chaque pty est associe a un autre fichier special qui se comporte
comme si il etait l'autre extremite du cable serie. Les deux fichiers
speciaux forment ce que l'on appelle un couple de pseudo terminaux ou
plus simplement un couple de terminaux ou 'tty pair'.

Les deux composants du couple se comportent comme un tube
bidirectionnel (un *pipe*) et l'un sera 'maitre' alors que l'autre
sera esclave. Le comportement des fichiers speciaux associe, n'est pas
completement symetrique de la meme maniere que les descripteurs de
fichiers associé a un tube ou a une socket: le terminal esclave est
typiquement un terminal reel, mais il peut etre ouvert seulement apres
l'ouverture du maitre qui lui est associe; le terminal maitre, par
contre, ne se comporte pas completement comme un terminal et ne peut
etre ouvert qu'une seule fois. ::


    Ouverture d'une couple de terminaux
    #include <stdlib.h>
    #include <fcntl.h>
    #include <errno.h>
    #include <sys/types.h>
    #include <sys/ioctl.h>
    #include <sys/stat.h>
    
    int main()
    {
        int i, j;
        char devname[]="/dev/pty--";
        char s1[]="pqrstuvwxyzabcde";
        char s2[]="0123456789abcdef";
        int fds, fdm = -1;
    
        for (i=0; fdm<0 && i<16; i++) {
            for (j=0; fdm<0 && j<16; j++) {
                devname[8] = s1[i];
                devname[9] = s2[j];
                if ((fdm = open(devname, O_RDWR)) < 0) {
                    if (errno == EIO) continue;
                    exit(1);
                }
            }
        }
        devname[5]='t';        //   /dev/ttyXY 
        if ((fds = open(devname, O_RDWR)) < 0)
    	exit(2);
        exit(0);
    }
    
L'interface historique
----------------------

Historiquement les pseudo-terminaux, maître et esclave, existaient
dans le répertoire /dev. En cas d'absence, ils peuvent être créés par
la commande ``/dev/MAKEDEV pty``. Les terminaux esclave portent le
numero majeur 3 et leur noms sont par exemples ``/dev/ttyp0``; les
terminaux maîtres portent le numéro majeur 2 et leur noms suivent la
rêgle ``/dev/ptyp0`` où chaque *p* signifie *pseudo*. Le code pour
gérer ces peripherique est optionel dans le kernel, et est inclu par
la clé è`CONFIG/LEGACYPTYS``.

Les noms des fichiers spéciaux associe a chaque couple de terminal
different par leur deux derniers caracteres, chacun d'eux pouvant
prendre 16 valeurs pour un total de 256 paires. Le bref programme
legacy.c dans l'encadre 1 montre la procedure classique d'ouverture
d'une paire de terminal, cherchant le premier maitre disponible puis
utilisant le slave associe. Si un maitre est deja utilisé, open
retourne EIO et la boucle recommence. Si le support des pseudo
terminal n'est pas compile, alors le premier open retournera ENODEV,
si le fichier special n'existe pas le premier open retournera ENOENT
et dans les deux cas, la boucle s'arrete. Le comportement du programme
peut etre observe avec strace.

UN programme qui utilise les terminaux pour resoudre une tache devra
naturellement faire d'autres operation comme changer le proprietaire
et les permissions d'acces au fichier special pour refleter
l'utilisateur qui en a pris le controle et les preferences (voir la
page d'exemple de mesg par exemple).

Les mecanismes avec paire de fichier decris au dessus ont neanmoins
quelque probleme non negligeable: le processus qui ouvre une session
doi etre privilegie (pour changer le proprietaire du terminal),
l'assignation du terminal n'est pas atomique et donne lieu a une
session critique, le scanning des dispositif pour en trouver un
disponible peut un retard indesiré.

Enfin, 512 fichier speciaux dans /dev sont souvent une entrave, et
cela pose un probleme avec les machines embarquées. Par exemple, le
systeme de developpement du processeur etrax est livre avec une
distribution avec le repertoire /dev/sur un dispositif en lecture
seulement ou ont ete cree seulement trois paires de terminaux pour ne
pas gacher l'espace limite a disposition. La consequence est que le
server telnet ne peut accepter plus de trois utilisateurs en meme
temps.  et il n'est pas possible de faire travailler plus de trois
etudiant en meme temps, a moins de reprogrammer la memoire flash avec
une version personnalisée du systeme.

L'interface actuelle
--------------------

Chacun des problemes relatif aux terminaux virtuel ont éte resolu
simplement par l'observation que le maitre est ouvert une seule fois,
il est alors possible d'implementer un seul fichier special pour gerer
l'ensemble des maitres, faisant ce que le noyau, une fois le fichier
ouvert, l'associe a un terminale maitre qui pourra etre requeté sur le
nom du fichier esclave associe. Par contre, il n'est pas possible
d'unifier tout les terminaux fils en un seul fichier parce que les
autres processus doivent pouvoir ouvrir les terminaux esclave en cours
d'utilisation. C'est de cette maniere que fonctionne les programme de
la famille de talk, qui est encore retenu comme meilleur qu'IRC dans
certain contexte.

Cette approche est specifiée dans le standard *unix98*, qui a défini une
série de fonctions pour ouvrir et configurer les terminaux.
L'utilisation de ces fonctions cache les détails de chaque
implémentation, comme les noms des fichiers spéciaux à utiliser ou le
mécanisme utilisé pour changer le propriétaire du terminal esclave
(souvent un tel mécanisme est un appel à setuid).

Cette infrastructure a été implémenté dans les systêmes GNU/linux;
mais une autre est aussi utilisée: au lieu d'utiliser le fichier
special situé dans /dev pour les terminaux esclave, un systême de
fichiers adaptés a été créé de telle sorte que le noyau doit rendre
visible les terminaux esclave en réponse aux accès au terminal maitre,
pour éviter que l'intégration du systême doivent choisir entre occuper le
precieux espace sur le disque ou limiter arbitrairement le nombre de
session. L'implémentation du systême de fichier entre code et données,
pese moins de 10KB et s'active grace a l'option CONFIG_UNIX98_PTY ::

    #include <stdio.h>
    #include <stdlib.h>
    #include <fcntl.h>
    #include <sys/types.h>
    #include <sys/ioctl.h>
    #include <sys/stat.h>
    
    int main()
    {
        int n;
        int zero=0;
        char name[16];
        int fds, fdm;
    
        if ((fdm = open("/dev/ptmx", O_RDWR)) < 0)
    	exit(1);
    
        if (ioctl(fdm, TIOCGPTN, &n) < 0)
    	exit(2);
        sprintf(name, "/dev/pts/%i", n);
        if (ioctl(fdm, TIOCSPTLCK, &zero) < 0)
    	exit(3);
    
        if ((fds = open(name, O_RDWR)) < 0)
    	exit(4);
        exit(0);
    }
        

L'ouverture et la configuration d'un couple de terminaux à la manière
*unix98* est effectuée à travers les fonctions de la librairie
*getpt*, *grantpt*, *ptsname*, *unlockpt* pour lesquelles les pages de
manuel sont disponibles pour plus de détails. Le programme *open.c*
montre par contre une approche de plus bas niveau qui utilise les
mecanismes du noyau Linux aux depends de la portabilité.

Dans ce cas, le terminal maitre est appele /dev/ptmx (pseudo-tty
multiplexer) et les terminaux esclaves sont situés dans le directory
/dev/pts où a été monté le système de fichier *devpts*. Les deux
commandes ioctl utilisee dans le programme d'exemple sont utilise pour
demander au systeme le numero du terminal esclave a ouvrir (TIOGPTN)
et pour le debloquer, autorisant l'acces a l'esclave (TIOCPTLCK:
terminal ioctl pseudo terminal lock). Le terminal esclave disparait
automaitquement du systeme de fichier son utilisation est
terminée. Si l'on execute open avec strace, l'on verra que le
programme ouvre un terminal esclave qui n'existe plus une fois
l'execution terminée.

Le systeme de fichiers devpts etait deja disponible dans les linux2.2
et n'a pratiquement pas evolue dans la version 2.6, seulement par
l'ajout des attributs etendus, une fonctionnalite disponible dans les
principaux systeme de fichiers mais en dehors du sujet de cet
article. Normalement, le systeme de fichier devpts est monte lors du
demarrage de la distribution, bien qu'il ne soit pas present dans
/etc/fstab. Il est possible de demonter /dev/pts seulement apres avoir
ferme tout les pseudo terminal en cours d'utilisation; le systeme
continuera a fonctionner aec le mecanisme precedent (a la condition
d'avoir le fichier special dans /dev et le support relatif dans le
noyau). Il est toujours possible de remonter /dev/pts et de faire
cohabiter les deux systemes. ::

    burla% who
	rubini   ttyp1        Apr  6 09:43 (ostro.i.gnudd.com)
	rubini   ttyp2        Apr  6 09:43 (ostro.i.gnudd.com)
	rubini   pts/16       Apr  6 09:43 (ostro.i.gnudd.com)

::

  #include <stdlib.h>
  #include <unistd.h>
  #include <pty.h>
  #include <utmp.h>
  #include <sys/time.h>
  #include <sys/wait.h>
  #include <sys/types.h>
  
  int main()
  {
      int fdm, fds;
      int pid, i;
      fd_set set;
      char buf[64];
      
      if (openpty(&fdm, &fds, NULL, NULL, NULL))
  	exit(1);
      if ((pid = fork()) < 0)
  	exit(2);
      if (!pid) {
  	// child 
  	close(fdm);
  	login_tty(fds);
  	execl("/bin/sh", "sh", NULL);
  	exit(3);
      }
      /* father: copy stdin/out to/from master */
      close(fds); system("stty raw -echo");
      FD_ZERO(&set);
      while (waitpid(pid, &i, WNOHANG)!=pid) {
  	FD_SET(0, &set);
  	FD_SET(fdm, &set);
  	select(fdm+1, &set, NULL, NULL, NULL);
  	if (FD_ISSET(0, &set)) {
  	    i = read(0, buf, 64);
  	    if (i>0) write(fdm, buf, i);
  	}
  	if (FD_ISSET(fdm, &set)) {
  	    i = read(fdm, buf, 64);
  	    if (i>0) write(1, buf, i);
  	}
      }
      system("stty sane");
      exit(0);
  }
  
L'execution de sh dans un nouveau terminal
------------------------------------------

Le programme openpty dans l'encadre 3, ouvre une paire de terminaux et
execute un interpreteur de commande a l'interieur de l'esclave. Pour
simplifier et raccourcir le code, les fonctions openpty et login_tty
sont utilisée. Ces fonctions font partie de la libutil, ils ne font
pas rigoureusement partie de la libc mais ont ete rendu possible pour
eviter que chaque application doivent les reimplementer. Le makefile
que j'ai utilise, donc, est compose de ces deux regles::

	 CFLAGS = -ggdb -Wall
	 LDFLAGS = -lutil

Une fois ouvert la paire de terminaux, le programme cree un processus
fils auquel est assigne le nouveau terminal esclave comme terminal de
controle, avant d'executer sh. Le processus pere, par contre, s'occupe
de copier son entree standard sur le terminal maitre et tout ce qui
sort du terminal maitre sur sur sa sortie standard.

La solution obtenue est celle represente sur la figure 1, dans
laquelle les fleches entrante et sortante des processus representent
les fichiers standards de input et d'output alors que la ligne bleue
sortant de openpty represente les fichiers ouverts vers le terminal
maitre. Mais puisque l'input standard et l'output de openpty seront
probablement en execution a l'interieur d'un autre terminal (la
console, xterm o comme dnas mon cas, rshd, a son tour controle par rsh
a travers un xterm), dont il est necessaire de configurer le terminal
invite pour permettre l'utilisation interactive (un caractere a la
fois). de l'interprete de commande invoque dans le nouveaux terminal
esclave, c'est pour cela qu'est utilise la commande stty presenté
precedemment.

Openpty fonctionne soit avec les terminaux legacy, soit avec devpts,
en ce que la fonction de la librairie utilisee dans le code demontrer
dans legacy.c repose sur le la methode standard de unix98 ::


	burla% tty
	     /dev/ttyp0
	burla% ./openpty
	sh-2.05a$ tty
	     /dev/ttyp1
	sh-2.05a$ exit
	     exit
	burla% sudo mount -t devpts none /dev/pts
	burla% ./openpty 
	sh-2.05a$ tty
             /dev/pts/7
	sh-2.05a$ exit
	burla% tty
	     /dev/ttyp0


Utilisation de PPP sur un pseudo terminal Les pseudo terminaux se
pretent aussi a des usages non conventionnels, profitant de leur
complete equivalence, au niveau logiciel avec un port serie, ou un
modem.

Le protocole (PPP mais aussi SLIP) est implementé avec une discipline
de ligne, un module logicielqui peux etre utilise sur n'importe auel
type de termial. La discipline de ligne a pour but de discipliner le
comportement du systeme en ce qui concerne les données qui rejoigne
le noyau e provenance du terminal, en plus de permettre l'envoi de
donnees vers le terminal. Une discussion approfondie de la discipline
est disponible dans l'article sur www.linux.it/kerneldocs/serial.

Mais si PPP peut travailler sur n'importe quel type de terminal, il
est alors possible de faire une connexion point a point entre deux
machines distantes, a condition de pouvoir creer une paire de
terminaux sur chacune des deux machines. Sur la figure 2 est
represente la maniere pour realiser telle connexion dirigeant le
protocole dans un canal ssh a la place d'un port serie est cela est
traditionnellement fait avec PPP. Chacuns des deux PPPD est mis en
communication avec avec un terminal esclave, qui par son logiciel est
indistingable d'un modem. et les deux processus ssh client et server,
s'occupent de faire le pont entre le terminal maitre et le canal
chiffre sur le protocol IP.

figure 2

Le code pour realiser une telle structure de processus est visible
dans l'encadre 4, cette fois ecrite dans le langage ettcl (une version
de TCL modifiée pour pouvoir faire fonctionner le systeme
EtLinux). Il se trouve sur internet une version de ppptunnel ecrite en
perl, et il est immediat d'ecrire cet outil dans n'importe quel
langage qui supporte l'ouverture d'une pair de terminal. Le choix du
langage n'influence que de maniere annexe la realisation parce que le
programme doit seulement connecter les fichiers descriptor et rendre
le controle aux deux pppd, dans un cas a travers ssh.

.. code-block:: c

    #!/usr/local/bin/ettclsh
    # -*-tcl-*-
    
    if [llength $argv]!=3 {
        puts stderr "use: \"$argv0 <remotehost> <local-IP> <remote-IP>\""
        exit 1
    }
    foreach {host ip1 ip2} $argv {}
    
    sys_ttypair master slave
    if ![set pid [sys_fork]] {
        # child
        after 1000
        sys_dup $slave stdin
        sys_dup $slave stdout
        close $slave; close $master
        set ttyname [file readlink /dev/fd/0]
        sys_exec sudo \
    	    pppd debug local $ip1:$ip2 nodetach noauth lock $ttyname
        exit
    }
    # father
    sys_dup $master stdin
    sys_dup $master stdout
    close $master; close $slave
    sys_exec ssh -t $host sudo \
    	pppd debug local $ip2:$ip1 nodetach noauth lock /dev/tty
    
* role d'un terminal (caractere par caractere, transmission de signaux)

* qu'est il possible de faire sur terminal qui n'est pas possible de faire

* difference venant de expect

* liens entre les processus fils et pere et terminaux maitre et esclave

Le role de ppptunnel est d'ouvrir une paire de terminal (dans le sous
système tty sur la figure) et d'appeler fork. Le processus fils ferme
le terminal maitre et execute pppd sur son terminal esclave; le
processus pere ferme le terminal esclave et excute ssh, en specifiant
sur la ligne de commande l'execution de pppd sur la machine distante
apres l'ouverture du terminal de controle (qui est une autre paire de
terminaux, specifie avec l'option -t).

Pour que la commande puisse s'executer telle qu'expliqué dans ce
paragraphe, il est nécessaire que l'utilisateur local soit autorisé à
se connecter via ssh sur la machine distante et que sudo puisse
fonctionner sans mot de passe sur chacune des machine, mais il est
possible de composer le mot de passe relatif a ssh et a sudo sur le
terminal dans lequel s'execute ppptunnel; et au lieu de nécessiter que
le sudo distant ne demande pas de mot de passe. Au niveau kernel,
cette connexion repose sur les modules normaux de PPP: ppp_generic,
ppp_async et les modules de compression.





