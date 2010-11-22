
A notification client in Twisted
================================

.. todo::

   Review and complete. Each iteration is contained in a single file
   and ends up as a single html page with the complete listing. It
   would help readability if the prototype.html article would be a
   single page, and only the code diffs were show. The Sphinx
   ``literalinclude`` command is super handy for that, especially
   with its *start-from*, *stop-at*, *lines* and *pyobject* argument 
   


Let's create a simple client and a simple server able to receive
notification. It will be super simple client supporting a custom line
based protocol, just to play with a *server to client notification
mechanism* in Twisted. While the traditional situation is for a client
to initiate requests to the server which generates responses,
notifications actually *invert* the role of client and server as the
serveur initiates notification that the client wait for and
acknowledges. With Twisted's abstractions, here is how to implement
exchanges between a client and a server:

#. The client protocol instance format the correct request string in
   the *transport* attribute of the protocol's factory.
   
   At the same time, it takes care to store the code processing the
   reply where the *lineReceived* method will be able to find
   it. *lineReceived* is called automatically by Twisted when the
   reply comes back in the *transport*.

   The callback is stored in a deferred, which is usually a member
   attribute of the protocol instance. The deferred is re-instantiated
   whenever sending a new request into the transport.

#. when the replies comes back, the reactor pass it on to the
   *lineReceived* which usually calls the callback chosen by the
   developer with the received data as argument.

   The deferred is suppressed when the reply gets available. The
   member attribute is empty between request/replies exchanges.

Now, to expect notifications:

#. the client sends a request to go into notification mode, and sets
   a callback in a deferred as usual,

#. the server replies and accepts, the callback is fired and here is
   the difference with the traditional client/server exchange: **the
   callback processing the reply re-instantiates a deferred** holding
   a callback meant to process the notification

#. at some point, the server sends a notification. The client receives
   the notification and might decide to expect other notifications, or
   turn to "normal" mode to actively request the server.

   Back to normal mode, when the notification has been actively
   processed, it is up to the client to reinitiate the notification
   mode.

The overview shows how to express notifications in Twisted with a
Protocol class and deferreds. The protocol section briefly presents
the four commands of the protocol. Later sections shows how the
prototype evolves toward a complete program.


A simple line oriented protocol
-------------------------------

The protocol includes three commands:

- ``random?``: the server should reply a random number,

- ``classified?``: the server should reply the recent unread
  classified ads,

- ``notif``: the server gets ready to send notifications about new
  items being available (see below). This command is not completed
  until the client sends ``stop_notif``.

A notification can either be : ``notif: random``, ``notif:
classified`` or ``notif: OK`` (the latter to acknowledge the
notification mod). The server notifies the client of the availability
of random numbers and classified ads. Then, it is up to the client to
exit the notification mode by sending the data ``stop_notif`` to
complete the ``notif`` command and then effectively download the
random number or the classified ad, whatever the client is interested
in. The successful completion of a command is indicated by sending the
``OK`` status response.

How will the protocol be typically used?

The client connects, retrieves the most recent items it is interested
in and request the server to send notifications about newly available
items. For each notification sent by the server, the client will exit
the notification mode to explicitly downloads the items. Here is an
example session, recorded on the server (the line begins with ``S:``
if sent by the server, ``C:`` if sent by the client)::

  C:  random?
  S:  456902234
  C:  classified?
  S:  Nice appart in the 11e.
  C:  _notif_
  S:  will send notifs
  S:  notif: classified
  C:  OK
  S:  notif: random
  C:  stop_notif
  S:  OK
  C:  random?
  S:  89765234756  
  C:  _notif_
  S:  will send notifs
  S:  notif: classified
  C:  OK
  

Prototype iterations
--------------------

Our prototype is built in several steps being a bit more useful and a
bit more complex at each iteration:

.. toctree::

   prototype/client_notif_1
   prototype/client_notif_2
   prototype/client_notif_3
   prototype/client_notif_4
   prototype/client_notif_5
   prototype/client_notif_6
   prototype/client_notif_7
   prototype/client_notif_8




