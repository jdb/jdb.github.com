
============
 hard drive
============

Two interesting questions with hardware elements: Is it working? and
is it performant? A failing hardware will show bad performances,
nevertheless, two functioning hard drives may offer different quality.

For disks, for the first question, there is *smartd* and *badblocks*,
for the second question, there is *dd*, *hdparm* and the *disk* test
suite of Phoronix.


Diagnose a bad hard drive
=========================

*I have a feel that my hard drive died, how to decide if the hard
drive is good for the trash*

Smartctl
--------

*SMART* is a standard technology which has been implemented into every
hard drive for many years, this technology is used for
example, by the HP rescue boot disk. We are going to query our disk
with the *smartctl* tool under linux.

Several kind of tests
---------------------

First thing to do: request the disk to activate smart: ``smartctl -s
/dev/sdb``

Il y a 4 types de tests, les offline, les shorts, les longs et les
conveyance. Ils sont lancés, respectivement avec la commande ::

  smartctl -t offline /dev/hda
  smartctl -t short /dev/hda
  smartctl -t long /dev/hda
  smartctl -t conveyance /dev/hda


Reading a test result
---------------------

http://www.the-little-things.net/?p=35

Various parameter can be read :

There are two categories of parameters: 

pre-fail

old age

There is another property available for each parameter: either the
value is updated continuously, of the value is updated when a test is
run. Example

smartctl -a /dev/hda affiche un tableau de resultat.

On lit dans la colonne "updated" qu'il y a deux catégorie de
paramètres qui sont updated "always" et ceux qui sont updated
"offline". Ceux qui sont "always" sont scrutés en permanence. Les
"offlines" sont mis a jour grâce au tests.

On lit la valeur du paramètre dans la colonne "value" (en %). La
colonne "worst donne la pire valeur du paramètre depuis la mise en
fonctionnement du disque (ou de l'activation de SMART?). La colonne
"threshold" donne le seuil en dessous duquel le disque est noté comme
failing.

La colonne "raw_value" indique la valeur brute avant qu'elle n'ait été
ramenée à 100 dans la colonne value. On peut y lire le nombre de
blocks réalloués, la température du disque, la durée pendant laquelle
le disque à été allumé jusqu'a maintenant ...

Il y a deux types de paramètres, ceux qui donne une indication d'un
crash imminent ou non (les paramètres notés Pre-fail dans la colonne
"type") et ceux qui dénotent un disque anciens (notés Old_age).

La colonne "when_failed" indique si le paramètre est failing en ce
moment ou dans le passé. Si la valeur de la colonne worst est
supérieure à la valeur de la colonne threshold, alors le paramètre n'a
jamais été failing et la colonne contient un tiret.

Les paramètres Old_age ont un seuil de 0. La valeur de ce paramètre ne
pourra jamais passer sous le seuil ce qui implique qu'un disque ne
sera jamais "failing" a cause d'un paramètre Old_age. Seuls les
paramètres Pre-fail sont utilisé pour statuer sur le disque. Les
colonnes threshold et when_failed ne sont pas pertinent pour les
paramètres old age.



How to do *incremental backups*, now? How to *ghost the system* or
learn how you can make a partition or a *device bootable*. You may
wish to do RAID1 hotpluggable RAID1 disks.

How to get several kind of smartd tests done regurlarly?? and links
with syslog.

Performances with hdparm and dd
===============================

You can use hdparm (hard disk parameters). It can be used for setting
or querying several parameters such as consumption mode, standby
timeout, drive geometry. With option `-t -T`, we get a performance
test, the output is the read speed in megabyte per seconds. Do the
test three time, on an inactive system, the third result is the more
accurate::

  lisa # hdparm -t -T /dev/sda
  /dev/sda:
   Timing cached reads:   2636 MB in  2.00 seconds = 1319.19 MB/sec
   Timing buffered disk reads:  172 MB in  3.01 seconds =  57.09 MB/sec

The simple ``dd`` command line tool is also helpful::

  lisa # dd if=/dev/zero of=toto bs=1024 count=500000
  500000+0 records in
  500000+0 records out
  512000000 bytes (512 MB) copied, 11,5127 s, 44,5 MB/s

The results varies between 44.5 and 57 MB per seconds value is good
for a laptop. For a server, performance can be 50 MB/s. On a NAS, we
were having performances problem, hdparm would tell read performance
of only 7MB/s.

Performance with Phoronix *disk* test suite
===========================================

Phoronix is heavier to install and longer to run, but is it simple to
do. This page explains how to install and set up Phoronix.

To install the *disk* test suite::

    phoronix install disk
    # the tests composing the suites are fetched and compiled
    # this can take 10 minutes

    phoronix batch-run disk
    # I got a 684 TPS for pgbench, 140 TPS for PostMark, 25MB/s  for iozone
