
A notification server in Twisted
================================

Let's create a simple client able to receive notification. It will be
super simple client which does not support HTTP nor IMAP. The goal is
just to play with a server to client notification mechanism: the
traditional situation for a client and server application is for the
server to initiate requests and the server to generate responses.
Notifications actually *inverts* the role of client and server as the
serveur initiates notification that the client acknowledge..

#. a client opens a connection to a serveur,

#. the client emits a traditional request and receives an answer, in
   our example, the client will request a random number.

#. the client requests to go into notification mode, the server
   accepts. The server notifies the client when there is a new
   appartment in town is offered for renting.

#. the client does nothing, and at some point, the server sends a
   notification. The client receives the notification and might decide
   to exit the notification mode and sends the request to receive the
   details of the offer.


Expressing a server to client notification mechanism in Twisted
involves several classes:

#. a client protocol,

#. a server protocol,

#. the right deferred dance,

#. a factory and a reactor


The client protocol
-------------------

The client Protocol has commands for requesting:

- random numbers, 

- renting offers details,

- changing state to listening for notification. 

Let's design our mini protocol to be line oriented:
  we will be able to

the client Factory is not really useful in our example: the reactor
requires the factory to be able to offer a protocol instance 

Deferred



