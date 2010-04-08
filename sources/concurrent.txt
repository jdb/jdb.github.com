

.. TODO: que deviennent les deferreds creer dans la premiere phase?
.. sont t'ils lister sur le singleton reactor?

.. TODO: c'est quoi un decorateur, expliquer mieux le inlineCallback?
.. exemples, comme pour le yield 

.. TODO: returnValue example or impasse?

.. The rul is seen in the nested function, it is incorrect that the
.. yield help with the visibility.

.. mettre des liens vers la docs officielles des deferreds, des
.. reactor, sinon, c'est re-inventer la roue


=====================================
 Concurrent programming with Twisted
=====================================

Twisted is a network framework written in Python which make it
possible to assemble applications supporting client or server services
delivered via many protocols not only TCP, UDP and HTTP but also FTP,
IMAP, XMPP, AMQP, etc. Twisted also features an approach to
concurrency called cooperative multitasking, different from the
traditional thread and process model.

Twisted offers asynchronous function for managing UDP and TCP
socket, but also offers high level functions for making request in
the following protocol Web, DNS, SMTP, POP, XMPP, SIP, AMQP, etc.

This article covers the basics of concurrency in Twisted through the
comparison of two web client scripts, one sequential and one
concurrent. The concurrent one is improved along the presentation of
new key points.

Problem introduction
====================

Concurrency is a key concept particularly useful for performance: take
a simple problem such as retrieving, for each element of a list of
blogs, the title of the web page of the first article of the
blog, which is the typical job of a web crawler. This means::

    for each blog url retrieve the list of articles 
    	get the first article url in the list
        retrieve the web page of the first article	
        display the title

Let's provide a quick and naive solution to this problem. Here are
three handy functions :

- **urlopen**\ ( url ) returns an html string.  Makes an http get request
  to the url passed as a parameter and returns the body of the http
  response as a string,

- **parse**\ ( html string ) returns an html tree. Makes an http get
  request to the url passed as a parameter and returns the html
  content of the response as tree structure,

- htmltree.\ **xpath**\ ( pattern ) returns a list of nodes matching
  the pattern. 

  The ``[0]`` suffix selects the first element of the list. The text
  content of an html node is accessed via the member attribute
  ``.text``. In our context, we will use it to find urls or page title
  in an html document.

And here is the script which uses them, which features a design
problem:

.. include:: concurrent/sequential.py
   :literal:

When there are *n* element in the blog list, there will be *2n* page
downloaded, one after the other, and this will take *2n * time to
download one page*. When the problem takes a time directly
proportional to the number of input, this is called an *O(n)*
complexity and this rightfully rise the eyebrow of any developer
concerned with performance or scalability. 

As each download is completely independent with regard to each other,
it is obvious that these downloads can be executed in parallel, or,
*concurrently*, which is the raison d'être of the Twisted Python
framework. Processes and threads are well known primitive for
programming concurrently but Twisted do without (not even behind your
back), to spare the developer from using semaphore, mutex, recursive
locks etc. The solution presented at the end of the article is not
longer, has a network complexity of *O(1)* and is three times faster.
	
.. note:: 

   A frequently heard reaction at this point is "Python is a slow
   language to start with, **a fast language** is the answer to
   performance". Notwithstanding the many existing techniques to make
   Python code compile and run on multiple processors, it is not the
   point, in some case, the C compiler can not fix a bad design. For
   example, take the download of a install CD, there is an
   insignificant gain in performance in a download client written in C
   over an implementation in Python, because 1. both implementation
   are very likely to end up leaving the network and disk stuff to the
   kernel and most importantly because 2. this job is inherently
   bound by the network bandwidth, not by CPU computations, where C
   shines. Both in C and in Python, in the context of multiple
   downloads, there is a need to run the tasks concurrently.


Twisted deferred and callback objects
=====================================

One of the core ideas is that Twisted functions which make a network
call should not block the application while the response is not yet
available, so that other processing may be started in parallel. For
example, *urlopen*, from the *urllib2* in the Python standard library,
blocks as long as the web page is not completely downloaded and
prevents the rest of the application to proceed. Twisted functions, on
the other hand, are asynchronous: they return before the result is
available and a *callback* is registered to handle the result. The
Twisted main loop (called the :obj:`reactor`) keeps track of the
available results and runs the callbacks with the result as the first
argument. Because Twisted functions are *non-blocking*, and because
they use callbacks to process the result, the result is processed
*asynchronously* (such framework are also called *event-driven*).

The concurrency model of the reactor and deferred is called
**cooperative multitasking** and is really different from a
traditional process or thread scheduler. A scheduler decides the
execution of a thread for a time slice, and at some unknown point,
blindly cuts the thread in the middle of a computation to let another
thread run. To avoid the effect of a big chainsaw messing with, for
example, a delicate variable increment, threads must use defensive
techniques to define critical sections and refuse to enter one if they
are not alone in it.

The Twisted asynchronous functions are not interrupted, other chains
of execution might be executed only at the specified points of when a
function returns, which alleviate the need for locks. They cooperate
in the sense that all strive to return as fast as they can to let
others execute. This is more like relay sprinters who choose when to
pass the baton, and passing the baton to the coach who decides, at the
time when he gets the baton, which sprinters is the fittest to run. If
a sprinters keep the baton indefinitely, there is no one to interrupt
him, and the other sprinters do not get to run.

Now, what does an asynchronous function returns if it does not return
the result? For the :obj:`reactor`, there is a need for an object
which associates an asynchronous function to its callbacks. The
Twisted abstraction which provides this feature is called a *Deferred*
object, it is meant as a **promise of a result** and have a method
:func:`addCallback`. Now for the user, a promise of a result is almost
the same as a result except for extra lines of code. It was to be
expected: as the result is not available yet, you need to be a bit
more patient and type some more code in the mean time, obviously.

Deferreds, callbacks and the reactor are three central objects of the
Twisted framework, understanding how they relate is a big step toward
understanding Twisted. The Twisted equivalent of *urlopen* is called
*getPage* is asynchronous and returns a deferred. The low level steps
composing :func:`getPage` are asynchronous as well: even the DNS
request turning the turning the url argument into an IP address will
not block the application. Here is how to rewrite the following
blocking code::

  html = urlopen( url ))
  parse( html ).xpath( ... )

which becomes::

  d = getPage( url )                  # asynchronous network call
  def getpage_callback( html ):       # definition of the callback
      parse( html ).xpath( ... )      # processing of the result

  d.addCallback( getpage_callback )   # attaching the callback

Let's compare two complete versions, one concurrent, one sequential
of a simple script which, 30 times, prints the html title of the
*http://twistedmatrix.com* web site.

.. include:: concurrent/trivial_sequential.py
   :literal:
   
Note that in the following version, the Twisted main loop started by
*reactor.run* never returns: a line of code below the start of the
reactor loop will never be executed. Ctrl-C can be used to terminate
the script.

.. include:: concurrent/trivial_deferred_dontstop.py
   :literal:




Synchronization of chains of callbacks
======================================

In the previous sequential script, the execution is implicit and so
obvious that it is not even worth mentioning it: the network calls are
executed along with the successive *urlopen* function calls and the
program stops when the interpreter reaches the end of the script. Now,
in a Twisted program, things goes differently, there is no more
gravity, and there is a fifth dimension... ok, I am being a bit
dramatic, the difference are more subtle. There are two phases:

1. the first phase is the specification of the execution steps through
   the chaining of callbacks, the *getPage* function call does not
   trigger a network HTTP request but creates a deferred which stacks
   a step in a callback chain,
 
2. the second phase is inside the *reactor.run* call, which triggers the
   execution of the callback chains and synchronizes the callbacks
   depending on when the response are available. 

If you want to see for yourself that the *getPage* does not trigger a
*HTTP GET* when the function is called, just comment out the call to
run the reactor and use wireshark to check that nothing is sent on the
network.

Did you see how the concurrent script did not stop when the 30 calls
completed successfully? Let's fix that: the script should stop when
all requests completed. In Twisted, this translates as *gather the
deferred returned from the requests in a list, define a callback which
will stop the reactor when all the deferreds in the list have
completed*. The code should be modified to create a *DeferredList*
from the list of calls to the title function. *DeferredList* is a
Twisted primitive which returns a deferred which *fires* when all the
deferred have completed. This function is sometimes called a *barrier*
in other concurrency context. An anonymous function which stop the
reactor is attached as a callback to the *DeferredList*::

      DeferredList( 
             [ title( url ) for _ in range(30) ]
         ).addCallback( lambda _:reactor.stop() )

Now that the script terminates gracefully, let's introduce another
concept. In the concurrent version, the function :func:`title` grouped
the:func:`getPage` request and its processing through the use of a
nested function. This is a common idiom in Twisted programs which is
compatible with old versions of Python. The latest versions of Twisted
takes advantage of the enhancements to the :func:`yield` Python
keyword in version 2.5. Let's see how this keyword can simplify the
script.


``yield`` simplifies Twisted code...
====================================

... once you understand what this crazy statement does

the ``yield`` Python statement
------------------------------

Python offers a really powerful keyword which Twisted uses in a clever
way to simplify the boilerplate of deferred and callback
manipulation. :obj:`yield` allows for returning from a function
half-way through and restarting later on at the point where the
function returned. The arguments of ``yield`` are returned to the
caller of the function as if the ``return`` statement was used. 

These examples only include code from the core Python language, there
is no Twisted involved:

>>> def func_with_several_entry_points():
...     yield 'this string is the first return value'
...     val = 1+1
...     yield 'the latest portion of the function was executed',val
...

>>> f=func_with_several_entry_points()
>>> f                                      # doctest:+ELLIPSIS
<generator object func_with_several_entry_points at ...>
>>> f.next()
'this string is the first return value'
>>> f.next()
('the latest portion of the function was executed', 2)
>>> f.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

On call, a function using ``yield`` returns a *generator* object i.e.
an object with a *next* method which, on successive calls, runs one
after the other, one of the sections of code delimited by the
``yield`` statement. A generator object also raises a
``StopIteration`` exception to signal when it has reached the end of
the last code section, and that it is no use calling it again.

.. note:: 

   Yield is really powerful: for instance, it is a *lazy*
   implementation of the fibonacci suite. Lazy in the sense that it
   looks like a list but the whole list is never completely computed
   and never fully stored in memory, even for huge value of n: the
   element is computed **on demand**, when the *next* method is called

   >>> def fib(max=10):
   ...     a,b=1,0	
   ...     for i in range(max):
   ...          yield b
   ...          b,a = a+b,b

   Generators are integrated with the ``for`` statement which
   dutifully call the *next* method on them until they raise the
   *StopIteration* exception:

   >>> [ n for n in fib() ]
   [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

Now, do you see the similarity of concept between the functions using
``yield`` and the Twisted callback chains? Both specify section of
codes to be called successively. A limitation of ``yield`` mechanism
was lifted in Python2.5: the next section of code can be called with
input data if the new *send* method is used instead of *next*.
``yield`` must be used on the right hand side of an affectation, the
sent data is stored in the variable set via the affectation. Calling
*send* with *None* as the argument is equivalent to calling the *next*
method.

>>> def func():
...     data = yield 3+5
...     yield "The double of the data I just received", 2*data
... 
>>> t=func()
>>> t.next()
8
>>> t.send( 64 )
('The double of the data I just received', 128)

Now that the *generators* can be called with input data, it makes it
possible for them to model Twisted callback chains.

The integration of yield with the Twisted main loop
---------------------------------------------------

The Twisted technical constraint to manipulate the result of a request
in a function different than the function making the request can be
inconvenient in some cases, the integration of ``yield`` with the
reactor alleviate this problem. Here are two versions of the *title*
function, the first one has already been presented before, it
repeated here for easy comparison::

   def title( url ):
       d = getPage( url )
   
       def cbGetPage( html_string ):
           print fromstring( html_string ).xpath( '/html/head/title' )[0].text
   
       d.addCallback( cbGetPage )    
       return d

The second one is a rewrite with the ``yield`` statement. Because the
:func:`title` is marked with the :func:`inlineCallbacks` decorator,
the reactor knows that the deferred returned by the function must be
attached to itself as a callback::

   @inlineCallbacks
   def title( url ):
        html = yield getPage( url )
        print fromstring( html ).xpath( '/html/head/title' )[0].text

As soon as the html page is available, the :obj:`reactor` will call the
:func:`send` method on the generator returned by :func:`title`, with
the requested html page as the argument.

This version is shorter, there is no need to create and name a nested
function, and to add a level of indentation to the callback code. This
is nice, but more importantly, with ``yield``, the inline callback shares
the visibility of the calling function: **the developer can manipulate
the result directly in the calling function**. For example, in our
context, if the initial url needs to be printed, the inline callback
already sees the url while the traditional nested callback needs to
have its signature modified and must be called accordingly::

   def title( url ):
       d = getPage( url )
   
       def cbGetPage( html_string, url ):
           print fromstring( html_string ).xpath( '/html/head/title' )[0].text
   	   print url

       d.addCallback( cbGetPage, url )    
       return d

At this point, we have a script whose flexibility and readability is
improved:

.. include:: concurrent/trivial_concurrent.py
   :literal:

Also, it is much more efficient than a sequential script (on my
machine, it is 8 times more efficient)::

   ~$ time python trivial_sequential.py
   real	1m22.945s
   ~$ time python trivial_concurrent.py
   real	0m10.315s


The strict minimum needed to use Twisted
========================================

.. function:: getStuffAsynchronously( args ) -> stuff

   When a Twisted function, that you use in your own function, document
   what they *return* a result, they really mean that a callback
   attached to the deferred they return will be called with the result
   as the argument.

   Or that you must use ``yield`` between the call of the asynchronous
   function and the equal sign which stores the result in a variable.
   
   In which case, do not forget to decorate your own function wrapping
   the asynchronous call and the yield with
   :func:`inlineCallbacks`. Also, if you want to return something, use
   :func:`returnValue`. As an asynchronous function return a deferred,
   the decorator will make this function will return a deferred,

.. class:: reactor

   The import, ``from twisted.internet import reactor``, must be the
   first line of the script. The reactor is a module attribute of the
   :mod:`twisted.internet` module to make sure there is only one
   reactor per application. The reactor is typically mentionned three
   times in a twisted application (an import, a start and a stop).

   .. method:: run( Deferred ) -> never returns

      Starts the main loop. The :func:`reactor.start` must be the last
      line of your program: it blocks and never returns.

   .. method:: stop()

      Stops the main loop, effectively terminating the
      application. Must be used as a callback of the last event of the
      application.

A concurrent solution
=====================

Here is a concurrent solution to our original problem, using Twisted,
three times faster than the sequential approach :

.. include:: concurrent/concurrent.py
   :literal:

This short article finishes here but poses as many questions as it
answers. Error handling is non existent in this script: manipulating
deferreds explicitly, though more verbose, help creating clearer
failure code path and help create more robust application and
libraries.

In our script, as well as when building network applications or
libraries, the following problems may arise: no network, no dns, no
route, no tcp server, page not found error, html title not found. How
easy it is to handle them gracefully?

Twisted use asynchronous functions to solve concurrency, how does it
compare to thread or process (the :func:`threading` and
:func:`multiprocessing` python module)? What does it mean for shared
object and race condition? How does it compare with the *libdispatch*,
erlang, haskell, stackless python, greenlet, coroutine or scala ways
of doing concurrency?

.. - How do reactor and deferreds interoperates? By dissecting the
..   getPage function, we should end understanding how it relates to the
..   system call on which the reactor is based. The system call is
..   :func:`select` by default, but can be :func:`epoll` on lLinux or
..   :func:`kqueue` on Freebsd.

.. - How to script Twisted versions of telnet, ping, dig, wget, mailx, etc?

.. - What is the best way to layout a Twisted development project, or to
..   write functional tests for the project?


