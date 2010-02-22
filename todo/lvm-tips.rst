Logical volume manager
======================

Create an lvm partition bigger than two physical partitions
-----------------------------------------------------------

These commands can be copied and pasted with no ill effects. They will
not operate on your real hard drive partitions but on loop partitions.

#. create fake partition just for demonstration purpose with losetup::

     ~# sudo -s
     ~# dd if=/dev/zero of=hda1 bs=1M count=1G
     ~# dd if=/dev/zero of=hda2 bs=1M count=1G
     ~# losetup /dev/loop1 hda1        # for demonstration purpose, I create two fake 
     ~# losetup /dev/loop2 hda2        # partitions from newly created files with losetup.


#. At this point, there are two unused partitions. We can merge them
   into one::

     ~# pvcreate /dev/loop1
       Physical volume "/dev/loop1" successfully created
     
     ~# pvcreate /dev/loop2
       Physical volume "/dev/loop2" successfully created
     
     ~# vgcreate datadisks /dev/loop2 /dev/loop1
       Volume group "datadisks" successfully created
     
     ~# lvcreate -n muzak -L 1500M datadisks
       Logical volume "muzak" created

#. The partition ``/dev/mapper/datadisks-muzak`` is free, let's create a
   filesystem and put some file on it::
      
     ~# mkfs.ext4 /dev/mapper/datadisks-muzak
     ~# mkdir /mnt/muzak && mount /dev/mapper/datadisks-muzak /mnt/muzak
     ~# dd if=/dev/zero of=metronomy bs=1M count=1300
     ~# du -sh metronomy
       1300M     metronomy
     ~# cp metronomy /mnt/muzak

   From two partition of 1G, we created a *logical volume* of 1.5G in
   which we copied more data (1.3G) than available on each of the
   partitions taken separatly.

#. cleaning up::

     ~# umount /mnt/muzak

     ~# lvremove datadisks/muzak
     Do you really want to remove active logical volume "muzak"? [y/n]: y
       Logical volume "muzak" successfully removed
     
     ~# vgremove datadisks
       Volume group "datadisks" successfully removed
     
     ~# pvremove /dev/loop1 /dev/loop2
       Labels on physical volume "/dev/loop1" successfully wiped
       Labels on physical volume "/dev/loop2" successfully wiped
     
     ~# ### lvm cleanup is done by now, let's clean the fake partitions
     ~# losetup -d /dev/loop2
     ~# losetup -d /dev/loop1
     ~# rm hda{1,2} metronomy -r /mnt/muzek 




Resetting the filesystem after an lvm hot resize resize
-------------------------------------------------------

You may need the following so that lvs and df -h agrees on the disk sizes ::

  umount /dev/mapper/fnac-fnac
  e2fsck -f /dev/mapper/fnac-fnac
  resize2fs /dev/mapper/fnac-fnac
  
.. question 

Is the umount necessary ?

Mounting a logical volume from a livecd
---------------------------------------

You cannot boot a live CD and expect the logical volume to be "mount
ready" as is a standard ext4. You need to type ::

  vgscan --mknodes
  vgchange -ay

Now you're set ::

  lvscan
  mount /dev/mini/root /mnt/

Also, I could not ``vgscan``, with the feisty live even after having
installed ``lvm2`` (``Unable to mount drive ('LVM2_member')``, and
``No program “vgscan” found for your current version of LVM``). I had
to use the Knoppix liveCD v5, instead.

See also
--------

- http://www.debian-administration.org/articles/410
- http://www.linuxdevcenter.com/pub/a/linux/2006/04/27/managing-disk-space-with-lvm.html
- http://www.howtoforge.com/linux_lvm
- http://tldp.org/HOWTO/LVM-HOWTO/

