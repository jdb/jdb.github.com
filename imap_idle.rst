

Extending Twisted Mail with the IMAP *Push*
===========================================

Twisted supports the IMAP protocol used by millions accross the world
to remotely access their mailboxes. There is one extension of the IMAP
protocol which is not handled by the Twisted client library and which is
supported by the Dovecot, Gmail and many other mail servers: it is the
IMAP IDLE commands which the client sends to the servers when it wants
to be notified of the reception of new mails.

This is the *push mail* fonctionality which allows for faster
reception of emails on the client and also better ressource usage by
avoiding the frequent and needless polling of the mailbox for new
messages.

This series illustrates the steps of the developments and integration
of this extension into the Twisted Project. First, a prototype of the
notification mechanism between a Twisted client and server is set
up. Then, this mechanism is *ported* to IMAP, by extending the Twisted
IMAP module. Then, this module interoperability is tested with a local
installation of Dovecot/Postfix on one hand, and on the other hand
with the Gmail servers, over SSL. Finally, the steps with connecting
with the Twisted community and methods are presented, so that our code
get merged upstream.

.. toctree::
   :maxdepth: 1
   
   imap_idle/prototype
   imap_idle/twisted_imap
   imap_idle/interop
   imap_idle/twisted_methods

.. todolist::


.. toctree::
   :hidden: 
   
   imap_idle/pycon-presentation/proposal
   imap_idle/pycon-presentation/speaker_bio
   imap_idle/pycon-presentation/speech
   imap_idle/twisted_imap/imap4client
   imap_idle/twisted_imap/imap4client_robust
   imap_idle/twisted_imap/imap4client_yield
   imap_idle/twisted_imap/imap4client_notif
   
