Using a windows box along with a linux desktop
----------------------------------------------

Access Samba shares ===
 1. {{{
aptitude install smbfs}}}
 1. Test it with {{{
# smbclient -L sandra -U%
# smbclient -L sandra -U "COMVERSE\jbrowne"
Password: 
# mount -t smbfs -o username="COMVERSE\jbrowne" //sandra/users /tmp/sandra
Password: 
# ls /tmp/sandra
 [ ... lots of directories ]

# umount /tmp/sandra
# mount -t smbfs -o username="COMVERSE\jbrowne",password="mypassword" //sandra/users /tmp/sandra
# ls /tmp/sandra
 [ ... lots of directories ]

# umount /tmp/sandra
# cat > /etc/comverse.credentials && chmod og-rwx /etc/comverse.credentials
username = COMVERSE\jbrowne
password = mypassword
# mount -t smbfs -o credentials=/etc/comverse.credentials //sandra/users /mnt/sandra
# ls /tmp/sandra && umount /tmp/sandra
 [ ... lots of directories ]

}}} Please note 1. the mandatory "realm" for the username, 2. the tricky use of `"' in some case but not in every case.
 1. Mount it at boot time {{{
# echo '//sandra/users  /mnt/sandra     smbfs   credentials=/etc/comverse.credentials,gid=jbrowne,uid=jbrowne 0 0' \
     >> /etc/fstab
# mount -a
# ls /mnt/sandra
 [ ... lots of directories ]
}}} Note the use of 'gid' and 'uid' so that a non root user can access the share.
 1. Easy access to the shares :{{{
$ cd
$ mkdir  /mnt/sandra/jbrowne/backup && ln -s /mnt/sandra/jbrowne/backup 
$ mkdir  /mnt/sandra/jbrowne/mycc && ln -s /mnt/sandra/jbrowne/mycc}}}

=== Use Synergy to share the same keyboard and mouse between your boxes ===
 1. On your linux box : {{{$ aptitude install synergy

$ ls ~/.synergy.conf*
.synergy.conf  .synergy.conf.bart  .synergy.conf.FR-PAR-JDBROWN

$ cat .synergy.conf
section: screens
        FR-PAR-JDBrown:
        lisa:
end

section: links
FR-PAR-JDBrown:
        right   =       lisa
lisa:
        left    =       FR-PAR-JDBrown
end

$ egrep 'lisa|FR' /etc/hosts
127.0.0.1       localhost lisa
10.165.128.92   FR-PAR-JDBrown

$ synergys}}}

 1. On your windows box, install synergy, and launch it as a client to the linux box (increase verbosity on the cient and server box to debug)

=== Evolution ===
