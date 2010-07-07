

Extending Twisted Mail with the IMAP *Push*
===========================================

Twisted supports the IMAP protocol used by millions accross the world
to remotely access their mailboxes. There is one extension of the IMAP
which is not handled by the Twisted client library and which is
supported by the Dovecot, Gmail and many other mail servers: it is the
IMAP IDLE commands which the client sends to the servers when it wants
to be notified of the reception of new mails.

This is the *push mail* fonctionality which allows for faster
reception of emails on the client and also better ressource usage by
avoiding the frequent and needless polling of the mailbox for new
messages.

This series illustrates the steps of the developements and integration
of this extension into the Twisted Project.

.. toctree::
   :maxdepth: 1
   
   imap_idle/notif
   imap_idle/imap
   imap_idle/local
   imap_idle/gmail
   imap_idle/twisted_methods
