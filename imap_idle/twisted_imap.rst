
The IMAP IDLE command in Twisted
================================


IMAP presentation in five keys points
-------------------------------------

IMAP is protocol to access and watch a remote mailbox, it is possible
for several client might be connected simutaneously and use the
mailbox concurrently. Also, the remote mailbox keeps the emails until
they are explicitly deleted; they are not deleted when they are
fetched from the client.

#. There are four types of messages, most of them are *commands* and
   *responses* but some commands such as authenticate, and interestingly
   *idle* will require messages of type *continuation data request* and
   *continuation data*.

   - **commands**, such as login, search, fetch, copy demand
     **responses**.
 
     First, there are responses with the information that the client
     need and then, there is one a line which terminates the response,
     which holds a status (either OK, NO, or BAD). This line is easily
     distinguished from the information lines because it begins with
     the **tag**: it is a unique number identifying the response to the
     command which carried the tag in the first place. When two
     commands are sent without waiting for the first response to
     arrive, the tag allows to dispatch the tagged response to the
     correct command.

     The final response which has a tag is called the tagged response,
     while the others are the untagged responses.

   - **continuation data requests**, and **continuation data**: for
     some commands, the command can not be completely sent in one
     step, the server will need some additional information. In this
     case, the server sends a *continuation data request*: it is a
     line beginning with *+*. The *authenticate* use this continuation
     pattern, and the *idle* command too.
 

#. **Sequence numbers**, and **UIDs**: messages in the mailbox have two
   identifiers. 
   
   The sequence number is unique to a message and a mailbox: it is
   possible to have two messages with sequence number 10 in two
   different mailboxes. Also, the message sequence number for a message
   might change over time. The server must enforce some rules on the
   sequence such as, for instance, there can't be a gap in the
   sequence, it starts at 1, new messages always get a sequence number
   higher than the existing messages. For a message in the mailbox, the
   sequence number can change.
 
   Then, the next message sequence number is predictable on the client
   without having to request the server. Just by knowing the number of
   new messages or the number of deleted messages, it is possible to
   deduce the sequence number of new messages and fetch them.
 
   The UID is a different identifier, it is a unique identifier accross
   mailbox and stays the same even if the messages are moved. It is
   possible to fetch messages by using the UID but in general the
   sequence number is used instead.

#. Since IMAP keeps the messages on the server until explicitly
   deleted, it is not necessary to store them all on the client. Also,
   when using the **fetch** commmand, the commands argument's can
   precisely describe the parts to download, for instance, only the
   *from* and *subject* headers. The specification for the messages parts
   understood by IMAP is the standard email format standard: the
   RFC2822.

#. Messages in the mailbox have the standard headers and body, but
   additionally, they have attributes called **flags**, named *seen*,
   *recent*, *answered*, *draft*, *deleted*, *flagged*. Flags are
   stored on the server and allow multiple clients to be connected to
   the same mailbox. For instance, without intervention from client
   #1, the *seen* flags of a message can become set to true, just
   because client #2 has fetched it.

#. The RFC 2177 defines an extension to the IMAP protocol defining how
   a client can request the server to send notifications. The **IDLE
   command** is sent, and a continuation request from the server ``+
   idling`` acknowledges that the server accepts the requests. No
   continuation data is actually sent to the server, and no tagged
   response is sent by the server to complete this command until the
   client explicitly request the command completion by sending the
   ``done`` continuation data.

   Between the *idle* command and the ``done`` data, the client might
   receive notifications in the form of untagged responses, especially
   the EXPUNGE and NEW responses.
   
Twisted's extension to support the idle command
-----------------------------------------------

Here is a :doc:`script <twisted_imap/imap4client_yield>` which shows
how Twisted supports interacting with an IMAP server: it logs in to a
account and retrieves the subjects of the mails in the inbox mailbox
[#]_.

The ``getMailboxConnection`` function is the first step of the script,
it can be called with a destination (server name, port and mailbox
name), and returns a deferred which fires an *IMAP connection*
instance, when the connection is ready:

.. literalinclude:: twisted_imap/imap4client_yield.py
   :pyobject:  GetMailboxConnection

The user has to attach a callback to this deferred, operating on the
mailbox via the methods of the IMAP connection instance. In this
script, the ``getSubjects`` function sends the *fetch* command to
retrieve the subjects of every mail in the inbox:

.. literalinclude:: twisted_imap/imap4client_yield.py
   :pyobject:  getSubjects

The next section explains exactly how Twisted handles the operation of
sending the *fetch* command, and the subsequent section get into the
details of how the response to this command is handled. When these
mechanism are understood, it is possible to propose an algorithm for
the *IDLE* patch.

How does a command gets sent?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. a **Command** object is instantiated with: 

   - the *FETCH* string as the command,

   - the command arguments,

   - the continuation function and its arguments,

   - the expected response (is unused at this time)

#. **sendCommand** 

   - takes this Command instance as an argument, 

   - instantiates a deferred stored in the command instance,

   - if the client waits for a response: queue the command and returns
     the command deferred,

   - else :

     - make a tag number which identifies the request, 

     - stores the command in the tags member dictionary,

     - call the format method of the *Command* instance to produce the
       correct request string,

     - returns the deferred

#. the **__cbStatus** callback which parses the reply string into a
   dictionary and returns the dictionary is automatically attached to
   the deferred

How does a network reply gets processed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. **lineReceived** is meant to distinguish between the lines and the
   literal strings. The case of literal strings is of minor importance
   in our context: in case of a line, it is split into:

   - the tag which can be either ``*``, ``+`` or an IMAP tag
     according to the RFC 3501,

   - and the rest which comprises of the response name and arguments.

   The tag and rest are passed to:

#. the **dispatchCommand** which selects a handler for the data based on
   the client state: the state of the Twisted client can be either
   *UNAUTH*, *AUTH* (the IMAP state *selected* and *logout* are
   comprised into the *AUTH* Twisted state).

#. The **response_AUTH** handler hands the *tag* and *data* to:

#. the **_defaultHandler** has several cases:

   - if the response is *untagged*
   
     - if the client is **not waiting** for an answer the *_extraInfo*
       method is evaluated with the tag and rest as arguments.

     - if the client is **waiting** for a response, the *waiting*
       member attribute contains the tag number. Using the *tags*
       dictionary, which stores the tag as keys and the Command object
       instance as value, it is possible to reach to the command name,
       the received line buffer, the continuation function, the
       deferred and its callback. Because the response is untagged,
       either it is :
       
       - a **continuation** (``+``), in which case the continuation
         function is called

       - a **data** (``*``), in which case the data is appended to the
         buffer. The buffer is used the tagged response arrives.

   
   - if the response is **tagged**, it is a final response, the finish
     method, of the command object instance corresponding to the tag,
     is executed.

#. the finish method of the command object parses the buffer of lines
   and executes the callback with the received lines.


.. [#] This script is simple and easy to read, but the following
       :doc:`twisted_imap/imap4client <version>` is compatible with
       python 2.3 and actually handles the error cases.

Our Twisted IMAP IDLE patch
---------------------------

IMAP IDLE
~~~~~~~~~





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




