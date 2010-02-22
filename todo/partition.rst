
=====================
 Partitioning a disk
=====================

Partition may serve several purpose depending on the use of the
machine. 

laptop with windows and linux
-----------------------------

You usually get windows installed on a partition spanning on the
entire hard drive. The next step is to install your prefered Linux
distro. During the partition step :

#. shrink the windows partition ie hda1 to 10 Go (installation CD for
   mandrake and ubuntu).

#. Then, make an 10 Go ext3 root partition for the linux (hda2).

#. Make a swap partition (hda3, 1 or 2 Go should be enough).

#. Make a vfat partition with the rest (hda4). The vfat partition will
   contain most of your personal data, documents, etc and will be
   read/writable by both OS.

Note:

* When the Unix is set up, you can mount the vfat partition in
  /mount/echange. Make it read/write for you user through the
  /etc/fstab::

    grep vfat /etc/fstab
    /dev/hdb    /mnt/echange    vfat uid=jd,gid=jd    0    0

  Make symbolic links in your home toward the main directories of this
  mount so that data is available quite transparently ::

    cd && ln -s /mnt/echange/muzak
    cd && ln -s /mnt/echange/photos
    
* Configure windows so that the 'My Documents' folder be on this
  fourth partition.

* It can be convenient to configure your firefox and thunderbird
  profiles on windows and linux to point to the same directory on the
  vfat partition. Then you may access the same mails, bookmarks,
  saved password from your Unix or your windows. Be real sure to use
  same versions for firefox under linux and windows (same for
  thunderbird).

* Due to vfat's limitations, you can't trust the permission and
  owners on the partition's files (you can assign temporary ones in
  /etc/fstab)

Server secured though partitions
--------------------------------

Partitions are a part of making a robust server.

Say your web site go wild and write GB and GB into /var. If /var is on
the root partitions, then the root partition will eventually get
full. The system, which needs some empty hard drive space on the root
partition will function poorly. If /var and / are on separate
partitions, the web site will fill its partitions without much
affecting the system. Other examples: users can fill their home
directory with downloads, loaded server may fill /var/log.

lvm is cool because you can adjust/adapt the size of the logical
volumes without affecting existing data on the partitions ("hot
resize").

#. Physically : 2 40 GB hd, sda et sdb sont chacun partitionnés en 2,
   100 Mo et 40Go (in the BIOS)

#. Raid 1 : containers #1: 2 100 MB partitions, containers #2: 2 40 GB
   partitions (in the BIOS)

#. LVM - physical volum : container #2 Raid de 40 GB

#. LVM - volume group : contains the 40 GB pv

#. LVM - volume logique : root (5 Go), home (10 Go), var (5 Go), log(5
   Go)

#. Filesystem : /boot sur la partition Raid de 100 Mo, / sur root,
   /home sur home, /var sur var et /var/log sur log

It is mandatory two create two real partitions, among them, one is not
on LVM and it contains /boot. The reason comes from Grub which does
not yet read LVM partitions, hence, grub will not be able to read the
kernel to boot.

My desktop PC
-------------

* free real partitions for testing new OS

* several OS and LANs with Xen on the main Debian

* tons of pictures, muzak spanning extra hd

* small partitions on every extra hd on which I duplicate old archives

* hda: system hard drive

  ========= =========== ======= ======
  partition mount point fs type size
  ========= =========== ======= ======
  hda1      /boot       ext3    500M 
  hda2      edgy  	ext3 	10 Go
  hda3      bsd   	bsd  	10 Go
  hda4      vg:sys 	lvm  	61 Go
  ========= =========== ======= ======

  hda4: pvs dans vg sys: lvm debian, home, xen itchy, xen scratchy


* hdx: small backup + data

  ========= ============ ======= =====
  partition mount point  fs type size
  ========= ============ ======= =====
  hdx1      backup    	 ext3  	 10Go 
  hdx2	    vg:fnac   	 lvm   	 \*   
  ========= ============ ======= =====
    
Notes
-----

* vfat is read/writable by Linux and Windows, vfat does not allow file
  permissions (hence multi-user filesystem), nor links.

* ntfs is not writable by Linux (Linux reads tons of cool filesystems,
  but ntfs is undocumented). The captive library may help you, it is a
  wrapper around the windows ntfs driver.

* if you have a windows, then you may need a vfat partition so that
  you can share data (or use a usb drive).

* grub cannot read a "lvm formatted" /boot (hence cannot boot on it),
  keep a separate partition for /boot.

* an lvm / cannot be read by a pristine linux kernel when it boots
  because it hasn't loaded yet the lvm stuff (Debian has patched the
  initrd, though it is not really a problem)

* either you can make a backup partition in pure ext3 (no lvm) so that
  it if you take the hard drive off, you simply need a Live CD to read
  the data, or you can mirror partitions with evms on several disks.

