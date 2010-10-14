
Robustness
==========

Even in the simple first iteration of the client when it was only able
to send requests and receive responses, the client crashes under
various conditions:

#. when a crazy server sends unexpected data: either before the client
   has sent anything, or because the server responses arrives twice on
   the client,

#. when a crazy client developer decides to send multiple messages in
   a burst without waiting for the response to the first command to be
   returned first,

The following methods are to blame::

  class Client(basic.LineReceiver):
    
      def command(self, cmd):
          self.sendLine(cmd)
          self.d = defer.Deferred()
          return self.d

      def lineReceived(self, data):
          self.d.callback(data)

In case 1., when a line is received, the *callback()* method is called
on the *d* member attribute which must be present. As *d* is only
created when *command()* is executed, the client crashes when the
server sends a data prior to any client request.

In case 2., when three commands are sent, three responses will come
back, there should be three deferred, one for each response. But the
deferred created in *command()* overwrite the previous deferred, even
if the response has come back yet. The first response is correctly
handed to the callback contained in *d* but the reception of the
second response will result in a second call of the *callback()*
method which is forbidden, the method triggers an
``AlreadyCalledException`` exception.

Clients should not crash when facing an uncompliant server: peers must
not only be correct but also need to be robust. In our prototype, when
a line is received, the *callback()* method of the *self.d* member
attribute is executed: both self.d and its *callback()* method must
exits. Even more, as a deferred raises an *AlreadyCalledException*
when called a second time, it must be suppressed whenever triggered.

To avoid case one: duplicate and unexpected data should be ignored. A
line received should be ignored if there is no callback registered
i.e. if the *d* member attribute is *None*. ::

  class Client(basic.LineReceiver):

      d = None    

      def lineReceived(self, data):
          if self.d is not None:
              self.d.callback(data)

To avoid case 2., let's just forbid the client to send a command when
the client is already waiting for a command. This choice puts a
constraint on the developer as an exception will be raised if the
developer tries. Another solution could be to spool the commands in a
queue, but then how do one decides on the max size for the queue?::

    def command(self, cmd):
        assert self.d is None
        self.sendLine(cmd)
        self.d = defer.Deferred()
        return self.d


.. _higher:

Higher level API
================

To accomodate category of users with little patience for protocol
study, the API can offer an even more straightforward method which
hides the need to know about switching modes between receiving the
notifications and fetching the newly available items. Here is how to
use it::

  class MyClient(NotifClient):
      def randomReceived(self, random): 
          print random

A *randomReceived* method is introduced in a *HigherClient* class,
which derives from the *Client* class. *randomAvailable* is
implemented and simply wraps the notification mode switch:

.. literalinclude:: curious/client_notif_full.py
   :lines: 56-68

Note that, for a developer deriving the *HigherLevelClient* class,
implementing *connectionMade()* is only needed when specific needs
arise, and is unneeded in the simple cases: the default
*connectionMade()* implemented by the parent class does what is commonly
expected by its users.

.. _timer:

Server inactivity timer
=======================

Let's extend the protocol specification to add a the common *time out*
feature: let's say the server must exit the notification mode after 30
minutes of inactivity (using 30 *seconds* is more handy in our
tests). To get around this constraint, the client shall exit and
re-enter the notification mode every 29 minutes.

A timeout is set to fire 29 seconds after entering the notification
state. Upon timeout the current deferred is saved, the notification
mode is explicitly exited, then re-entered. The original deferred is
restored. This upgrade is backward compatible for the public API.

Our client class not only derives from ``basic.LineReceiver``, but it
additionaly uses the ``policies.TimeoutMixin`` as a base class which
adds the ``setTimeout`` method and offers the ``timeoutConnection``
for the user to implement which is called on timeout. In our context,
the timeout must be set in the ``notify`` method, and canceled in the
``stopNotify`` method. The changes are contained in the ``Client``
class, the methods which are not modified are not displayed.

.. literalinclude:: curious/client_notif_full.py
   :lines: 5-6,29-34,45-47,52-54

.. _desktop:

Nice desktop notifications
==========================

The *pynotify* Python package, when installed on the system, offers
notifications integrated to a desktop compliant with the Freedesktop
specifications. This short example sends the latest random numbers to
a nice and unobstrusive popup in the corner of the screen:

.. literalinclude:: curious/client_notif_full.py
   :lines: 76-83

The full source of the notification client can be read
:doc:`here<curious/client_notif_full>`, the source for a compliant
server can be found :doc:`here<curious/server_notify>`.

