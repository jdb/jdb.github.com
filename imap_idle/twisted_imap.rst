
The IMAP IDLE command in Twisted
================================

IMAP presentation in four keys points
-------------------------------------

- commands, response, data, continuation

- flags,

- tag, sequence numbers, uid

- fetch and rfc 2822

Twisted IMAP support
--------------------

See what is already possible with the existing API: 

- :doc:`_imap4client`: a lightly edited version of the original
  imap4client example. It features comments hinting on how to keep the
  connection in plain text, without TLS, which is easier to debug with
  wireshark. A bug fix: login in a TLS session not considered insecure
  anymore. Script stop the reactor in the end

- :doc:`_imap4client_yield`: a rewrite of the previous script in a
  simpler way using inline callbacks: much more basic and simpler to
  read (the original is 4 times longer)

- :doc:`_imap4client_robust`: an update of :doc:`_imap4client_yield`
  on par with the original examples. Still twice shorter: inline
  callbacks are really helpfull if you are do not have to deal with
  Python version before 2.5.

Main classes, main functions

How are the deferreds stored

The state machine in the client

The algorithm of our extension to Twisted
-----------------------------------------

1. Send the right command IDLE command,

2. Add the IDLE command to the authorized set of commands in
   auth STATE,

3. Define the untagged responses acceptable for IDLE,

4. Play with the exists number coming through the notifications
   to guess the sequence numbers and the unique messages ids,

5. Do the right fetch on the latest sequence numbers and on the
   pattern


So in the end, what is really in the patch
------------------------------------------

- :doc:`_imap4client_yield2`: an update of :doc:`_imap4client_yield`
  with the notify features


I am not sure I see the state machines clearly: 

- how does the IMAP4Client ensures the response is one of the
  authorized ones?

- how does the IMAP4Client client makes sure only commands sent are
  authorized ion the current mode (unauth, auth, selected)?

Here are the events involved in a simple notification server:

#. 



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

Here is the client procotol:

.. literalinclude:: twisted_exceptions.py
   :pyobject: ConnectInbox


Here is the associated factory:

.. literalinclude:: twisted_exceptions.py
   :pyobject: ConnectInbox

Here is the "higher level" function:

.. literalinclude:: twisted_exceptions.py
   :pyobject: getTitles

And here is how these objects are instantiated and called via the
reactor:

.. literalinclude:: twisted_exceptions.py
   :start-after: __main__

