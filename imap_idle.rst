

Extending Twisted Mail with the IMAP *Push*
===========================================

Twisted supports the IMAP protocol used by millions accross the world
to remotely access their mailboxes. There is one extension of the IMAP
protocol though, which is not handled by the Twisted client library
and which is supported by popular mail server such as Dovecot or
Gmail: it is the IMAP IDLE command. An IMAP client sends this command
to the servers when it wants to be notified of the reception of new
mails. This is the *push mail* fonctionality which allows for faster
reception of emails on the client and also better ressource usage by
avoiding the frequent and needless polling of the mailbox for new
messages.

This serie of articles illustrates the steps of the developments and
integration of this extension into the Twisted Project. First, a
prototype of the notification mechanism between a Twisted client and
server is set up. The mechanism is similar to the real IMAP
notification mechanism and makes it easy to present the Twisted
abstractions and concepts involved without the IMAP protocol cruft.

An introduction of IMAP in five points follows with a presentation of
the current support by Twisted. At this point, it is possible to point
out exactly which and how Twisted's imap4 classes and methods needs to
be extended to support the IDLE command.

Then, the module is tested for its correct interoperability with a
local installation of Dovecot/Postfix on one hand, and on the other
hand with the Gmail servers, over SSL.

The next step is to connect with the Twisted community and get
familiar with the project methods, so that the patch gets merged
upstream. 

Finally, a simple plugin using the new command and solving a real
world problem is packaged and published, it shows a simple example of
how to use of the IMAP API from the user point of view.

.. toctree::
   :maxdepth: 1
   
   imap_idle/prototype
   imap_idle/twisted_imap
   imap_idle/interop
   imap_idle/twisted_methods
   imap_idle/notification_plugin

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
   
