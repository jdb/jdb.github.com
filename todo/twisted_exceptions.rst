
It is not cristal clear at first how twisted handles exceptions. Look
at this example. Trying to connect to a IMAP server and retrieve the
*subject* lines of the email.

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
   :start: if __name__=="__main__":

