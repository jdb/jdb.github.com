
.. _robust:

Robust
------

At this poiny, the client crashes on many cases: 

#. when lines are sent by a crazy server before the client has sent
   anything,

#. when a crazy server replies twice to a client request command,

#. when a crazy client sends multiple messages in a burst without
   waiting for the response to the first request to be returned first?

#. when the server sends a notification at the exact same time that
   the client sends a request to stop the notification?

Cases 1., 2., 3. are different from case 4. The latter. will happen
one day even with perfectly correct clients and servers, it is a clear
buggy corner case. For the former, clients should not crash when facing am
uncompliant server: peers must not only be correct but also need to be
robust.  In our prototype, when a line is received, the *callback()*
method of the *self.d* member attribute is executed: both self.d and
its *callback()* method must exits. Even more, as a deferred raises an
*AlreadyCalledException* when called a second time: it must be
suppressed whenever triggered. Here is a corrected version of
*lineReceived()*:

.. literalinclude::
   :lines: 7-13

To make sure the client waits for the completion of a command before
emitting a subsequent command, the *command()* can be enhanced with
the following (extreme) measure: the client stops with an exception is
a command is called when a response is expected. Another solution could be
to spool the requests in a queue but if there is a risk that the user
of the API will fill the queue or use too much memory on the client.

.. literalinclude::
   :lines: 15-19

.. Problem of the day: make a generator of network requests/replies, I
.. wish I could write: ::

     for notif in conn.notifs('random'):
         with conn.pause_notifs():
             print (yield random())
     maybe possible with corotwine

.. with defer.inlineCallbacks and yield, it seems impossible, the
.. coroutines seems more adapted since they hide asynchronous calls
.. behing a blocking interface.




