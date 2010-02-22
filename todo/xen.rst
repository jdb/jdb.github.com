
the Xen virtual machine hypervisor
==================================

install Xen
-----------

 1. install the xen hypervisor and kernel{{{
aptitude install xen-linux-system-2.6.18-4-xen-686 debootstrap
shutdown -r now}}}
 1. Enable network for the VM (though a bridge):{{{
sed -i "s/# \((network-script network-bridge)\)/\1/" /etc/xen/xend-config.sxp
xend restart}}}

quick start to building a VM
----------------------------

 1. create a partition {{{
lvcreate -n krusty -L 2G hd && mkfs.ext3 /dev/mapper/hd-krusty
mkdir /mnt/krusty && mount /dev/mapper/hd-krusty /mnt/krusty}}}
 1. install a minimum debian system: {{{
debootstrap lenny /mnt/krusty http://ftp.debian.org/debian/}}}
 1. configure the minimum debian system : {{{
chroot /mnt/krusty
aptitude install libc6-xen
cat > /etc/hostname <<.
krusty 
.
cat > /etc/fstab <<.
/dev/hda1       /           ext3    defaults        0       1
.
cat > /etc/network/interfaces <<.
auto lo eth0
iface lo inet loopback
iface eth0 inet dhcp
.
exit
umount /mnt/krusty
}}}
 1. create a "xen domain" ie a vm {{{
cat > /etc/xen/krusty <<.
name    = "krusty"
kernel  = "/boot/vmlinuz-2.6.18-4-xen-686"
ramdisk = "/boot/initrd.img-2.6.18-4-xen-686"
root    = "/dev/hda1"
disk    = [ 'phy:/dev/hd/krusty,hda1,w' ]
vif     = [ 'mac=00:16:3E:00:01:01']
memory  = 100
.}}}

Conclusion
----------

 1. test your virtual machine {{{
xm create -c krusty
#login as root
ping www.google.com
aptitude install less}}}
 1. give a permanent dhcp lease to that MAC address

packages
--------

`xen-linux-system-2.6.18-4-xen-686` is a cool package that installs a bunch of needed packages.
 * bridge-utils, iproute 
 * libatm1, libc6-xen 
 * linux-{image,modules,headers}-2.6.18-4-xen-686
 * xen-{hypervisor,utils}-3.0.3-1-i386-pae
 * xen-utils-common

Please, fill in the blank, what is the use those package??
 * linux-{headers,image,modules}-2.6.17-2-xen-686
 * xen-hypervisor
 * libatm1
 * iproute 
 * bridge-utils
 * xen-ioemu-3.0
 * redhat-cluster-modules-2.6-xen-686
 * spca5xx-modules-2.6-xen-686 
 * squashfs-modules-2.6-xen-686 
 * xen-docs-3.0
 * libc6-xen
 * xen-tools 
 * xen-utils{,-common}:: 


Questions
---------

 * http, backup, migration, xen tools and xen products???
 * Unclean dom0 shutdown can affects virtual machines???
 * Howto to debug a network pb with any virtual machines??? ex DHCP, restart the xen-bridge?

