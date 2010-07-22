
Higher level API
----------------

A *receive* method is introduced in the *Client* protocol Class which
allows the user of the API not to know a specificity of the protocol
which is to switch modes between receiving the notifications and
fetching the newly available items.

Here is a higher level *receive* method which encapsulate the
notification mode:

.. literalinclude:: client_notif_5.py
   :lines: 36-52

For a user which only wants to receive the random number as fast as
possible, the code is much more straightforward:


.. literalinclude:: client_notif_5.py
   :lines: 56-63
