
A notification server in Twisted
================================

Let's create a simple client and a simple server able to receive
notification. It will be super simple client supporting s custom dumb
protocol no HTTP nor IMAP. The goal is just to play with a *server to
client notification mechanism* with Twisted: 

#. the traditional situation for a client and server application is for
   the server to initiate requests and the server to generate
   responses,

#. notifications actually *inverts* the role of client and server as
   the serveur initiates notification that the client wait for and
   acknowledges.

The overview shows how to express notifications in Twisted. The
protocol section presents the four commands of the protocol. The next
sections shows how the prototype evolves to satisfy the need.

Overview
--------

In Twisted, to exchange requests and replies with a server:. 

#. a client emits a request,

#. it writes the command string in the transport socket, 

#. and takes care to stores the code processing the reply where the
   *lineReceived* will be able to find it when the reply comes back,

#. when the replies comes back, the reactor pass it on to the
   *lineReceived* which usually calls the callback chosen by the
   developer with the data as argument.

The callback is stored in a deferred as an member attribute of the
protocol instance. The deferred is re-instantiated whenever sending a
new request into the transport. The member attribute is empty between
request/replies exchanges and reset to fire from a request and until
the replies arrives from the server.

To expect notifications:

#. the client requests to go into notification mode, sets the callback

#. the server replies, the callback is fired and here is the
   difference with the traditional client/server exchange: 

#. **the callback processing the reply from the server re-instantiates
   a deferred** holding the callback processing the notification.

#. at some point, the server sends a notification. The client receives
   the notification and might decide to expect other notification, or
   turn to "normal" mode to actively request the server.

   Back to normal mode, when the notification has been actively
   processed, it is up to the client to reinitiate the notification
   mode.

Our prototype is built in several steps being a bit more useful and a
bit more complex at each iteration:

#. the client can send a request get a reply, 

#. the client can ask notification from the server, receives and process a
   notification, exit the notification mode and quit,

#. the client can loop on the notifications until killed with a control-C,

#. the client will exit the notification mode to get more information
   from server

#. there is no more need to derive a class and override a specific
   method to process a notification. It is only a matter 

#. as the server automatically timeout in notification mode, the
   client exits the notification mode and re-enters it automatically a
   few seconds before the timeout

#. The server gets robust and behaves in case of problems


Basic request and reply
-----------------------




Robustness and error handling
-----------------------------

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
  some might also say is unecessarily too strict. Why not just ignore
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
  bing, subtle bug an ``AlreadyCalledException`` is raised
  again. self.d must be overwritten *before* the callback is fired,
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

The client protocol
-------------------

The client Protocol has commands for requesting:

- random numbers, 

- renting offers details,

- changing state to listening for notification. 

Let's design our mini protocol to be line oriented:
  we will be able to

the client Factory is not really useful in our example: the reactor
requires the factory to be able to offer a protocol instance 

Deferred



