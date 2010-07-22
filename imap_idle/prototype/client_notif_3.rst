
the client loops and ends the notification mode to get the available new item
-----------------------------------------------------------------------------

A client watching for notification is expected to loop to act on the
notifications. Also, whenever an interesting notification arrives, it
is the signal that new data is available. The API is not modified,
only the code executing when the connection is established is extended.

.. literalinclude:: client_notif_3.py
   :lines: 37-50

