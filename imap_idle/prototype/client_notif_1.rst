
The client can send a request get a reply
-----------------------------------------

This is one of the most basic implementation of a Twisted client:

- the client *high level* API is based on the *command* method which
  formats the network request and returns a Deferred, to which the
  user can attach the code processing the result,

- *lineReceived* is an internal command called by Twisted, when a a
  reply from the server is available. The reply gets passed to the
  callback set by the user,

.. literalinclude:: client_notif_1.py

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
:doc:`robustified version <client_notif_7>`.

For more details on *defer.inlineCallback* and the peculiar use of
*yield*, see :doc:`../../concurrent/smartpython`. In brief, the
association of the two makes it possible to turn a function returning
a deferred which fires a result into a more conventional function
which (*seemingly*) returns a result.

