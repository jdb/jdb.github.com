
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





The client can send a request get a reply
-----------------------------------------

This is one of the most basic implementation of a Twisted client:

- the client *high level* API is based on the *command* method which
  formats the network request and returns a Deferred, to which the
  user can attach the code processing the result,

- *lineReceived* is an internal command called by Twisted, when a a
  reply from the server is available. The reply gets passed to the
  callback set by the user,

.. literalinclude:: prototype/client_notif_1.py

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


If you want to use this code as an example, make sure to check the
:doc:`robustified version <prototype/client_notif_7>`.

For more details on *defer.inlineCallback* and the peculiar use of
*yield*, see :doc:`../../concurrent/smartpython`. In brief, the
association of the two makes it possible to turn a function returning
a deferred which fires a result into a more conventional function
which (*seemingly*) returns a result.


Notification mode and reception of two notifications
----------------------------------------------------

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

.. literalinclude:: prototype/client_notif_2.py
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

the client loops and ends the notification mode to get the available new item
-----------------------------------------------------------------------------

A client watching for notification is expected to loop to act on the
notifications. Also, whenever an interesting notification arrives, it
is the signal that new data is available. The API is not modified,
only the code executing when the connection is established is extended.

.. literalinclude:: prototype/client_notif_3.py
   :lines: 37-50


The user code is contain in one function
----------------------------------------

This iteration does not add new functionalities to the code, it
refactors the code to cleanly separate a general API from a specific
client script. There is no more need to derive a class and override a
specific method to process a notification. It is only a matter of
using the API in one function. 

.. literalinclude:: prototype/client_notif_4.py
   :lines: 38-55


Higher level API
----------------

A *receive* method is introduced in the *Client* protocol Class which
allows the user of the API not to know a specificity of the protocol
which is to switch modes between receiving the notifications and
fetching the newly available items.

Here is a higher level *receive* method which encapsulate the
notification mode:

.. literalinclude:: prototype/client_notif_5.py
   :lines: 36-52

For a user which only wants to receive the random number as fast as
possible, the code is much more straightforward:


.. literalinclude:: prototype/client_notif_5.py
   :lines: 56-63

Defeating the autologout server timer
-------------------------------------

.. todo:: 

   The IDLE rfc states that the client must quit and re-enter the
   notif mode every 29 minutes. The Python code stub is to be written
   to support this, and the article might receive one or two explanation.

.. literalinclude:: prototype/client_notif_6.py

Robust
------

.. todo::

   Mostly review and complete with new corner cases. Automating these
   tests with trial would surely help.

.. literalinclude:: prototype/client_notif_7.py

- what if a command is sent during in notification mode?

- *The server sends stuff in the socket before client has emitted a
  requests?*

  The behavior is defined in the first lines of the client protocol::

    class Client(basic.LineReceiver):
        
        d = None
    
        def lineReceived(self, data):
            self.d.callback(data)
            
        def command(self, cmd):
            self.sendLine(cmd)
            self.d = defer.Deferred()
            return self.d
    
  If data is received before a command has been emitted, the
  lineReceived will call the callback method on whatever is stored in
  the *d* attribute.

  When the client starts, the attribute *d* meant to receive the
  deferred triggered for the request replies is set to None. It is the
  job of the *command* method to instantiate and store a Deferred in
  this attribute because we only expect data after a command has been
  emitted. So in our case, the callback method is called on *None*
  which leads to a ``exceptions.AttributeError: 'NoneType' object has no
  attribute 'callback'``::

    def lineReceived(self, data):
        assert self.d is not None, ("Unexpected data from the server, "
                                    "no command emitted and not in "
                                    "notification mode")
        self.d.callback(data)

  Since receiving data while not in notification mode or waiting for a
  command is not allowed in our custom protocol, we can rightfully can
  raise an exception in this case and crash the program. This is a
  failfast strategy that will quickly spot bad behaving servers. But
  some might also say is unnecessarily too strict. Why not just ignore
  the unexpected data? ::

    def lineReceived(self, data):
        if self.d is None:
	    return 
        self.d.callback(data)

- *The server having emitted a command receives two answers*? 

  It could be because the server is crazy, or because a buggy network
  and network stack have duplicated the packets. *lineReceived* will
  call the callback method on the deferred a second time. It is the
  same situation as with this example

  >>> from twisted.internet import defer
  >>> d = defer.Deferred().addCallback(lambda x:42)
  >>> d.callback(None)
  >>> d.callback(None)
  Traceback (most recent call last): ...
  twisted.internet.defer.AlreadyCalledError

  A deferred is consumed when it is called, it can't be called
  twice. We must again make sure that the already used deferred is
  suppressed::

    def lineReceived(self, data):
        if self.d is None:
	    return 
        self.d.callback(data)
	self.d = None

  As *None* overwrite the used deferred, there is no way the deferred
  will be called again... Or is it really so? It is completely
  possible that the callback actually call lineReceived. At this
  point, the instruction ``self.d = None`` has not yet been executed:
  bing, subtle bug: an ``AlreadyCalledException`` is raised
  again. *self.d* must be overwritten *before* the callback is fired,
  and to be able to access the deferred to actually call the callback,
  the deferred can be stored in a temporary variable::

    def lineReceived(self, data):
        if self.d is None:
	    return 
	d, self.d = self.d, None
        d.callback(data)

- *What if the client sends multiple messages in a burst without
  waiting for the response to the first request to be back first?*

  ???

  it is easy to crash the client with an assert on the deferred
  attribute::

    def command(self, cmd):
        assert self.d is None
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d

  Maybe standard similar protocol, explicitly forbids this, and
  expects commands to be spooled, the next command being written only
  when the first reply is back.

  Another solution is to enumerate the requests and expect the request
  number in the replies. In the latter case, the Twisted client could
  maintain a dictionary of deferreds as a member of the protocol
  instead of a keeping track of a single deferred. The key would be
  the request number (the request id).

- *What if the server sends a notification at the exact same time
  that the client sends a request?*


.. 1. going into notification mode and exiting notification mode would be
.. adapted as a context manager: but the __enter__ and __exit__ will
.. return a deferred, the body of the with will be run as soon as the
.. enter() returns while we want the body to run as soon as the
.. deferred is fired... 

.. 2. What about deferred that can be recalled?


- What if the server sends a notification right before receiving a
  request from the client: won't the client be mislead and parse the
  notification for the reply?  

  In our context, this would be ``_stop_notify_`` being sent when a
  notification is on already on the wire. There are at least two
  solutions: 

  - The data received by the client must contain enough information to
    distinguish a reply from a notification, regardless of the state
    of the protocol. In our case, the notification data is prefixed by
    ``notif:``.  Conversely replies should never use this prefix. The
    client protocol instance features member attributes: the reply
    deferred and the notification deferred. ``lineReceived`` fires the
    correct callback by observing the data (checking foe the
    notification prefix)

- What if requests are sent in batch, instead of waiting for the first
  reply to the first command request before sending the second
  request? 

  In our case, the notif(), stopNotif() commands can be sent in a
  quick sequence when two notifications are quickly created. Looking
  at the code, it is clear that a new deferred will be created and
  will suppress the previous one before it is fired. When to replies
  come back, the first reply might be passed to the wrong callback,
  and it is certain that the second exeuction of the same callback
  will result in an AlreadyCalled exception.

  The solution is for the protocol to be extended sot that replies can
  include an unique id of the request, to be able to send requests in
  batch. The protocol instance would not keep one deferred got.

  A lighter solution is, instead of suppressing the existing deferred
  with a new one, chaining them: the requests will be queued.


- What is the server receives a request to send notifications, then do
  not reply as soon as possible, then replies a notif, and only then,
  sends the reply to the request?*


# is it possible in Twisted Python, to do a generator of network
# requests: with yield it seems a bit compromise since the value will
# not be available as argument of the function

# I wish I could write: 
# pattern, getter = conn.items["random"]
# for notif in conn.notifs(pattern):
#     with conn.pause_notifs():
#         print (yield getter())

Integration with the nice deskptop notification system
------------------------------------------------------

.. todo::

   The ``python-notify`` and ``libnotify-bin`` package offer the API
   to the Ubuntu notification system. The code is to be written and
   the paragraph in the article to be written.


1+1 == 2
