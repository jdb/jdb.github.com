

tips
====





nice bash prompt ::

  PS1='\[\033[00;32m\]\u@\h \[\033[00;33m\]\W \[\033[00m'}}}


set local time on a remote system and MOBO ::

 
  ssh $i "date -s $(date) && hwclock --systohc"}}}

given a ip dest and port dest, set the src port ::

  sudo iptables -t nat -A POSTROUTING -p tcp -d 192.168.1.10 --dport 10000 -j SNAT --to-source 192.168.1.11:8000

dos2unix ::
 
  sed -i 's/.$//' file.txt

substitute the line below a given pattern::

  sub_below () { sed -r "h; N; s/^(.*$1.*\n).*/\1$2/; P; D" $3  ; }
  echo -e 'a\nb\nc\nd' > myfile
  sub_below a Z myfile
  sub_below b Z myfile



When you see the following whinings in a chroot, it is because the
environment still point to the system locales with the locales files
missing in the chroot ::

  perl: warning: Please check that your locale settings:
          LANGUAGE = "fr_FR.UTF-8",
          LC_ALL = "fr_FR.UTF-8",
          LC_CTYPE = "fr_FR.UTF-8",
          LANG = "fr_FR.UTF-8"
      are supported and installed on your system.
  perl: warning: Falling back to the standard locale ("C").
  locale: Cannot set LC_ALL to default locale: No such file or directory
  /usr/bin/locale: Cannot set LC_CTYPE to default locale: No such file or directory
  [ ... ]

  # Set the locale for the system in `/etc/environment`, and re source

  cat >> /etc/environment <<EOF
  LANG="C"
  LANGUAGE="C"
  LC_CTYPE="C"
  LC_ALL="C"
  EOF

Useful regexp::

  # Validation de paramètre numérique 
  echo '12?3 a,' | grep   -o '[^[:alnum:]]'

  # Regexp de nettoyage d'expace
  echo ' 123 ' | grep -E -o '[^[:space:]]+'}}}

  # Matching a MAC address
  echo '' | egrep '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'}}}

How to track debian testing with fallback on unstable::

  itchy:~# cat /etc/apt/sources.list
  deb http://ftp.fr.debian.org/debian testing main non-free contrib
  deb http://ftp.fr.debian.org/debian unstable main non-free contrib
  deb http://security.debian.org/ etch/updates main
  
  itchy:~# cat /etc/apt/apt.conf
  APT::Default-Release "testing";

Another way to do it ::

  itchy:~# cat /etc/apt/preferences
  Package: *
  Pin: release a=testing
  Pin-Priority: 900
  
  Package: *
  Pin: release a=unstable
  Pin-Priority: 80
  
  Package: *
  Pin: release o=Debian
  Pin-Priority: -10
  

Getting started with postgres on Debian ::

  jd@lisa ~ sudo aptitude install postgresql-doc-8.1 postgresql-8.1
  jd@lisa ~ su
  Password:
  root@lisa:/home/jd# su postgres
  postgres@lisa:/home/jd$ createuser jd
  Le nouvel rôle est-t'il un superutilisateur ? (y/n) n
  Le nouvel rôle doit-il être autorisé à créer des bases de données ? (y/n) n
  Le nouvel rôle doit-il être autorisé à créer de nouveaux rôles ? (y/n) n
  CREATE ROLE
  postgres@lisa:/home/jd$ createdb jd
  CREATE DATABASE
  postgres@lisa:/home/jd$ exit
  root@lisa:/home/jd# exit
  jd@lisa ~ psql
  jd=> create temporary table toto (id int)'
  CREATE TABLE
  jd=> insert into fichier_loue values ('jd', 'misc', 1);
  INSERT 0 1
  

Gestion des servies sous debian ::

  update-rc.d -n -f lighttpd remove
  update-rc.d -f lighttpd remove
  update-rc.d  lighttpd install defaults
  

Quiet login ::

  touch ~/.hushlogin}}}


Binary/IP address string conversion ::

  binary2ip () { 
    for i in 0 8 16; do 
      echo -n  `bc <<< "ibase=2;${1:$i:8}"`. ;done
    echo  .`bc <<< "ibase=2;${1:24:8}"`
  }
  
  binary2ip 11111111111111110000000000000000
  255.255.0.0

  
  ip2binary () { 
  echo $1  
   | tr '.' ' ' 
   | xargs printf "obase=2;%d;%d;%d;%d\n" 
   | bc 
   | xargs printf "%8d" 
   | tr ' ' '0'
  echo
  }

  ip2binary 192.168.0.1
  11000000101010000000000000000001
  

Synchronize two directories ::

  rsync -az -e ssh --delete /var/www/moin/data/ bart:/var/wiki/data


A good Emacs font :: 
  
  (set-default-font "-*-terminal-medium-*-*-*-14-*-*-*-*-*-*-*")


Additional software on a new install::

  aptitude install apg less netcat nmap rsync tcpdump mc tshark \
     smartmontools hdparm screen emacs22
  
  sudo aptitude install ssh apache moinmoin zope postgresql-8.1 \
     xen-linux-system-2.6.17-2-xen-686 zope3{,-doc} debootstrap
  
  sudo aptitude install wireshark gtk-sharp2 libavahi-cil mono-gmcs 
  wget -c http://dev.mmgsecurity.com/downloads/lat/1.2/lat_1.2.0.1-1_i386.deb
  dpkg -i lat_1.2.0.1-1_i386.deb
  

Good .inputrc configuration ::

  set completion-ignore-case on
  set match-hidden-files off
  
  "\C-xi": "\C-a\C-k ifconfig | grep 'inet ' \C-j"
  "\C-xr": "\C-a\C-k grep   /etc/hosts \e13\C-b"
  "\C-xf": "for i in  ; do     ; done\e17\C-b "
  
  # if $psql
  # "\C-xu":"update \"\" set \"\" ;\e10\C-b"
  # "\C-x*":"select * from \"\" \e2\C-b"
  # "\C-x=":" where \"\" = \e4\C-b"
  # endif
  


Use Synergy to share the same keyboard and mouse between your boxes ::

  $ sudo aptitude install synergy
  
  $ cat .synergy.conf
  section: screens
          windows:
          debian:
  end
  
  section: links
  	windows:
  		right   =       debian
  	lisa:
  		left    =       windows
  end
  
  $ egrep 'debian|windows' /etc/hosts
  127.0.0.1    localhost debian
  10.0.0.1     windows
  
  $ synergys
  
  # On your windows box, install synergy, and launch it as a client to the
  # linux box (increase verbosity on the client and server box to debug)

filtre de trace rséeau::

  filtre_capture ()
  {
    smu01="192.168.8.251"
    smu02="192.168.8.252"
    smugw="192.168.8.254"
    
    OF=`echo $1 | sed s/^/clean-/`
    
    tethereal -R "(tcp or udp) \
                  and not (icmp or nfs or ssh) \
          	  and not (ip.addr==$smu01 or ip.addr==$smu02 or ip.addr==$smugw)" 
	      -r $1 -w $OF
  }


if [ "$TERM" != "dumb" ]; then
    export LS_COLORS='no=00:fi=00:di=01;34:ln=01;32:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:ex=01;30:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.gz=01;31:*.bz2=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.ogg=01;35:*.mp3=01;35:*.wav=01;35:';
    alias ls='ls --color=auto --format=vertical'
    #alias vdir='ls --color=auto --format=long'
fi

