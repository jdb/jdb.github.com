
Interoperability with Dovecot and Gmail
=======================================

.. todo::

   The imap4client_notif.py code is untested 

.. todo::

   The interop page is to be written, does not have to be long, jsut
   copy and paste the commands ot have dovecot/postfix running, and
   show an interaction of the client with a server and/or with netcat



::

  'nc -C' or 'delimiter = \n' in the LineReceiver instance

Postfix and Dovecot installed locally
-------------------------------------




The IMAP protocol at Gmail
--------------------------


.. todo::
   
   Bottom line: connect to gmail with a reactor.connectSSL instead of
   a connectTCP and use the login command instead of the authenticate
   command

   The original imapclient script would not connect, I think because
   gmail listens on a TLS socket from the start instead of beginning
   an open connection and then starting TLS as dovecot does

