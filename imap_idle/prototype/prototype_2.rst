
loop on notifications until killed with a control-C,
----------------------------------------------------

The notify command arms two deferred, the usual deferred for the reply
to the notify command: *d*. The response for this command will
actually much later, when the client sends the stop_notif data to the
server. Only at this point, the server will send the OK reply which
acknowledges the completion of the ``notif`` command.

.. literalinclude:: prototype_2.py
