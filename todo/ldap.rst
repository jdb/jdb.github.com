
Cheatsheet on LDAP
------------------

 * server ::

    aptitude install slapd ldap-utils
    sed -n 's/#\(rootdn.*\)/\1/p' /etc/ldap/slapd.conf
    ldapadd -x -W -c -D "cn=admin,dc=leela,dc=fr" -f backup_de_la_base.ldif}}}
    
 * create an OpenSSL certificate for the server::  

    openssl genrsa -out ldap.pem 2048 openssl req -new -x509 -key
    ldap.pem -out ldap-cert.pem -days 1095 

   * `OpenSSL keys`_
   * `OpenSSL keys`_

   .. _OpenSSL keys: http://www.openssl.org/docs/HOWTO/keys.txt
   .. _OpenSSL certificates: http://www.openssl.org/docs/HOWTO/certificates.txt


 * client ::

     cd && echo -n "BASE dc=leela,dc=fr\nHOST apu" >> .ldaprc
     echo 'alias ldapsearch="ldapsearch -x -LLL"' >> .bashrc
     echo '"\C-xa": "ldapsearch displayName= mobile homePhone\e17\C-b"' >> .inputrc

 * gq ::

     aptitude install gq

   Note that gq has two painful bugs: when you enter the description
   of a new server, then you need to validate and close the soft asap,
   or else the server's settings are forgotten ({{{watch cat
   ~/.gq}}}). Quite the same bug and workaround, when "remembering the
   password", when asked the password, type it and before doing
   anything else quit and relaunch gq or else the password don't get
   remembered.

 * SASL + thunderbird integration???

=== Howto ===
 * install to form scratch in Debian and add your first user?
 * How o define the root admin? 

