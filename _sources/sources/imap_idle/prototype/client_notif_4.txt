
The user code is contain in one function
----------------------------------------

There is no more need to derive a class and override a specific method
to process a notification. It is only a matter of using the API in one
function separated from the protocol class. It is a simplification
that actually does not buy much, it a higher level function which gets
called when the connection is established, with the protocol instance
as argument.

.. literalinclude:: client_notif_4.py

Here is the same script without API, where the protocole is exposed in
raw form. This make it quite clear, what really is echanged on the
wire, and what it happening with the protocol strings exchanged and the
deferreds.

.. literalinclude:: client_notif_4raw.py
