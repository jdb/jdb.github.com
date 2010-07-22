
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

.. literalinclude:: client_notif_2.py
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

  ~$ python client_notif_2.py 
  34
  43
  will send notif
  a notif: 'notif: random'
  a second notif: 'notif: random'
  OK

.. there is a bug is notify are called without waitNotif: alreadycalledcallback
