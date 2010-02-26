=====================================
 Concurrent programming with Twisted
=====================================

.. todo::

   Proofread and make link to the official documentation,

   Clarify the API at the end of the doc, 

   Clarify the getpage_deferred concerning the storage of the
   intermediate results in the callback chain.


Problem introduction
====================

Concurrency is a key concept particularly useful for performance: take
a simple problem such as retrieving, for each element of a list of
blogs, the title of the web page of the first article of the
blog. This means::

    for each blog url retrieve the list of articles 
    	get the first article url in the list
        retrieve the web page of the first article	
        display the title

This is solved quite elegantly in Python. Here are the two functions
we will use:

.. function:: getpage( url ) -> html tree 

   Makes an http get request to the url passed as a parameter and
   returns the html content of the response as tree structure,

.. function:: xpath( pattern ) -> list of matching nodes

   Can operate on an html tree structure, selecting the list of html nodes
   matching the *xpath* pattern: can find urls or page title.

Here is the script:


.. include:: concurrent/getpage_sequential.py
   :literal:

This solution has a fondamental problem: when there are *n* element in
the blog list, there will be *2n* page downloaded, one after the
other, and this will take *2n * time to download one page*. When the
problem takes a time directly proportional to the number of input,
this is called an *O(n)* complexity and this rightfully rise the
eyebrow of any developer concerned with performance or
scalability. The solution presented at the end of the article is not
longer, has a network complexity of *O(1)* and is three times faster.

As each download is completely independent with regard to each other,
it is obvious that these downloads can be executed in parallel, or,
*concurrently*, which is the raison d'être of the Twisted Python
framework. Processes and threads are well known primitive for
programming concurrently but Twisted do without (not even behind your
back), to spares the developer from using locks, mutex, etc.

.. note:: A fast language 

   A frequently heard reaction at this point is "Python is a slow
   language to start with, a fast language is the answer to
   performance". Notwithstanding the many existing techniques to make
   compiled Python code run on multiple processors, it is not the
   point, in some case, a fast language like C does not help. For
   example, take the download of a install CD, there is an
   insignificant gain in performance in a download client written in C
   over an implementation in Python, because (1) both implementation
   are very likely to end up leaving the network and disk stuff to the
   kernel and most importantly because (2) this job is inherently
   bound by the network bandwidth, not by CPU computations, where C
   shines. Both in C and in Python, in the context of multiple
   downloads, there is a need to run the tasks concurrently.


Twisted in brief
================

One of the core ideas is that Twisted functions which make a network
call should not block the application while the response is not yet
available. :func:`urlopen`, for example, blocks as long as the web
page is not downloaded. Asynchronous functions register one or more
*callbacks* to handle the result and returns to the main loop as soon
as possible. The main loop (the :obj:`reactor`) keeps track of the
available results and runs the callbacks with the result as the first
argument. Because Twisted functions are *non-blocking*, and because
they use callbacks to process the result, the result is processed
*asynchronously* (such framework are also called *event-driven*).


Now, what does an asynchronous function returns if it does not return
the result? From the :obj:`reactor` point of view, there is a need for
an object which associates an asynchronous function to its
callbacks. From the point of view of the user of Twisted, he (or she!)
will want to process the result: the Twisted abstraction returned by
asynchronous functions is called a *Deferred* object, it is meant as a
**promise of a result** and have a method :func:`addCallback`. Now for
the user, a promise of a result is almost the same as a result except
for extra lines of code. It was to be expected, as the result is not
available yet, you need to be a bit more patient and type some more
code, obviously.

Deferreds, callbacks and the reactor are three central objects of the
Twisted framework, understanding how they relate is a good step toward
Twisted. Here is how a traditional ``doSomethingWithResult( getPage(
url ))`` is rewritten with this mental shift::

  deferred = getPage( url )

  def doSomethingWithResult( html ):
      ...
      return result

  deferred.addCallback( doSomethingWithResult )

Surprising huh? Every function which would block waiting before
processing a result is rewritten in two steps: 

#. the step which does the request and returns a deferred,

#. the step which process the request results and gets attached as a
   callback to the deferred.

The good news is that Python offers a really powerful keyword
:obj:`yield` to simplify the boilerplate of deferred and callback
manipulation. :obj:`yield` allows for returning from a function
half-way through and continuing later on at the point where the
function returned. For asynchronous functions decorated with
:func:`inlineCallbacks`, Twisted leverages :obj:`yield` : the reactor
passes the result when it is available and continues the function
where it exited.

Here is the strict minimum needed to use Twisted:

.. function:: getStuffAsynchronously( args ) -> Deferred

   Asynchronous in Twisted implies returning a Deferred which fires a
   result, and that a callback must have been attached to the Deferred
   to process the result. A callback can be either synchronous or
   asynchronous, it just needs to expect the result of the requesting
   functions as its first argument. A request must be asynchronous, it
   is the whole point of Twisted. 

   #. decorate this function with :func:`inlineCallbacks`,

   #. use a Twisted asynchronous primitive to do a request,

   #. :obj:`yield` this function call, resulting in giving back control to
      the reactor to run other callback, and eventually calling back
      :func:`getStuffAsynchronously` with the result,

   #. stores the return value of the yield (the result of the request)
      in a variable. The code manipulating the variable is the
      callback inline with the request in the same function, hence the
      name :func:`inlineCallbacks`,

   #. if you want to return something, use :func:`returnValue`. As an
      asynchronous function return a deferred, the decorator will make
      this function will return a deferred,

   Here is an example of an asynchronous function which respect these rules::

      from twisted.foobar import getSpam
      from twisted.internet.defer import inlineCallbacks

      @inlineCallbacks
      def stuff():
          result = yield getSpam( 'foobar://spam_server' )
	  returnValue( mangle( result ))

.. class:: reactor

   The import, ``from twisted.internet import reactor``, must be the
   first line of the script. The reactor is a module attribute of the
   :mod:`twisted.internet` module to make sure there is only one
   reactor per application. The reactor is typically mentionned three
   times in a twisted application (an import, a start and a stop),
   then you can forget about it.

   .. method:: start( Deferred ) -> never returns

      Starts the main loop. The :func:`reactor.start` must be the last
      line of your program: it blocks and never returns.

   .. method:: stop()

      Stops the main loop, effectively terminating the
      application. This function must be used in the callback of the
      last event of the application.


A short example
===============

The following simple example shows side by side two codes which
download, 30 times, the main page of *twistedmatrix.com* to extract
and print the title. The first snippet is sequential, and the second
is concurrent.

.. include:: concurrent/sequential.py
   :literal:
   
.. include:: concurrent/concurrent.py
   :literal:

Here is, step by step, how the concurrent code operates:

#. With the :func:`inlineCallbacks` decorator, :func:`title` implicitly
   returns a deferred, and the reactor will call the function again
   when the result of the http request is available.

#. :func:`getPage` is one of the many (many many actually)
   asynchronous function offered by Twisted, it returns a deferred,
   whose result is the html string. The low level steps composing
   :func:`getPage` are asynchronous as well: even the DNS request turning
   the ``twistedmatrix.com`` into an IP address will not block the
   application !

   Twisted offers asynchronous function for managing UDP and TCP
   socket, but also offers high level functions for making request in
   the following protocol Web, DNS, SMTP, POP, XMPP, SIP, AMQP, etc.

#. :obj:`yield` is the Python continuation keyword: the :func:`title`
   function returns at this point but will be restarted at this point
   at the next call of :func:`title`. This is crazy and perfect in the
   Twisted context. It is the :func:`reactor` which will eventually
   call back the :func:`title` function when the result of the
   deferred - when the response of the asynchronous request - is
   available.

   The result can be manipulated via the label at the left hand side
   of the :obj:`yield` assignement. In our example, the response is
   made available in the ``html`` placeholder.

#. This line is the callback code, it parses and prints a fragment of
   the result of the asynchronous request. At this point lies the gain
   in performance over ``urlopen( url )``: the application was not
   blocked until the return value was available,  :func:`getPage`
   returned as soon as the request was sent.

   ``[0].text`` means : from the first element of the list - which is
   an html node, here - take the text content.

#. :func:`DeferredList` takes a list of deferred as an input and
   returns a deferred whose callback is called after every element of
   the deferred list have been consumed. This function is sometimes
   called a *barrier* in other concurrency context. 

   In our example, the deferred list is composed of the deferreds of
   the 30 calls to the :func:`title` function, when they are done, it
   is the right time to stop the script by calling
   :func:`reactor.stop`.

Run the two script the measure the performance difference::

  time python sequential.py
  time python concurrent.py

This is a 4x performance increase:  not bad.

A concurrent solution
=====================

Here is a concurrent solution using Twisted to our original
problem, three times faster than the sequential approach :

.. include:: concurrent/getpage.py
   :literal:

This short article finishes here but poses as many questions as it
answers:

- Error handling is non existent in this script: manipulating
  deferreds explicitly, though more verbose, help creating clearer
  failure code path and help create more robust application and
  libraries.

  In our script, as well as when building network applications or
  libraries, the following problems may arise: no network, no dns, no
  route, no tcp server, page not found error, html title not
  found. How easy it is to handle them gracefully?

- Twisted use asynchronous functions to solve concurrency, how does it
  compare to thread or process (the :func:`threading` and
  :func:`multiprocessing` python module)? What does it mean for shared
  object and race condition? How does it compare with the *libdispatch*,
  erlang, haskell, stackless python, greenlet, coroutine or scala ways
  of doing concurrency?

- How do reactor and deferreds interoperates? By dissecting the
  getPage function, we should end understanding how it relates to the
  system call on which the reactor is based. The system call is
  :func:`select` by default, but can be :func:`epoll` on lLinux or
  :func:`kqueue` on Freebsd.

- How to script Twisted versions of telnet, ping, dig, wget, mailx, etc?

- What is the best way to layout a Twisted development project, or to
  write functional tests for the project?


