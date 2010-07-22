
The IMAP IDLE command in Twisted
================================

.. todo::

   Rethink this page which is ugly to read and might be too long.

IMAP presentation in four keys points
-------------------------------------

- commands, response, data, continuation: TODO

- flags: TODO

- tag, sequence numbers, uid: TODO

- fetch and rfc 2822 parts: TODO

IMAP IDLE
---------




Twisted IMAP support
--------------------

Here three examples deriving from the script contained in the official
documentation, which can connect to an IMAP mailbox and retrieve the
messages subjects:

- :doc:`twisted_imap/imap4client`: the original Twisted imap4client
  example,

- :doc:`twisted_imap/imap4client_yield`: the same script using the
  recent *inline callbacks*: much more basic and simpler to read (the
  original is 4 times longer). 

- :doc:`twisted_imap/imap4client_robust`: on par with the features of
  the original example but still twice shorter. Arguably, inline
  callbacks do help with readability (if you are not stuck with a Python
  version before 2.5)

How does a command gets sent?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's take the example of the status method

#. a Command object is instantiated with: 

   - the *STATUS* string as the command,

   - the command arguments,

   - the continuation function and its arguments,

   - the expected response (is unused at this time)

#. *sendCommand* 

   - takes this Command instance as an argument, 

   - stores a deferred in the cmd,

   - if there is a reply expected for a running command: queue the
     command and returns the command deferred,

   - else :

     - make a tag number which identifies the request, 

     - stores the command in the tags member dictionary

     - send the request and returns the deferred

#. the *__cbStatus* callback which parses the reply string into a dictionary
   and returns the dictionary is attached to the deferred


How does a network reply gets processed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. *lineReceived* is meant to distinguish between the lines and the
   literal strings. The case of literal strings is of minor importance
   in our context: in case of a line, it is split into:

   - the tag which can be either ``*``, ``+`` or an IMAP tag
     according to the RFC 3501,

   - and the rest which comprises of the response name and arguments.

   The tag and rest are passed to:

#. the *dispatchCommand* which selects a handler for the data based on
   the client state: the state of the Twisted client can be either
   *UNAUTH*, *AUTH* (the IMAP state *selected* and *logout* are
   comprised into the *AUTH* Twisted state).

#. The *response_AUTH* handler, which correspond to our context, hands
   the the *tag* and *data* to:

#. the *_defaultHandler* has several cases:

   - if the response is **untagged**
   
     - if the client is **not waiting** for an answer the *_extraInfo*
       method is evaluated with the tag and rest as arguments.

     - if the client is **waiting**, the *waiting* member attribute
       contains the tag number. Using the *tags* dictionary, which
       stores the tag as keys and the Command object instance as
       value, it is possible to reach to the command name, the
       received line buffer, the continuation function, the deferred
       and its callback. Because the response is untagged, either it
       is :
       
       - a **continuation** (``+``), in which case the continuation
         function is called

       - a **data** (``*``), in which case the data is appended to the
         buffer. The buffer is used the tagged response arrives.

   
   - if the response is **tagged**, it is a final response, the finish
     method, of the command object instance corresponding to the tag,
     is executed.

#. the finish method of the command object parses the buffer of lines
   and executes the callback with the received lines.



These steps are not adapted to the processing of notifications as:

- there is no callback stored for the message from the server
  *accepting notifications*, the ``+ idling`` continuation data requests

- the data is buffered until the reception final tag response which
  triggers the callback of the command while a user callback should be
  executed for each notification,

The algorithm of our extension to Twisted
-----------------------------------------

#. Send the IDLE command, returns a deferred which is triggered, not
   on the final tagged response but on the reception of ``+ idling``

#. Play with the exists number coming through the notifications
   to guess the sequence numbers and the unique messages ids,

#. Do the right fetch on the latest sequence numbers and on the
   pattern


#. Add the IDLE command to the authorized set of commands in
   auth STATE,

#. Define the untagged responses acceptable for IDLE,



Patching the twisted.mail.imap module
-------------------------------------

- :doc:`twisted_imap/imap4client_notif`: an update of
  the simpler version seen above with the notify features

I am not sure I see the state machines clearly: 

- how does the IMAP4Client ensures the response is one of the
  authorized ones?

- how does the IMAP4Client client makes sure only commands sent are
  authorized ion the current mode (unauth, auth, selected)?

Here are the events involved in a simple notification server:

#. 

How can this API be used
------------------------

(and yes it is a shame errors are completely ingored)

The pattern for this task is :

#. A client factory deriving from tw.in.pr.ClientFactory, configured
   with the server name, port, user, account and mailbox

#. A protocol deriving from tw.pr.imap4.IMAP4Client which connect to
   the mailbox on serverGreetings and calls the factory deferred

#. A higher level function attached to the factory deferred expecting
   a connection to the inbox and fetching the latest emails titles

The chronological steps are:

#. declare the client factory, the protocol, and in the main: the
   higher level function which receives the list of email in the inbox
   and prints them

#. instanciate a factory with the account information

#. attach the higher level function to the deferred factory

#. attach the factory to the reactor with a TCPConnect and the
   mailserver informations

#. run the reactor 

#. the TCP connection is opened triggering the buildprotocol on the
   factory, returning a protocol instance on which connectionMade is
   called which says "hi" to the server

#. the server replies with its greetings and capabilities, triggering
   the protocol serverGreetings callback:

   #. login

   #. select the correct mailbox

   #. download the message subjects

   #. call the factory deferred with the result

#. the function prints the title and stops the reactor

02 51 68 50 63
5, rue des pins
Fromentine
