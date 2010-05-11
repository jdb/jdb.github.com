
.. mettre des liens vers les tutoriaux

=============================================
 Concurrent network programming with Twisted
=============================================

What is Twisted?
================

Twisted_ is a an organised set of Python modules, classes and
functions aiming at efficiently building network client or server
applications. Twisted base classes wrap the UDP, TCP and SSL
transports and child classes offer well tested, application protocol
implementations which can coherently weave file tranfer, email, chat
and presence, enterprise messaging, name services, etc. 

.. _Twisted: http://twistedmatrix.com/trac/

Twisted is written in Python and is fast partly because the data is
processed as soon as it is available no matter how many connections
are open. This *event-driven networking engine* enables developers to
produce a stable and performant mail transfer agent or domain name
server with less than fifteen lines of code.

Dumb simple example here.

Also, Twisted has methods for implementing features which are often
required by sophisticated software projects. For instance, Twisted can
map a tree of ressources behind URLs, can authentify users against
flexible backends, or can safely distribute objects on a network
enabling remote procedure calls and load balancing. 

Twisted really_ has_ many_ modules available.

.. _really: https://launchpad.net/tx

.. _has: http://twistedmatrix.com/documents/current/core/howto/index.html

.. _many: http://twistedmatrix.com/trac/wiki/TwistedProjects 

:doc:`who <concurrent/who>` |




