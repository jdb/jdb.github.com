
A notification client in Twisted
================================

Let's create a simple client and a simple server able to receive
notification. It will be super simple client supporting a custom line
based protocol, just to play with a *server to client notification
mechanism* in Twisted. While the traditional situation is for a client
to initiate requests to the server which generates responses,
notifications actually *inverts* the role of client and server as the
serveur initiates notification that the client wait for and
acknowledges. With Twisted's abstractions, here is how to implement
exchanges between a client and a server:

#. The client instance writes the command string in its factory.


of a class which derives from
   Protocol. The instance was created by a ClientFactory which is
   referenced from the client instance by the ``factory``
   attribute. 

   an instance of class deriving writes the command string
   in its the transport socket,

   - at the same time, it takes care to store the code processing the
     reply where the *lineReceived* method, called automatically by
     Twisted, will be able to find it when the reply comes back,

     The callback is stored in a deferred, usually as an member
     attribute of the protocol instance. The deferred is
     re-instantiated whenever sending a new request into the
     transport. The member attribute is empty between request/replies
     exchanges and reset to fire from a request and until the replies
     arrives from the server.

#. when the replies comes back, the reactor pass it on to the
   *lineReceived* which usually calls the callback chosen by the
   developer with the received data as argument.

Now, to expect notifications:

#. the client sends a request to go into notification mode, and sets
   a callback,

#. the server replies and accepts, the callback is fired and here is
   the difference with the traditional client/server exchange:

#. **the callback processing the reply from the server re-instantiates
   a deferred** holding a callback processing the notification

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

The protocol includes four commands:

- ``random?``: the server should reply a random number,

- ``classified?``: the server should reply the recent unread
  classified ads,

- ``_notif_``: the server gets ready to send notifications about new
  items being available (see below)

- ``_stop_notif_``: the server stops sending notifications and get
  back to replying to requests.

A notification can either be : ``notif: random`` or ``notif:
classified``. The server notifies the client of the availability of
random numbers and classified ads. Then, it is up to the client to
exit the notification mode to effectively download the random number
or the classified ad. 

How will the protocol be typically used?

Clients can be interested in random numbers or in classifieds ads. The
client connects, retrieves the most recent items it is interested in
and request the server to send notifications about newly available
items. For each notification sent by the server, the client will exit
the notification mode to explicitly downloads the items. Here is an
example session, recorded on the server (the line begins with ``S:`` if
sent by the server, ``C:`` if sent by the client)::

  C:  random?
  S:  456902234
  C:  classified?
  S:  Nice appart in the 11e.
  C:  _notif_
  S:  OK
  S:  notif: classified
  C:  OK
  S:  notif: random
  C:  OK
  C:  _stop_notif_
  S:  OK
  C:  random?
  S:  89765234756  
  C:  _notif_
  S:  OK
  S:  notif: classified
  C:  OK

Here is the data received by the client ::

  456902234
  Nice appart in the 11e.
  notif: classified
  notif: random
  89765234756
  notif: classified
  

Prototype tests
---------------

Our prototype is built in several steps being a bit more useful and a
bit more complex at each iteration:

#. the client can send a request get a reply, 

#. the client can loop on the notifications until killed with a
   control-C,

#. the client will exit the notification mode to get more information
   from server when new random numbers are available,

#. there is no more need to derive a class and override a specific
   method to process a notification. It is only a matter of using the
   high level API in one function separated from the protocol class.

#. as the server automatically timeout in notification mode, the
   client exits the notification mode and re-enters it automatically a
   few seconds before the timeout

#. The server gets robust and does the right thing in case of problems


Basic request and reply
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: notif_1.py

Receiving notification
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: notif_2.py

Entering and exiting the notification mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: notif_3.py

Working around the server timeouts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: notif_4.py

Robustness and error handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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

