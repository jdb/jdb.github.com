
Robust
------

.. todo::

   Mostly review and complete with new corner cases. Automating these
   tests with trial would surely help.

.. literalinclude:: client_notif_7.py

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
