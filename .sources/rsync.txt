
rsync
=====

Incremental backup
------------------

::

   #!/bin/sh
   #backup.sh
   
   # `rsync src/ dst/` snchronize src and dst so that only the difference 
   # between the dirs will be *transferred* between source and destination
   
   # `rsync -a src/ dst/`  -a stand for "archive" and implies "the whole 
   # directory recursively" plus "keep the date and permissions"
   
   # `--link-dest=most-recent` is the magic option that allows only the 
   # differences between dest and the most recent backup to occupy space 
   # on disk (ie incremental backup)
   
   
   if [ -f /etc/backuprc   ]; then source /etc/backuprc  ; fi
   if [ -f $HOME/.backuprc ]; then source $HOME/.backuprc; fi
   
   precious=${1:-${precious_directory:-precious_directory}}
     backup=${2:-${backup_directory:-backup_directory}}
   
   ( echo $precious | grep -q '^/\|:' ) || precious=`pwd`/$precious
   ( echo $backup   | grep -q '^/\|:' ) ||   backup=`pwd`/$backup
   
   prefix=${3:-manual}
   ( echo $3 | grep  -q -o '[^[:alnum:]]' ) \
       && (echo "Prefix is not alnum. Exiting"; exit 1 )
   
   name=$prefix-`date +%F-%H-%M-%S`
   max=$((${max:-5}+1))  # max backup kept
   
   echo $backup | grep -q ':'
   
   if [ $?  -eq 0 ]; then
         host=`echo $backup | cut -d ':' -f 1`
       backup=`echo $backup | cut -d ':' -f 2`
   
       cmd="ls -d $backup/$prefix-* 2>/dev/null "
       recent=`echo $cmd | ssh $host 2>/dev/null  | head -n 1`
   
       ssh $host "cp -al $recent $backup/$name
       
       rsync -e ssh -a --delete $precious/ $host:$backup/$name/  \
   	|| ( echo -e "rsync error. Exiting.";  exit 1 )
   
       echo "new backup \"$backup/$name\" was created on $host."
   
       cmd="ls -rd $backup/$prefix-* 2>/dev/null"
       oldest=` echo $cmd | ssh $host 2>/dev/null | sed  -n "$max,\\$p" `
       if [ ! -z "$oldest" ] ; then 
   	echo $oldest | ssh $host "xargs  rm -r"
   	for i in $oldest; do  
   	    echo "old backup \"$i\" was deleted on $host."; done; fi
   
   else 
   
       cd $backup
       recent=`ls -d $prefix-* 2>/dev/null | head -n 1`
       
       rsync -e ssh -a --delete --link-dest=$recent $precious/ $name/ \
   	|| ( echo -e "rsync error. Exiting.";  exit 1 )
       echo "new backup \"`pwd`/$name\" was created."
       
       oldest=`ls -rd $prefix-* | sed  -n "$max,\\$p" `
       if [ ! -z "$oldest" ] ; then 
   	for i in $oldest; do  
   	    rm -r $i ; 
   	    echo "old backup \"`pwd`/$i\" was deleted."; done; fi
   fi


Notes
-----

 * prerequisite: rsync + ssh, installed both locally and remotely

 * make sure the filesystem is inactive when taking the backup or
   rollbacking (switch off apache or backup a lvm snapshot)

 * rollback::

     rsync -a --delete $recent/ /my-precious-directory/

 * cron: put the backup script in /usr/local/bin/backup.sh and in
   /etc/cron.daily place this executable script:: 

     #!/bin/sh
     /usr/local/bin/backup.sh /home/jd/toto /home/jd/tata daily



Most recent backup
------------------

To minize the data kept on disk, we reuse the most recent backup, to
keep only the differences between the current data and the most recent
backup. To determine the most recent backup, it is possible to:

* use the modification time of the backup folder (fragile, just don't
  "touch" the oldest backup!)

* use the name of the backup and it contains the date (we use this
  solution)

Tests
-----

 * bogus options: none,  non alnum characters for the prefix ::

     backup.sh 
     backup.sh azert 
     backup.sh a b 2,2
     backup.sh a apu:b 
  
 * remote, distant ??

 * No recent, rsync does the right thing. Non existing directory:
   rsync stops, we care for the return code.

Bugs
----

 * Incremental disk write does not work remotely ie when the value of
   the option --link-dest includes a host ::

     rsync precious/ apu:/var/backups/  
     rsync --link-dest=/var/backups/recent precious/ /var/backups/new-backup
     rsync --link-dest=apu:/var/backups/recent precious/ apu:/var/backups/new-backup

 * now I prefer names like {{{backup-1}}} to {{{backup-`date +%F`}}}

Integration of virtual machines
-------------------------------

On apu, if you keep the vm name and the logical volume the same, then
you can get the list of lv to backup by looking for the vm config
files in /etc/xen (grepping some vm config file pattern). Then,
iterating on this list :

 * mount a snapshot of the lv in /mnt/snap

 * make a backup from /mnt/snap to /var/backup/$i

 * umount snapshot

The script can be launched daily, weekly and monthly by putting it
into /usr/local and putting a link to it in cron.*. Also, I want to be
able launch it by hand on a specific vm just by specifying the vm and
it would happily backup the vm to manual/ ::

   #!/bin/bash
   max=10
   
   if [ -z "$PS1" ];
   then  # non interactif
   
       # prefix should be either daily, weekly,.. since launch from cron.{daily,weekly,...}
       prefix=$(basename `pwd`  | cut -f 2 -d '.')  
       vmlist=`ls /etc/xen | xargs grep -H vif  | cut -f 1 -d ':'`  # get the list of vm form /etc/xen/*
   
   else  # mode interactif
   
       if [ ! -f /etc/xen/$1 ] ; then
           echo $i is not a xen domU; 
           exit 1 ; done
   
       if [ $? -ne `lvs | awk '{print $1}' | grep -q $1` ]; then
           echo $i logical volume; 
           exit 1 ; done
   
       if [ ! -d /var/backup/$i ] ; then
           mkdir -p -d /var/backup/$i; done
   
       prefix=manual
       vmlist=
   fi
   
   clean-up () { 
       umount /mnt/snap && lvremove sys/snap
       exit 1
   } 
   
   trap clean-up SIGINT SIGTERM
   
   for i in $vmlist; do 
       lvcreate -s -n snap -L 200m  sys/$i
       mount /dev/sys/snap /mnt/snap
   
       (   cd $backup/$i
           recent=`ls manual-* | head -n 1`
   
           rsync -a --delete --link-dest=$recent /mnt/snap/ $prefix-`date +%F`
   
           # delete the oldest backup if there are at least 10 backups 
           oldest=`ls  $prefix-* | sed  -n "$max,\$p" | tail -n 1`
           if [ -d "$oldest" ] ; then rm -r $oldest ; fi
       )
   
       umount /mnt/snap && lvremove sys/snap
   
   done

