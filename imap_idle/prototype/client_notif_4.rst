
The user code is contain in one function
----------------------------------------

This iteration does not add new functionalities to the code, it
refactors the code to cleanly separate a general API from a specific
client script. There is no more need to derive a class and override a
specific method to process a notification. It is only a matter of
using the API in one function. 

.. literalinclude:: client_notif_4.py
   :lines: 38-55

