

.. TODO: que deviennent les deferreds creer dans la premiere phase?
.. sont t'ils lister sur le singleton reactor?

.. TODO: c'est quoi un decorateur, expliquer mieux le inlineCallback?
.. exemples, comme pour le yield 

.. TODO: returnValue example or impasse?

.. The rul is seen in the nested function, it is incorrect that the
.. yield help with the visibility.

.. mettre des liens vers la docs officielles des deferreds, des
.. reactor, sinon, c'est re-inventer la roue

=============================================
 Concurrent network programming with Twisted
=============================================

Twisted is a network framework, it maps protocol exchanges between
network nodes to an organized set of module, classes and functions
aimimg at building client and server applications efficiently. Twisted
classes wrap the UDP, TCP and SSL protocols and child classes offer
well tested, higher level protocol implementation such as FTP, IMAP,
XMPP, AMQP, DNS, etc.

Also, Twisted has methods for implementing generic features which are
decoupled from any specific protocols and which are often required by
substantial software projects. For instance, Twisted can map a tree of
ressources behind URLs, or can authentify users against flexible
backends, or can distribute objects on a network allowing remote
procedure calls. Twisted is written in Python and C and is fast
partly because, as we will see, the data is processed as soon as it is
available no matter how many connections are open.

This article introduces the problem of network concurrency, then
compare Twisted concurrency to the thread model. Follows an overview
of how Twisted handle simultaneous connections at the system
level. Finally, to get a feel of how Twisted code shows. We will
compare two web client scripts: one sequential and one concurrent. The
concurrent one is improved along the presentation of new key points.

Problem introduction
====================

Concurrency is a key concept particularly useful for performance: take
a simple problem such as retrieving, for each element of a list of
blogs, the title of the web page of the first article of the
blog, which is the typical core job of a web crawler. This means::

    for each blog url retrieve the list of articles 
    	get the first article url in the list
        retrieve the web page of the first article	
        display the title

Let's provide a quick and naive solution to this problem. Here are
three handy functions :

- **urlopen**\ ( url ) returns an html string. Makes an http get request
  to the url passed as a parameter and returns the body of the http
  response as a string,

- **parse**\ ( html string ) takes an html string as an input and
  returns a tree structure of html nodes,

- htmltree.\ **xpath**\ ( pattern ) returns a list of nodes matching
  the pattern. The text content of an html node is accessed via the
  member attribute ``.text``. In our context, we will use it to find
  urls or title of page in an html document.

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
it is obvious that these downloads should be executed in parallel, or,
*concurrently*, which is the raison d'être of the Twisted Python
framework. Processes and threads are well known primitive for
programming concurrently but Twisted do without (not even behind your
back), and spares the developer from using semaphores, mutexes or
recursive locks. The solution presented at the end of the article is
not longer in term of number of line of codes, it has a network
complexity of only *O(1)* and is actually three times faster.
	
.. note:: 

   A frequently heard reaction at this point is "Python is a slow
   language to start with, **a fast language** is the answer to
   performance". Notwithstanding the many existing techniques to make
   Python code compile and run on multiple processors, it is not the
   point. In many case, the C compiler can not fix a bad design. For
   example, take the download of an install CD, there is an
   insignificant gain in performance in a download client written in C
   over an implementation in Python, because 1. both implementation
   are very likely to end up leaving the network and disk stuff to the
   kernel and most importantly because 2. this job is inherently
   bound by the network bandwidth, not by CPU computations, where C
   shines. Both in C and in Python, in the context of multiple
   downloads, there is a need to run the tasks concurrently.

One of the core ideas is that Twisted functions which make a network
call should not block the application while the response is not yet
available: they are split in two: a function which emits the network
system calls and another function, the *callback* which will process
the received bytes, and will return a parsed result. In the period of
time between the return of the requesting functions and the execution
of the callback, other processing may occur in the mean time. This is
the basic idea which makes asynchronous code faster than blocking
code.


Twisted's concurrency model: a comparison with threads
======================================================

The concurrency model of Twisted is called **cooperative
multitasking** and is really different from a traditional process or
thread scheduler. There are two advantages over the thread model: it
is safer and faster.

Safer: no need to worry about locking shared ressources
-------------------------------------------------------

A scheduler decides the execution of a thread for a time slice, and at
some unknown point, pauses the thread in the middle of a computation
to let another thread run. This is problematic, see the following code
which is incorrect. A counter is defined and will be updated by many
threads. 

>>> from threading import Thread
>>> counter = [0]
>>> def incr(counter):
...    for i in range(1000):
...        counter[0]+=1 

The counter is contained in a Python list, to make it possible to pass
the counter by *reference*, not by *value*.  The *incr* function
increments the counter one thousand times. Below, the *execute*
function creates a hundred threads to execute the *incr* function.

>>> def execute(func, args):
...     threads=[]
...     for i in range(100):
...         threads.append(Thread(target=func, args=args))
...
...     for t in threads: t.start()
...     for t in threads: t.join()
>>> execute(incr, (counter,))
>>> counter[0]>0
True

The counter has been incremented but is different than 100 000.

>>> counter[0] == 100000
False

The value of counter was 96733 last time this article was checked, which
means 3% of the counter increments went wrong. Here is what happened:

1. thread *a* is allocated a timeslice, and has the time to read the
   current value for the counter in its thread context before it gets
   paused,

2. then thread *b* gets executed, it has the time not only to read the
   current value in counter, but also to increment it to 5001 and
   store it back before getting paused,

3. now *a* gets executed again, increments the value *it had read and
   also stores back 5001*. At this point, 5002 should have been
   stored. From the Python virtual machine, down to the processor
   instruction, a variable read and an addition are not atomic by
   default.

To avoid the effect of a big blind chainsaw messing with a subtle
variable increment, as seen in this example, threads must use
defensive techniques: they define critical sections and refuse to
enter one until every other thread have left the critical
section. Here is a correct version of the *incr* version using a lock
dedicated to the *counter* ressource.

>>> from threading import Lock
>>> lock = Lock()
>>> def safe_incr(counter, lock):
...     for i in range(1000):
...         with lock:
...             counter[0]+=1 

>>> counter = [0]  
>>> execute(safe_incr, (counter,lock))

At this point, the counter is correct:

>>> counter[0]
100000

Back to our comparisons, Twisted handles many network connections
concurrently, but functions and method are not executed concurrently:
the callbacks registered to execute on the various events of a network
connection lifecycle will execute one after the other, no matter how
many connections exist. Since functions are not concurrent and always
execute until they return, there is no race conditions and no need for
the definition of critical section with mutexes, recursive locks, etc.

Twisted network concurrency model is called cooperative multitasking
in the sense that all functions are written striving to return as fast
as they can, especially after having emitted a network request. As the
thread scheduler can be compared to a bling chainsaw, Twisted
functions are more like relay sprinters who choose when to pass the
baton. They decides to pass the baton to the coach who, at the time
when he gets the baton, decides which sprinters is the fittest to
run. If a sprinter keeps the baton indefinitely, there is no one to
interrupt him, and the other sprinters do not get to run. Twisted
concurrent model is safer as long as everyone behave as a gentlemen.


Faster: no overhead scheduling the threads
------------------------------------------

The previous threaded code using a shared ressource is less and less
efficient as the number of threads increase: the ressource becomes a
bottleneck. Each thread gets nominated by the scheduler whose decision
is based on an algorithm which has no clue of the existing locks and
ressources. When a thread is run, the thread context and stack is
copied back which takes times, but it may be in vain, as the thread
does not have the lock. The threads get re-scheduled until the only
threads which has it releases it.

Let's define a *chronometer* closure which returns the duration since
the last call:

>>> from datetime import datetime as d
>>> def chrono( start=[d.now()] ):
...     elapsed, start[0] = d.now()-start[0], d.now()
...     return elapsed

Now, let's compare the execution time of the *incr* and *safe_incr*.

>>> execute(incr,      (counter,    ));      no_lock = chrono()
>>>
>>> execute(safe_incr, (counter,lock));      locked = chrono()
>>>
>>> 10*no_lock < locked
True

Too many threads and not enough ressources impacts negatively the
performances. In our example, the safe code is at least 10 times less
efficient. As Twisted functions do not fight for the locks, they
execute faster. This `"paper"`_ has more information and pointers
and the subject of scalable IO strategies.

.. _`paper`:: http://www.kegel.com/c10k.html

Just remember that Python execute one after the other on one
core/processor, new system processes needs to be created to make use
of every core of the server.


The reactor handles concurrent network connections
==================================================

How does Twisted do away with the problems of threads in the context
of network connections? The thread scheduler decisions have no clue
the shared ressources and their lock ownership, and neither have clues
on the sockets managed in a thread. As each thread takes care of its
own socket, the received data waits to be processed until the thread
is run again, and the thread scheduler might run threads in vain
because no data is available in the socket for processing. Well, the
Twisted Reactor solves exactly this problem, **the scheduling decision
are based directly on the availability of the data received in the
socket**:

- on one hand, it is a wrapper around a kernel system call specialised
  in monitoring the reception of data in any of *many* file
  descriptors, each one representing a socket. Depending on the
  platform the system call is *select*, *epoll* or *kpoll*.

  Put simply, this system call returns after either a timeout or after
  the reception of a data in one of the file descriptor. The system
  call returns an array of bytes received, for each supervised file
  descriptor.

- on the other hand, the reactor execute one specific method of the
  object instance associated to the connection, so that the object
  instance reads the bytes in the file descriptor and triggers the
  processing of the data.

The reactor is a central piece of the Twisted framework, it handles
the network connections and triggers the processing of the received
data as soon as they arrive.

Let's details the steps in the download of a web page with *urlopen*,
in the sequential model and then let's compare it to the steps
involved with *getPage* which is the Twisted equivalent::

   urlopen( url ):
      parses the url to get the fully qualified name                    # 1 
      resolve the fqdn to a IP address:                                 # 2
            open a socket toward the system resolver
            format a DNS request for the url
            writes the request to the socket                            # 3
	    blocks until the DNS server replies with the IP address
      open a TCP socket to the correct IP address
      format an HTTP get request for the url
      writes the request to the socket
      blocks until the Web server replies with the html page            # 4
      
1. ex: 'bit.ly' from \http://bit.ly/42,

2. this is a network request which might take some time, depending on
   the network, the DNS server load, localization. This network
   request is generally avoided if the local resolver maintains a
   cache,

4. in a sequential script, everyone block here in a dangling suspense
   for the server reply,

5. bing, another blocking wait, another shot at the script
   productivity,
  
Twisted operates differently:

1. a Twisted script begins with the import of the reactor singleton
   object,

2. The getPage is called, it parses the input URL, format the HTTP
   request string, and stack a socket creation request to the reactor
   by presenting it a Twisted *protocol* object,

3. The getPage returns a slot that the developer must fill with a
   function which will be executed when the HTTP reply arrives. This
   function should expect the html body of the response as the
   argument,

4. Only then, the reactor is run: for each *protocol* object queued,
   the reactor opens a socket, associates the socket to the protocol
   instance, and puts the socket under supervision, and finally calls
   the *connectionMade* method of the protocol. 

   The *protocol object* derives from the HTTP GET client class whose
   *connectionMade* method writes the HTTP request to the socket and
   returns.

5. When the reactor detects the reply bytes in a socket, it calls the
   *dataReceived* method of the protocol associated to the socket which
   parses in the bytes, the HTTP header from the HTML body. The method calls
   the developer callback with the html as the parameter.



The *Deferred*
--------------

Event driven/asynchronous are usually provided with a fixed set of
class with predefined events. To model an HTTP client, we expect to
have to derive a class and implement a method with a specific
name. Something like::

   class Client(HTTP): 
       gotHtml( html ):
           [ ... here my specific client code parsing the html ]

This happens like this in Twisted too, but there is a handy and
cleaner alternative on top which allows to avoid the requirement to
subclass anything. More importantly, it allows the requester not to
specify, knows or care the name of the callback function. The code
which executes the request, instead of blocking and returning the
result: returns immediately a deferred. For the user, it is meant as a
**promise of a result** and is a slot in which to put any callable
whose only condition is to accept one parameter: the result of the
request. 

What is the relationship between the reactor and the deferreds? There
is None, the interface that the reactor knows from the protocols is
just a few hardcoded functions such as the connectionMade, the
dataReceived methods which correpond to the lifecycle of the UDP, TCP
and SSL connections. It is up to the protocol implementer to create a
deferred, keep it as a attribute of the protocol instance and execute
the callback which has been set by the protocol user, on this deferred
on the desired event.

Here is an example of a use of the deferred without a reactor::

   from twisted.internet.defer import Deferred
   
   counter = [0]
   
   def request():
       return Deferred()
   
   def callback( counter ):
       for i in range(1000):
           counter[0]+=1
   
   deferreds = [ request().addCallback(callback) for i in range(100) ] 
   
   # There is a hundred concurrent actions pending, I can 
   # execute the callback exactly whenever I want ...

   # Now !    
   for d in deferreds:
       d.callback( counter )
   
   print counter[0]
   # returns 100 000

The Twisted equivalent of *urlopen* is called *getPage* is
asynchronous and returns a deferred. The low level steps composing
:func:`getPage` are asynchronous as well: even the DNS request turning
the url argument into an IP address will not block the
application. Here is how to rewrite the following blocking code::

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

This article finishes here and left many questions aside. Error
handling is non existent in the scripts: manipulating deferreds
explicitly, though more verbose, help creating clearer failure code
path and help create more robust application and libraries.

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


.. - How to script Twisted versions of telnet, ping, dig, wget, mailx, etc?

.. - What is the best way to layout a Twisted development project, or to
..   write functional tests for the project?


