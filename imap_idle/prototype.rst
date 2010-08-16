
A notification client in Twisted
================================

Let's create a simple client and a simple server able to receive
notifications. It will be a simple client supporting a custom line
based protocol, just to play with a **server to client notification
mechanism** in Twisted. While the traditional situation is for a client
to initiate commands to the server which generates responses,
notifications actually *invert* the role of client and server as the
server initiates notification that the client wait for. With Twisted's
abstractions, here is how to implement command/responses between a
client and a server:

#. The client protocol instance format the correct command string and
   writes it in the *transport* attribute of the instance's factory.
   
   At the same time, it takes care to store the code processing the
   response where, later on, the *lineReceived* method will be able to
   find it. *lineReceived* is called automatically by Twisted when the
   response comes back in the *transport*.

   The callback is stored in a deferred, which is usually a member
   attribute of the protocol instance. The deferred is re-instantiated
   whenever sending a new command into the transport.

#. when the response comes back, the Twisted reactor pass it on to the
   *lineReceived* which usually calls the callback chosen by the
   developer with the received data as argument.

   The deferred is consumed when the response gets available. The member
   attribute containing the deferred is empty between command/response
   exchanges.

Now, let's try this first approach to process notifications:

#. the client sends a command for the server to go into notification
   mode, and sets a callback in a deferred as usual,

#. the server response and accepts, the callback is fired and here is
   the difference with the traditional client/server exchange

#. A method generating a deferred must be called to attach the
   callback of the next notification,

#. at some point, the server sends a notification. The client receives
   the notification and might decide to expect other notifications, or
   turn to "normal" mode to actively command the server.

   Back to normal mode, when the notification has been actively
   processed, it is up to the client to reinitiate the notification
   mode.

The next section presents an overview of a custom protocol example:
the four commands of the protocol are presented. Later sections shows
how the prototype evolves iteratively toward a more complete program.

.. _protocol:

A simple line oriented protocol
-------------------------------

The protocol includes four commands:

- ``random?``: the server should reply a random number,

- ``classified?``: the server should reply the recent unread
  classified ads,

- ``notif``: the server gets ready to send notifications about new
  items being available. 

- ``stop_notif``: the server stops sending notifications. For
  ``notif`` and ``stop_notif``, the server replies ``OK`` to accept
  the command.

A notification can either be : ``notif: random`` or ``notif:
classified`` and is used by the server to notify the client of the
availability of random numbers and classified ads. Then, it is up to
the client to exit the notification mode by sending the data
``stop_notif`` to complete the ``notif`` command and then effectively
download the random number or the classified ad, whatever the client
is interested in. 

The protocol will typically be used in the following manner? The
client connects, retrieves the most recent items it is interested in
and request the server to send notifications about newly available
items. For each notification sent by the server, the client will exit
the notification mode to explicitly downloads the items. Here is an
example session, recorded on the server (the line begins with ``S:``
if sent by the server, ``C:`` if sent by the client)::

  C:  random?
  S:  456902234
  C:  classified?
  S:  Nice appart in the 11e.
  C:  notif
  S:  OK
  S:  notif: classified
  S:  notif: random
  C:  stop_notif
  S:  OK
  C:  random?
  S:  89765234756  
  C:  notif
  S:  OK
  S:  notif: classified

Iterations
----------

Our prototype is built in several steps being a bit more useful and a
bit more complex at each iteration:

#. :ref:`command_response` 
#. :ref:`notifs`
#. :ref:`loop`
#. :ref:`robust`
#. :ref:`async`
#. :ref:`higher`
#. :ref:`timer`
#. :ref:`desktop`

.. _command_response:

The client can send a command and get a response
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is one of the most basic implementation of a Twisted client:

- the client API is based on the *command* internal method which
  formats the network command and returns a Deferred, to which the
  user can attach the code processing the result,

- *lineReceived* is a command called by Twisted when a a
  response from the server is available. The response gets passed to the
  callback set by the user,

.. literalinclude:: prototype/client_notif_1_command_response.py

To use this client: in a first console, launch the server which can
simply be: ``nc -C -l 6789`` (the port is hardcoded in the
client). Then launch the client in another console. You can then
reply, by hand to the client commands on the server console. Here is
an example session from the server::

   $ nc -C -l 6789
   random?
   5739578
   classified?
   A cool duplex in the 11e

For more details on *defer.inlineCallbacks* and the peculiar
use of *yield*, see :doc:`../../concurrent/smartpython`. In brief, the
association of the two makes it possible to turn a function returning
a deferred which fires a result into a more conventional function
which (*seemingly*) returns a result.


.. _notifs:

Notification mode and reception of two notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This iteration introduces three methods in our *Client* class
protocol, for supporting the events related to the ``notif``
and ``stop_notif`` protocol commands:

- *notify*: requests the server to switch to notification
  mode. Returns a callback which will fire 'OK' according to the
  :ref:`protocol definition <protocol>`

- *waitNotif*: installs and return a deferred, used to attach a
  callback processing the notification

- *stopNotify*: ends the notification mode, and switches the server
  back into the traditional client/server mode. 



.. literalinclude:: prototype/client_notif_2_notifs.py
   :lines: 25-46

The changes made to connectionMade illustrates how to use the API,
from the client this might looks like::

  $ python prototype/client_notif_2.py 
  34
  43
  OK
  a notif: 'notif: random'
  a second notif: 'notif: random'
  OK

.. _loop:

The client loops and ends the notification mode to get the available new item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is good to receive notifications about random numbers, it better to
get the random number.

.. literalinclude:: prototype/client_notif_3_loop.py
   :lines: 37-50

.. _robust:

Robustness
~~~~~~~~~~

At this point, the client crashes on many cases: 

#. when a crazy server sends unexpected data: either before the client
   has sent anything, or because the server responses arrives twice on
   the client,

#. when a crazy client sends multiple messages in a burst without
   waiting for the response to the first command to be returned first?

#. when the server sends a notification at the exact same time that
   the client sends a command to stop the notification?

Cases 1. and 2. are different from case 3. The latter will happen one
day even with perfectly correct clients and servers, it is a bug. For
the former, clients should not crash when facing am uncompliant
server: peers must not only be correct but also need to be robust.  

Duplicate and unexpected data should be ignored. In our prototype,
when a line is received, the *callback()* method of the *self.d*
member attribute is executed: both self.d and its *callback()* method
must exits. Even more, as a deferred raises an
*AlreadyCalledException* when called a second time, it must be 
suppressed whenever triggered. A line received should be ignored if
one of these condition is unmet. Here is a more robust version of
*lineReceived()*:

.. literalinclude:: prototype/client_notif_4_robust.py
   :lines: 5-13

To make sure the client waits for the completion of a command before
emitting a subsequent command, the *command()* can be enhanced with
the following (extreme) measure: the client stops with an exception is
a command is called when a response is being expected, the user of the
API is warned! Another solution could be to spool the commands in a
queue...

.. literalinclude:: prototype/client_notif_4_robust.py
   :lines: 15-19

.. Problem of the day: make a generator of network commands/responses, I
.. wish I could write: 

     .. for notif in conn.notifs('random'):
     ..     with conn.pause_notifs():
     ..         print (yield random())
     .. maybe possible with corotwine

.. with defer.inlineCallbacks and yield, it seems impossible, the
.. coroutines seems more adapted since they hide asynchronous calls
.. behing a blocking interface.

.. _async:

The advantages of using asynchronous APIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two problems with the previous code:

#. using this seemingly blocking code, it is difficult to model a
   command which results in multiple different events:

   - the **notify** method results in an ``OK`` response and in
     notifications. For each notification, the *waitNotif* method must
     be called. This constraint must be clearly documented to the
     user.

   - the **stopNotify** results in an ``OK`` response but inevitably,
     one day, a notification will be sent right before the stop
     protocol command is received by the server, and the client which
     expects ``OK`` will receive a notification instead. It is out of
     question to ignore this notification which might carry a crucial
     information.

#. the user of the API needs to parse the notification to determine
   the nature of the notification, and the user needs to know the
   exact syntax of the protocol to be able to parse the message.
   
   It is an unnecessary constraint to ask your users to know the
   details of the protocol, there must be a way to decouple the
   protocol parsing from the user code processing the notification.

There is also the smell of a clumsy use of Twisted: there is a ``while
True`` loop running, while the reactor is itself a main loop. Here is
a second approach solves both problems by taking advantage of the
aynchronous nature of the Twisted framework: the *lineReceived* method
of the *Client* class dispatches:

- on hand hand, the responses to commands to callbacks registered in
  the command callback,

- on the other hand, the notifications are parsed and sent to the
  correct notification handler. If the notification handler is not
  implemented, the notification is ignored.

.. literalinclude:: prototype/client_notif_5_async.py
   :lines: 7-22

When a user wants to process a random number notification, the steps
are 1. subclass the *Client* class, 2. implement the *randomAvailable*
method (and create a factory, run the reactor, etc).

.. literalinclude:: prototype/client_notif_5_async.py
   :lines: 51-64    

.. _higher:

Higher level API
~~~~~~~~~~~~~~~~

To adapt to a category of users with little patience for protocol
study, the API can offer an even more straightforward method which
hides the need to switch modes between receiving the notifications and
fetching the newly available items. Here is how to use it:

.. literalinclude:: prototype/client_notif_6_higher.py
   :lines: 65-67


A *randomReceived* method is introduced in a *HigherClient* class,
which derives from the *Client* class. *randomAvailable* is
implemented and simply wraps the notification mode switch:

.. literalinclude:: prototype/client_notif_6_higher.py
   :lines: 48-60

Note that, for the user of the *HigherLevelClient* class, implementing
*connectionMade* is only needed when specific needs arise, and is
unneeded in the simple cases: the *connectionMade* implemented by the
parent class *does the right thing*.

.. _timer:

Defeating the *auto stop-notify* server timer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's extend the protocol specification: let's say the server must
exit the notification mode after 30 minutes of inactivity (using 30
*seconds* is more handy in our tests). To get around this constraint,
the client shall exit and re-enter the notification mode every 29
minutes.

A timeout is set to fire 29 seconds after entering the notification
state. Upon timeout the current deferred is saved, the notification
mode is explicitly exited, then re-entered. Eventually the original
deferred is restored. This upgrade is backward compatible for the
public API.

Our client class not only derives from ``basic.LineReceiver``, but it
additionaly uses the ``policies.TimeoutMixin`` as a base class which
adds the ``setTimeout`` method and offers the ``timeoutConnection``
for the user to implement which is called on timeout. In our context,
the timeout must be set in the ``notify`` method, and canceled in the
``stopNotify`` method. The changes are contained in the ``Client``
class, the methods which are not modified are not displayed.

.. literalinclude:: prototype/client_notif_7_timer.py
   :lines: 5-6,30-36,46-49,53-55

.. _desktop:

Integration with the nice desktop notification system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *pynotify* Python package, when installed on the system, offers
notifications integrated to a desktop compliant with the Freedesktop
specifications. This short example sends the latest random numbers to
the nice and unobstrusive popup in the corner of the screen:

.. literalinclude:: prototype/client_notif_8_desktop.py
   :lines: 72-82

The full source of the notification client can be read
:doc:`here<prototype/full>`, the source for a compliant server can be
found :doc:`here<prototype/server_notify>`.

.. toctree::
   :hidden:

   prototype/full
   prototype/server_notify
