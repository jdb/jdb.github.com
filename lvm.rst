
An upgrade safety net with the logical volume manager
=====================================================

It is the story of a website with files and a database which gets into
production and then, after a while, needs to have its schema corrected
and related files upgraded safely. As usual, it would have been better
to get the schema right from the beginning but as errors always happen
at some point, technologies such as the LVM snapshots exists so that
the website gets its invasive (read scary) upgrade but there is a good
safety net in case of a mess.

The idea is to take a **snapshot** of the *disk partition*: it is like
making a backup of a partition and copy it back later whenever
required, with the added benefit of :

- the backup is done in almost not time, it is *not* depending on the
  size of the disk,

- there is no actual copy of the blocks so it is very light on the
  io and space available,

- most importantly, even if the backup happens during a massive
  modification of the filesystem structure, the filesystem data
  structures are coherent.

It is not magic though, the snapshot itself is a partition and it
grows along when new data is added to the original partition to which
the snapshot is attached. *Make sure the snapshot partition is big
enough to contain the updates to the original partition or suppress
the snapshot partition before it gets full*.

Note that the operation needs to be done from the administrator
account.

A trick for fake physical partitions
------------------------------------

Before showing how to setup a logical partition with lvm, let's first
present a cool trick to create *virtual physical partitions*: it is
not related to lvm per se but it eases experimentation with RAID or LVM
without mangling a real disk.

With *losetup*'s loopback partitions, it is possible to turn a normal
file into a disk image device, available in */dev*. Here we create,
with *dd*, a file of 1.5 gigabyte called *loop1.raw* in the
current directory, and make it available under */dev/loop1* 

.. sourcecode:: sh

   ~# dd if=/dev/zero of=loop1.raw bs=1M count=40
   ~# losetup /dev/loop1 loop1.raw
 
   ~# grep loop /proc/partitions 
    7        1     ... loop1


There was no partitions available called *loop1* and it appeared after
the *losetup command*. We will set up the partition to use with lvm in
the next paragraph.

Setting up an logical volume
----------------------------

To represent LVM hot resize, hot backup or physical disk aggregation,
there are three object you need to be familiar with, and for each of
these objects, there is the corresponding shell commands for *creating*,
*listing* and *removing* said object.

`physical volume`: a physical partitions of one of the physical hard
   drive which has been allocated to lvm. Managed with *pvcreate*,
   *pvs* and *pvremove*. The *s* of *pvs* is for *show*.

`volume group`: aggregation of **physical volumes**. When I first read
   documentation about LVM, I thought the volume groups was meant to
   aggregate the logical partitions and data, but it is the other way
   round, they aggregate the real partitions. Managed with *vgcreate*,
   *vgs* and *vgremove*.

`logical volume`: volume is what you will use in the end with *mkfs*
   and *mount*. This is the device which look like the traditional
   partitions but with additional features like snapshots or resize on
   the fly. Managed with *lvcreate*, *lvs* and *lvemove*.

Use *pvcreate* from the *lvm2* package to initialise the partition for
use with lvm

.. sourcecode:: sh

   ~# pvcreate /dev/loop1
     Physical volume "/dev/loop1" successfully created
  
A disk can only be added once to a volume group, multiple physical
disks compose a *volume group*

.. sourcecode:: sh

   ~# vgcreate datadisks /dev/loop1
     Volume group "datadisks" successfully created

So far, the partitions available have not changed and the
*/dev/datadisks/website* partition does not exists. A logical volume
can now be created, it has a *name* and a *size* parameter and is inside a
*group*

.. sourcecode:: sh

   ~# lvcreate -n website -L 12M datadisks
     Logical volume "website" created
 
   ~# lvs
   LV      VG        Attr   LSize  Origin Snap%  Move Log Copy%  Convert
     website datadisks -wi-a...M

   ~# grep dm /proc/partitions && ls /dev/datadisks/website
    252 ... dm-0
   /dev/datadisks/website

Among the partitions, a new *dm* entry is shown (I'll bet it
stands for *device mapper*), the device is available in */dev*
contained in a directory named after the volume group.

As usual, the partition must be formatted and mounted to be integrated
to the filesystem

.. sourcecode:: sh

   ~# mkfs.ext4 /dev/datadisks/website > /dev/null
   ~# mkdir -p ./mnt/website && mount /dev/datadisks/website ./mnt/website


Design of an upgrade plan
-------------------------

Let's compose a dummy three-tier website, that we will have to
upgrade, corrupt, rollback, etc

.. sourcecode:: sh

   ~# touch ./mnt/website/database
   ~# touch ./mnt/website/index.html
   ~# add_new_user () { 
          echo "name:$1,age:$2" >> ./mnt/website/database ; } 

With the adapted amount of marketing and public relation, the website
is put in production and made available to the public. Everyday,
torrents of new users line up to subscribe

.. sourcecode:: sh

   ~# add_new_user alice 29
   ~# add_new_user bob 18
   ~# cat ./mnt/website/database
   name:alice,age:29
   name:bob,age:18

*Sparky the architect* have realised that the database schema must be
upgraded to include an *id* for each user. It should end up look like this::

   id=001,name:alice,age:29
   id=002,name:bob,age:18

Also, the website in production is not web2.0 enough, so a designer
has done a great job beautifying a new prototype, which is added to
the upgrade procedure. So the upgrade procedure is

.. sourcecode:: sh

   ~# upgrade_schema_and_website () {

         # Web changes
         touch ./mnt/website/{social-caramels.js,ponies.js,eye-candy.css}

         # API upgrade: now there is an id  
         add_new_user () { 
            echo "id:$RANDOM,name:$1,age:$2" >> ./mnt/website/database ; }

         # For the "db schema", you don't want to know ... 
         nl -n rz -w 3 ./mnt/website/database \
            | sed 's/\t/,/; s/^/if:/' > ./mnt/website/database.new
         mv ./mnt/website/database{.new,}
         } 

Rollback of a failed upgrade
----------------------------

The system administrator tunes a transaction API and convince the
operator to use it the day of the upgrade. Before doing any change,
the operator must use the command *transaction*. If all is well after
a few days of testing, the command *remove_snapshot* is used, else the
operator can use the *abort* function.

The transaction functions are built on top of the LVM snapshot

.. sourcecode:: sh

   ~# transaction () {
         lvcreate -s -n backup -L 24M  /dev/datadisks/website ; }
 
   ~# abort () {
         mkdir ./mnt/backup
         mount /dev/datadisks/backup ./mnt/backup

	 # tar cf - -C ./mnt/backup . | tar  x -C ./mnt/website
 	 rsync --del -a ./mnt/backup/ ./mnt/website/ ; 

	 add_new_user () { 
              echo "name:$1,age:$2" >> ./mnt/website/database ; } 
         }
 	
   ~# remove_snapshot () {
         umount /dev/datadisks/backup
         lvremove -f /dev/datadisks/backup ; }

.. what happens when you copy back the data from the backup which
.. records the modification from the original. Does the backup
.. partition size grows or shrink?

.. can the backup stop recording modification? maybe it is what
.. happens when the backup is mounted ...

.. mount de la partition de backup doit etre read only. What does write
.. means for the backup partitions?

The upgrade procedure requires the database to go read only, no new
users can be created. Comes the night of the upgrade

.. sourcecode:: sh

   ~# transaction
   Logical volume "backup" created

.. sourcecode:: sh

   ~# upgrade_schema_and_website

At dawn, the db looks like

.. sourcecode:: sh

   ~# cat ./mnt/website/database
   if:001,name:alice,age:29
   if:002,name:bob,age:18

Ouuuch man! it is corrupted, there is no 'id' column instead it is
written 'if' everywhere now and we have no clue why. We need to go
back to the lab, figure out what happened... What do we do now with
this mess now: we need roll back so that the production site can
continue. Easy, here is the command

.. sourcecode:: sh

   ~# abort

The abort is based on the ``lvcreate --snapshot`` and really is the
core of this article. Now, to control that the rollback went fine

.. sourcecode:: sh

   ~# cat ./mnt/website/database
   name:alice,age:29
   name:bob,age:18

   ~# ls ./mnt/website/ponies.js 2>&1 || true
   ls: cannot access ./mnt/website/ponies.js: No such file or directory

Ok, the situation is similar as before the upgrade. The service can be
restored. 

.. note::

  It is actually not easy to get the right options for ``rsync`` or
  ``tar`` for re-install the data of the backup. The version 2.02.57 of
  lvm with the device mapper hopefully integrated into the linux
  2.6.33 will be more convenient by integrating it to the
  ``lvconvert`` command of the LVM set of commands: no need for
  everyone to write (and debug) a custom ``abort`` function like we
  did. The new lvconvert command could be available in the
  distributions in the second half of 2010.


Fixing and re-applying the upgrade
----------------------------------

Three weeks later, many more users have been created

.. sourcecode:: sh

   ~# add_new_user robwilco 35
   ~# add_new_user DuncanMacLeod 539

   ~# cat ./mnt/website/database
   name:alice,age:29
   name:bob,age:18
   name:robwilco,age:35
   name:DuncanMacLeod,age:539

R&D has come up with a *complete* re-design of the upgrade procedure:
a snapshot and some *correct* database mangling commands. Only the
schema upgrade was modified

.. sourcecode:: sh

   ~# upgrade_schema_and_website () {

       # Same as before ...
       touch ./mnt/website/{social-caramels.js,ponies.js,eye-candy.css}

       # Same as before ...
       add_new_user () { 
         echo "id:$RANDOM,name:$1,age:$2" >> ./mnt/website/database ; }

       # Correction added here: substituted 'if' by 'id'
       nl -n rz -w 5 ./mnt/website/database \
          | sed 's/\t/,/; s/^/id:/' > ./mnt/website/database.new
       mv ./mnt/website/database.new ./mnt/website/database
       } 

   ~# upgrade_schema_and_website

   ~# cat ./mnt/website/database
   id:00001,name:alice,age:29
   id:00002,name:bob,age:18
   id:00003,name:robwilco,age:35
   id:00004,name:DuncanMacLeod,age:539

At dawn, the database is correct, the snapshot safety net was
thankfully not used. It is possible to confirm the upgrade by removing
the snapshot

.. sourcecode:: sh

   ~# remove_snapshot
   Logical volume "backup" successfully removed

Obviously, removing the snapshot does not impact the original partition

.. sourcecode:: sh

   ~# cat ./mnt/website/database
   id:00001,name:alice,age:29
   id:00002,name:bob,age:18
   id:00003,name:robwilco,age:35
   id:00004,name:DuncanMacLeod,age:539

We are done with this howto, to clean up after this exercice

.. sourcecode:: sh

   ~# umount ./mnt/website
   ~# lvremove -f /dev/datadisks/backup 2> /dev/null || true
   ~# lvremove -f /dev/datadisks/website
   Logical volume "website" successfully removed

   ~# vgremove datadisks 
   Volume group "datadisks" successfully removed

   ~# pvremove /dev/loop1
   Labels on physical volume "/dev/loop1" successfully wiped

   ~# losetup -d /dev/loop1
   ~# rm -r ./mnt/backup ./mnt/website loop1.raw


*Tue, 09 Feb 2010*

This article was verified with the wordish_ module.

.. _wordish: http://pypi.python.org/pypi/wordish
