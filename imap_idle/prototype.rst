
A notification client in Twisted
================================

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

.. _protocol:

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

Since the ``notif`` command lasts until the client sends
``stop_notif``, the server can't acknowledge the switch to
notification mode with the ``OK`` response which is used to terminate
a command. Instead, the server replies ``will send notif``

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
  C:  notif
  S:  will send notifs
  S:  notif: classified
  C:  OK
  S:  notif: random
  C:  stop_notif
  S:  OK
  C:  random?
  S:  89765234756  
  C:  notif
  S:  will send notifs
  S:  notif: classified
  C:  OK
  

Iterations
----------

Our prototype is built in several steps being a bit more useful and a
bit more complex at each iteration:

#. :ref:`request_reply` 
#. :ref:`notifs`
#. :ref:`loop`
#. :ref:`clientcreator`
#. :ref:`higher`
#. :ref:`timer`
#. :ref:`desktop`

.. _request_reply:

The client can send a request get a reply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is one of the most basic implementation of a Twisted client:

- the client *high level* API is based on the *command* method which
  formats the network request and returns a Deferred, to which the
  user can attach the code processing the result,

- *lineReceived* is an internal command called by Twisted, when a a
  reply from the server is available. The reply gets passed to the
  callback set by the user,

.. literalinclude:: prototype/client_notif_1_request_reply.py

To use this client: in a first console, launch the server which can
simply be: ``nc -C -l 6789`` (the port is hardcoded in the
client). Then launch the client in another console. You can then
reply, by hand to the client requests on the server console. Here is
an example session from he server::

   ~$ nc -C -l 6789
   random?
   5739578
   classified?
   A cool duplex in the 11e

From the client::

   $ python client_notif_1.py 
   5739578
   A cool duplex in the 11e


If you want to use this code as an example, be aware that it features
many bugs, be sure to check the :doc:`robustified version
<robust>`. Also, for more details on *defer.inlineCallback* and the peculiar
use of *yield*, see :doc:`../../concurrent/smartpython`. In brief, the
association of the two makes it possible to turn a function returning
a deferred which fires a result into a more conventional function
which (*seemingly*) returns a result.


.. toctree::
   :hidden:

   robust
   

.. _notifs:

Notification mode and reception of two notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This iteration introduces three methods in our *Client* class
protocol, only for supporting the events related to the ``notif``
protocol command:

- *notify*: requests the server to switch to notification
  mode. Returns a callback which won't fire 'OK' but will fire 'will
  send notif' according to the :ref:`protocol definition  <protocol>`

- *waitNotif*: re-installs a deferred, and returns a deferred used to
  attach a callback processing the notification 

- *stopNotify*: ends the notification mode, and switches the server
  back into the traditional client/server mode. stopNotifiy does not
  sends a protocol command.


The changes made to connectionMade illustrates how to use the API

.. literalinclude:: prototype/client_notif_2_notifs.py
   :lines: 25-46

An example session on the server::

   ~$ nc -C -l 6789
   random?
   23
   classified?
   32
   notif
   will send notification
   notif: random
   notif: random
   stop_notif
   OK

From the client this looks like::

  ~$ python prototype/client_notif_2.py 
  34
  43
  will send notif
  a notif: 'notif: random'
  a second notif: 'notif: random'
  OK

.. there is a bug is notify are called without waitNotif: alreadycalledcallback

.. _loop:

The client loops and ends the notification mode to get the available new item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A client watching for notification is expected to loop to act on the
notifications. Also, whenever an interesting notification arrives, it
is the signal that new data is available. The API is not modified,
only the code executing when the connection is established is extended.

.. literalinclude:: prototype/client_notif_3_loop.py
   :lines: 37-50

.. _clientcreator:

The user code is contain in one function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This iteration does not add new functionalities to the code, it
refactors the code to cleanly separate a general API from a specific
client script. There is no more need to derive a class and override a
specific method to process a notification. It is only a matter of
using the API in one function. 

.. literalinclude:: prototype/client_notif_4_clientcreator.py
   :lines: 38-55

.. _higher:

Higher level API
~~~~~~~~~~~~~~~~

For a user which only wants to receive the random number as fast as
possible, the API can be much more straightforward:

.. literalinclude:: prototype/client_notif_5_higher.py
   :lines: 56-63

A *receive* method is introduced in the *Client* protocol Class which
hides the need which is specific to this protocol to switch modes
between receiving the notifications and fetching the newly available
items. *receive* method wraps the notification mode switch:

.. literalinclude:: prototype/client_notif_5_higher.py
   :lines: 36-52

.. _timer:

Defeating the *auto stop-notify* server timer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: 

   The IDLE rfc states that the client must quit and re-enter the
   notif mode every 29 minutes. The Python code stub is to be written
   to support this, and the article might receive one or two explanation.

.. literalinclude:: prototype/client_notif_6_timer.py
   :lines: 3-5

.. _desktop:

Integration with the nice deskptop notification system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo::

   The ``python-notify`` and ``libnotify-bin`` package offer the API
   to the Ubuntu notification system. The code is to be written and
   the paragraph in the article to be written.


1+1 == 2

.. literalinclude:: prototype/client_notif_7_desktop.py
   :lines: 3-5

In the end, the full source of the notiication client can be read
:doc:`here<prototype/full>`.

.. toctree::
   :hidden:

   prototype/full
