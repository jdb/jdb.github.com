
==================================
 A notification client in Twisted
==================================

Let's create a simple client able not only to send requests and process
responses but also able to receive notifications. It will be a client
supporting the super simple custom protocol presented in the first
section. Let's see then how this protocol maps to Twisted's
abstractions. Finally, we present the steps of an implementation
of a client in Twisted.

.. _protocol:

A simple hand made protocol
===========================

The protocol is based on strings terminated by a newline, it includes
four commands:

- ``random?``: the server should return a random number,

- ``classified?``: the server should return the recent unread
  classified ads,

- ``notif``: the server gets ready to send notifications about new
  items being available,

- ``stop_notif``: the server stops sending notifications and just
  waits for client requests. For ``notif`` and ``stop_notif``, the
  server replies ``OK`` to accept the command.

A notification can either be : ``notif: random`` or ``notif:
classified`` and is used by the server to notify the client of the
availability of random numbers and classified ads. Then, it is up to
the client to exit the notification mode by sending the data
``stop_notif`` to complete the ``notif`` command and then effectively
download the random number or the classified ad, whatever the client
is interested in. 

The protocol will typically be used in the following manner: The
client connects, retrieves the most recent items either a random
number or a classified ad it is interested in and requests the server
to send notifications about newly available items. For each
notification sent by the server, the client will exit the notification
mode to explicitly download the items. Here is an example session,
recorded on the server (the line begins with ``S:`` if sent by the
server, ``C:`` if sent by the client)::

  C:  random?
  S:  456902234

  C:  classified?
  S:  Nice appart in the 10e.

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
  [...]

This section briefly specified a protocol, the next section describes
how to design a client implementating this protocol with Twisted.

.. _twisted:

The Twisted objects involved
============================

The protocol has three kinds of exchange: requests/responses and
notifications. Here is a way to process requests/responses with
Twisted objects:

#. **request**: the client *Protocol* instance formats the correct
   command string and writes it in the *transport* attribute of the
   *factory* of the *Protocol* instance to initiate the request. A
   line based *Protocol* class has the helper method *sendLine* for
   this task.

   .. make api links from the classes to the Twisted API
   
   At the same time, it creates a container for the code processing
   the response and stores it as an instance attribute of the
   *Protocol*. The container is called a Deferred and has two main
   methods: *addCallback()* which is used to store the code meant to
   process the response and *callback()* which is executed to launch
   the callback with the received data passed as an argument.

   The deferred is returned by the requesting method so that the
   caller can attach the callback of this choice with the *addCallback()*
   method.

#. **response**: *lineReceived* is called automatically by Twisted as
   soon as the response comes back in the *transport*. *lineReceived*
   is called with the response data as argument and usually hands the
   data to the callback stored in the deferred.

   The deferred is *consumed* whenever *callback()* is called and must
   be regenerated at each requests.

Notifications actually *invert* the role of client and server as the
*server* initiates the notifications and the client is waiting,
listening to the notifications. With Twisted's abstractions, here is a
first approach to process notifications:

#. the client sends a command for the server to go into notification
   mode, and sets a callback in the returned deferred as usual,

#. the server accepts and sends an ``OK`` response, the callback is
   fired and here is the difference with the traditional client/server
   exchange:

#. a method generating storing and returning a deferred needs to be
   called to attach a callback of the next notification,

#. at some point, the server sends a notification which is is handed
   by Twisted to the client *lineReceived()* which as previously
   explained routes the notification to the callback.

   The client code receives the notification and might decide to
   expect other notifications, or turn to "normal" mode to actively
   command the server. When done, the client can go back to normal
   mode, when the notification has been actively processed, it is up
   to the client to reinitiate the notification mode.

Let's put these steps into code.

Three iterations
================

Our prototype is built in three steps, while the first step simply
implements commands/reponses, the next steps show two attempts to
implements an API to handle notification events:

#. :ref:`command_response` 
#. :ref:`notifs`
#. :ref:`async`

.. _command_response:

commands/responses
------------------

A basic implementation of a Twisted client for this simple protocol
class can derive from the *LineReceiver* Protocol:

- the client API is based on the *command()* internal method which
  sends the command string on the network and returns a *Deferred*, to
  which the user can attach the code meant to process the result,

- *lineReceived()* is called by Twisted when a a response from the
  server is available. The response gets passed to the callback set by
  the user,

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

For more details on *defer.inlineCallbacks* and the peculiar use of
*yield*, see :doc:`../../concurrent/smartpython`. In brief, the
association of the two makes it possible to turn a function returning
a deferred which fires a result into a more conventional function
which reads as if it blocks until returns a result (while it does not
actually block!).


.. _notifs:

notifications: 1st try
----------------------

This iteration introduces three methods in our *Client* class
protocol, for supporting the events related to the ``notif``
and ``stop_notif`` protocol commands:

- *notify()*: requests the server to switch to notification
  mode. Returns a callback which will fire ``OK`` according to the
  :ref:`protocol definition <protocol>`

- *waitNotif()*: installs and return a deferred, used to attach a
  callback processing the notification. ``yield waitNotif()`` is an
  expression which returns the notification when used in a function
  decorated by *inlineCallbacks*.

- *stopNotify()*: ends the notification mode, and switches the server
  back into the traditional client/server mode. 

.. literalinclude:: prototype/client_notif_2_notifs.py
   :lines: 24-32

The changes made to *connectionMade()* illustrates how to use the API
from a user point of view. In particular, the client never stops as it
is listening to notifications.

.. literalinclude:: prototype/client_notif_2_notifs.py
   :lines: 34-50

Here is an example of the client script execution::

  $ python prototype/client_notif_2.py 
  34478
  43482
  "not interested, will wait for the next notif"
  47395

.. _async:

notifications: a better API
---------------------------

In a way, the line which calls waitNotif() can be read as a call which
blocks until it returns the notification. There are two problems with
this design:

#. the user of the API needs to parse the notification data to
   determine the nature of the notification, which requires the user
   to know the exact syntax of the protocol to be able to parse
   the string to direct the execution flow toward the correct code
   depending on the notification.

   Even if the parsing is eased and wrapped into higher level symbols,
   the user stil have to test for the event and dispatch to the
   correct processing code.

   There must be a way to cleanly separate the responsibilities of
   protocol parsing (which belongs to the protocol implementor) from
   the processing of the event (which is up to the user). After all,
   the only thing on which user wants to write is the code processing
   the event.
   
#. using this seemingly blocking code, it is difficult to model *one
   function which results in multiple, delayed events of different
   types*. Here the ``notif`` command results in an acknowledgment
   and then potentially multiple notifications:

   - the **notify** method results in an ``OK`` acknowledgement
     response and in potentially multiple subsequent
     notifications. Also, for each notification, the *waitNotif()*
     method **must** be called. This constraint must be clearly
     documented to the user.

   - the **stopNotify** results in an ``OK`` response but inevitably,
     one day, a notification will be sent right before the stop
     protocol command is received by the server, and the client which
     expects ``OK`` will receive a notification instead. It is out of
     question to ignore this notification which might carry a crucial
     information.

There is also the *smell* of a clumsy use of Twisted: there is a
``while True`` loop running, while the reactor is itself already a
main loop and. Here is a second asynchronous approach solves both
problems, the *lineReceived()* method of the *Client* class parses the
data received and :

- dispatches, on one hand hand, the responses to commands toward callbacks
  stored in the command *Deferred*,

- dispaches on the other hand, the notifications toward the correct
  notification handler. If the notification handler is not
  implemented, the notification is simply ignored.

The user of the API must implement two functions in the *Protocol*
child class: the *connectionMade()* and the *randomAvailable()*
callback.

.. literalinclude:: prototype/client_notif_3_async.py
   :lines: 46-57

The parsing of the line received is moved to the  *lineReceived()*
methods, under the responsability of the protocol implementor, and
there is no need for a seemingly blocking *waitNotif()* method. A
verification that the server acknowledged the ``notif`` and
``stopNotify`` request can be added, the user of the API do not have
to care.

.. literalinclude:: prototype/client_notif_3_async.py
   :lines: 7-16    

The full version of this script can be read here
:doc:`prototype/client_notif_3_async`. For the curious a subsequent
iteration can be read :doc:`here <curious>`, it adds robustness, a
higher level API, a workaround for the automatic disconnection from
the notification mode, and an integration to the nice freedesktop
notifications.

Now that the overall mechanism for handling notification events with
Twisted abstraction have been presented on a simple protocol, let's
see how this mechanism is actually implemented in the context of the
IMAP protocol.

