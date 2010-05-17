
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
implementations which can weave file tranfer, email, chat and
presence, enterprise messaging, name services, etc, with the same
mental model.

.. _Twisted: http://twistedmatrix.com/trac/

Twisted is written in Python and is fast partly because the data is
processed as soon as it is available no matter how many connections
are open. This *event-driven networking engine* enables developers to
produce a stable and performant mail transfer agent or domain name
server with less than fifty lines of code.

Also, Twisted has methods for implementing features which are often
required by sophisticated software projects. For instance, Twisted can
map a tree of ressources behind URLs, can authentify users against
flexible backends, or can safely distribute objects on a network
enabling remote procedure calls and load balancing, etc (Twisted has_ many_
modules_ available).

.. _modules: https://launchpad.net/tx

.. _has: http://twistedmatrix.com/documents/current/core/howto/index.html

.. _many: http://twistedmatrix.com/trac/wiki/TwistedProjects 


This article introduces the problem of network concurrency, and
compares Twisted's model to the sequential model through the example
of web pages download. This article points to other articles along the
lines which they present with more depth the concepts only mentioned
here. They are listed here for memo:

.. toctree::
   :maxdepth: 1

   Comparison with threads and sockets <concurrent/preemptive>
   Twisted's core objects : the reactor and the Protocols <concurrent/reactor>
   Twisted's abstraction for pending results: the Deferred <concurrent/deferred>
   concurrent/smartpython

Retrieving the title of a list of blog articles
===============================================

Network concurrency is a key concept particularly for performance:
take a simple problem such as retrieving, for each blog of a list of
blogs, the title of the web page of the first article of the
blog. This first problem is actually the core job of a Web scraper or
a crawler. This means::

    for each blog url 
        retrieve the list of articles 
    	parses the first article url in the list
        retrieve the web page of the first article	
        display the title

Let's provide a quick and naive solution to this problem. Here are
three handy functions :

- **urlopen**\ (url) sends an HTTP GET request to the url and returns
  the body of the HTTP response as an open file,

- **parse**\ (HTML string) takes an HTML string as an input and
  returns a tree structure of HTML nodes,

- htmltree.\ **xpath**\ (pattern) returns a list of nodes matching the
  pattern. The text content of a HTML node is accessed via the member
  attribute ``.text``. We will use **xpath**  to find urls or page titles
  in a HTML document.

And here is the script which brings all this together (and includes a
design problem):

.. include:: concurrent/sequential.py
   :literal:

Concurrency vs sequential processing
====================================

When there are *n* element in the blog list, there will be *2n* page
downloaded, one after the other, and this will take *2n * time to
download a page*. When the time taken by an algorithm is directly
proportional to the number of inputs, this is called a linear
complexity and this will rightfully raise the eyebrow of any developer
concerned with performance and scalability.

As each download is completely independent from each other, it is
obvious that these downloads should be executed in parallel, or,
*concurrently*, and this is the raison d'être of the Twisted Python
framework. :doc:`Processes and threads <concurrent/preemptive>` are
well-known primitives for programming concurrently but Twisted does
without (not even behind your back), because it is not adapted for
scalable network programming. This frees the developer from using
locks, recursive locks, or mutexes. The solution presented at the end
of the article does not have more lines of code, does not take much
longer for *n* downloads than it takes for one download (ie *constant
complexity*) and is actually three times faster.
	
A frequently heard reaction at this point is "Python is a slow
language to start with, **a fast language** is the answer to
performance". Notwithstanding the many existing techniques to make
Python code compile and run on multiple processors, the speed of the
language is not the point. In many case, even a C compiler can not fix
a bad design. For example, take the download of an install CD, there
is an insignificant gain in performance in a download client written
in C over an implementation in Python, because 1. both implementations
are very likely to end up leaving the network and disk stuff to the
kernel and most importantly because 2. this job is inherently bound by
the network bandwidth, not by CPU computations, where C shines. Both
in C and in Python, in the context of multiple downloads, performance
depends on concurrent connections. 

This example is obvious but most network libraries blocks when doing a
network request. This is the core idea: **Twisted functions which make
a network call do not block the application while the response is not
yet available**. Network functions are split: first the request is sent,
then the *callback* code receives and manipulates the received
data. **In the period of time between the return of the requesting
function and the execution of the callback, the** :class:`reactor`,
**(Twisted's event loop) can run other processing**. This is
the basic idea which makes asynchronous code faster than blocking
code.

A concurrent solution
=====================

Here is a concurrent solution to the blog problem. It is three times
faster than the sequential approach:

.. include:: concurrent/concurrent_dontstop.py
   :literal:

The Twisted equivalent of :func:`urlopen` is called
:func:`getPage`. It is asynchronous and returns a :doc:`deferred
<concurrent/deferred>`. The low level steps composing :func:`getPage`
are asynchronous as well: even the DNS request turning the url
argument into an IP address will not block the application and let
other processing occurs.

*The page* :doc:`concurrent/smartpython` *explains the Python yield
keyword and decorator syntax in the context of Twisted. The page*
:doc:`concurrent/reactor` *gives a precise overview of how Twisted
works at the operating system system.*

Want to learn more? The project documentation_ presents many code
examples and reference articles. Would you trust the Twisted framework
for your core business development? Hmm, difficult question: maybe you
can check at the development methods_ to get the beginning of an
answer.

.. _documentation: http://twistedmatrix.com/documents/current/core/howto/index.html

.. _methods: http://twistedmatrix.com/trac/wiki/ContributingToTwistedLabs

*15 May 2010*

.. This article leaves many questions aside. For instance, error handling
.. is non existent in the scripts: manipulating deferreds explicitly,
.. though more verbose, help creating clearer failure code path and help
.. create more robust application and libraries. In our script, as well
.. as when building network applications or libraries, the following
.. problems may arise: no network, no dns, no route, no tcp server, page
.. not found error, HTML title not found. How easy it is to handle them
.. gracefully?


.. Twisted use asynchronous functions to solve concurrency, how does it
.. compare to thread or process (the :func:`threading` and
.. :func:`multiprocessing` python module)? What does it mean for shared
.. object and race condition? How does it compare with the *libdispatch*,
.. erlang, haskell, stackless python, greenlet, coroutine or scala ways
.. of doing concurrency?

.. Win95 way of doing things is not adapted for an OS were it is
.. difficult to control that every code executing "behaves" and return
.. fast, it is much more credible at the granularite multicore and
.. process there is still a demand for a process pool.

.. - How to script Twisted versions of telnet, ping, dig, wget, mailx, etc?

.. - What is the best way to layout a Twisted development project, or to
..   write functional tests for the project?


.. Just remember that Python execute one after the other on one
.. core/processor, new system processes needs to be created to make use
.. of every core of the server.

.. threadpool, processpool




