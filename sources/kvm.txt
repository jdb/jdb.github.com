
=====
 kvm
=====

sudo aptitude install virt-manager

curl -L -O -C - http://cdimage.debian.org/debian-cd/5.0.3/i386/iso-cd/debian-503-i386-netinst.iso

sudo virt-manager

# The default en-us keymap is broken, once the image is installed,
# shutdown the image and edit the xml description to change it to fr

sudo virsh list --inactive
sudo virsh edit fedora
