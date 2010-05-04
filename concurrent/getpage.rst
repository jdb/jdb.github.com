

This article introduces the problem of network concurrency, and
compare Twisted model to the sequential programming. This article
refers to other article along the lines, they present the concept of the
concepts mentioned here more in depth. They are listed here for memo:

.. toctree::
   :maxdepth: 1

   Comparison with threads and sockets <preemptive>
   Twisted core objects : the reactor and the Protocols <reactor>
   concurrent/smartpython
   An abstraction for pending results: the Deferred <deferred>

The problem of concurrency
==========================

Network concurrency is a key concept particularly for performance:
take a simple problem such as retrieving, for each blog of a list of
blogs, the title of the web page of the first article of the
blog. This first problem is actually the core job of a Web scraper or
crawler. This means::

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

.. include:: sequential.py
   :literal:
   
When there are *n* element in the blog list, there will be *2n* page
downloaded, one after the other, and this will take *2n * time to
download a page*. When the time taken by an algorithm the algo
directly proportional to the number of inputs, this is called a linear
complexity and this will rightfully raise the eyebrow of any developer
concerned with performance and scalability.

As each download is completely independent from each other, it is
obvious that these downloads should be executed in parallel, or,
*concurrently*, and this is the raison d'être of the Twisted Python
framework. :doc:`Processes and threads <preemptive>` are well-known
primitives for programming concurrently but Twisted does without (not
even behind your back), because it is not adapted for scalable network
programming. This frees the developer from using locks, recursive
locks, or mutexes. The solution presented at the end of the article
does not have more line of codes, does not take much longer for *n*
downloads than it takes for one download (a constant complexity) and
is actually three times faster.
	
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
in C and in Python, in the context of multiple downloads, prformance
depends on concurrent connections.

One of the core ideas is that Twisted functions which make a network
call should not block the application while the response is not yet
available. Functions are split in two functions, one which emits the
network system call and another function, the *callback*, which will
process the received bytes, and then return a processed result. In the
period of time between the return of the requesting functions and the
execution of the callback, the :doc:`reactor`, which is the
Twisted's event loop, can run other instructions. This is the basic
idea which makes asynchronous code faster than blocking code.

.. _yield:

A concurrent solution
=====================

Here is a concurrent solution to the problem detailed in the
introduction. It is three times faster than the sequential approach:

.. include:: concurrent_dontstop.py
   :literal:

The Twisted equivalent of :func:`urlopen` is called
:func:`getPage`. It is asynchronous and returns a deferred. The low
level steps composing :func:`getPage` are asynchronous as well: even
the DNS request turning the url argument into an IP address will not
block the application which is why such code is efficient. Learn about
how twisted uses :keyword:`yield` and the Python decorator_ on
:doc:`this page<smartpython>`

.. _decorator: http://wiki.python.org/moin/PythonDecorators

This article leaves many questions aside. For instance, error handling
is non existent in the scripts: manipulating deferreds explicitly,
though more verbose, help creating clearer failure code path and help
create more robust application and libraries. In our script, as well
as when building network applications or libraries, the following
problems may arise: no network, no dns, no route, no tcp server, page
not found error, HTML title not found. How easy it is to handle them
gracefully?


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
