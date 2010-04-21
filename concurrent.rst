

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

Twisted is a network framework: it maps protocol exchanges between
network nodes to an organized set of module, classes and functions
aimimg at building client and server applications efficiently. Twisted
classes wrap the UDP, TCP and SSL transport protocols and child
classes offer well tested, application protocol implementations such
as FTP, IMAP, XMPP, AMQP, DNS, etc.

Also, Twisted has methods for implementing generic features which are
decoupled from any specific protocols and which are often required by
substantial software projects. For instance, Twisted can map a tree of
ressources behind URLs, or can authentify users against flexible
backends, or can safely distribute objects on a network allowing
remote procedure calls. Twisted is written in Python and C and is fast
partly because, as we will see, the data is processed as soon as it is
available no matter how many connections are open.

This article introduces the problem of network concurrency, then
compare Twisted concurrency to the thread model. Follows an overview
of the main objects of the framework, namely the reactor which
supervise the simultaneous connections, the protocols and the
factories. Finally, to get a feel of how Twisted code shows, we will
compare two web client scripts: one sequential and one concurrent. The
concurrent one is improved along the presentation of new key points.

Problem introduction
====================

Concurrency is a key concept particularly useful for performance: take
a simple problem such as retrieving, for each blog of a list of
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
recursive locks. The solution presented at the end of the article does
not have more line of codes, does not take much longer for n download
than it takes for one download (a complexity of *O(1)*) and is
actually three times faster.
	
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
of the callback, other instructions can be processed. This is the
basic idea which makes asynchronous code faster than blocking code.


Twisted's concurrency model: a comparison with threads
======================================================

The concurrency model of Twisted is called *cooperative
multitasking* and is really different from a traditional process or
thread scheduler. There are two advantages over the thread model: it
is safer and faster on one core. 

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
function creates 100 threads to execute the *incr* function.

>>> def execute(f, *args):
...     threads=[]
...     for i in range(100):
...         threads.append(Thread(target=f, args=*args))
...
...     for t in threads: t.start()
...     for t in threads: t.join()

>>> execute(incr, (counter,))
>>> counter[0]>0
True

When the threads are run, the counter has been incremented but
curiously, but is different than 100000.

>>> counter[0] == 100000
False

The value of counter was 96733 last time this article was checked, which
means 3% of the counter increments went wrong. Here is what happened:

1. thread *x* is allocated a timeslice, and has the time to read the
   current value for the counter in its thread context before it gets
   paused,

2. then thread *y* gets executed, it has the time not only to read the
   current value in counter, but also to increment it to 5001 and
   store it back before getting paused,

3. now *x* gets executed again, increments the value *it had read and
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
>>> execute(safe_incr, counter, lock)

At this point, the counter is correct:

>>> counter[0]
100000

Twisted behaves differently, it handles many network connections
concurrently, but functions and method are not executed concurrently:
the callbacks triggered on the various events of a network connection
lifecycle will execute one after the other, no matter how many
connections exist. Since functions are not concurrent and always
execute until they return, there is no race conditions and no need for
the definition of critical section with mutexes, recursive locks, etc.

Twisted network concurrency model is called *cooperative multitasking*
in the sense that all functions are written striving to return as fast
as they can, especially after having emitted a network request. 

As the thread scheduler can be compared to a blind chainsaw, Twisted
functions are more like relay sprinters who choose when to pass the
baton. They decides to pass the baton to the coach who, at the time
when he gets the baton, decides which sprinters is the fittest to
run. If a sprinter keeps the baton indefinitely, there is no one to
interrupt him, and the other sprinters do not get to run: Twisted
concurrent model is safer as long as everyone behave as a gentlemen.

Faster: no overhead scheduling the threads
------------------------------------------

The previous threaded code using a shared ressource is less and less
efficient as the number of threads increases: the ressource becomes a
bottleneck. The following function times the execution in multiple
threads of the function given as a parameter:

>>> from timeit import Timer
>>> chrono = lambda f, *args: Timer(execute(f,*args)).timeit(number=1000)

Now, let's compare the execution time of the *incr* and *safe_incr*.

>>> no_lock = chrono( incr, counter)
>>> locked  = chrono( safe_incr, counter, lock)
>>>
>>> 10*no_lock < locked
True

In our example, the safe and locked code is at least 10 times less
efficient. The decision by the thread scheduler to run a particular
thread is based on an algorithm which has no clue of the existing
ressources. What happens here is that:

- when a thread is run, the thread context and stack is copied back
  which costs CPU cycles and data transfers, and it might actually be
  in vain, as the thread does not have the lock needed to execute. The
  threads get re-scheduled until it can own the ressource.
  
  The concept of *ressources* applies equally well to lock ownership,
  data received via sockets, or even user input in a graphical user
  interface. 

  As each Twisted function runs until its return point without
  interruption there is no concurrent access to the ressource, the
  ressource is always free for a function which runs.

- once the data is received by the kernel and made available to the
  application via a socket, the data might actually wait there sits
  there until the thread gets a chance to run again, As each thread
  takes care of its own socket, the received data waits to be
  processed until the thread is run again.

Several threads or processes in a pool are always needed to take
advantages of the multicore, Twisted


The Reactor and the Protocols
=============================

How does Twisted do away with the problems of threads in the context
of network connections?  Well, the Twisted runs a main loop called the
reactor, which runs the callback. **The reactor scheduling decisions
derives directly from the availability of the data received in the
supervised file descriptors**. The reactor is twofold:

- it is a wrapper around a kernel system call specialised in
  monitoring the reception of data in any of *many* (called
  a *transport*), each one representing a socket. Depending on the
  platform the system call is *select*, *epoll* or *kpoll*.

  In a nutshell, this system call returns after either a timeout or after
  the reception of data in one of the transport. The system
  call returns an array of bytes received, for each supervised file
  descriptor,

- the reactor maintains a list of Twisted :class:`Protocol` instances,
  each associated to a transport. When the system call returns, one
  after the other, for each data received transport, the reactor
  dutifully runs the :meth:`dataReceived` of the :obj:`protocol`
  associated to the :attr:`transport`.

The reactor is the runtime hub of the Twisted framework, it handles
the network connections and triggers the processing of the received
data as soon as they arrive.

With the sequential :meth:`urlopen` function :
      
1. the input url is parsed into a fully qualified domain name and a
   path, ex: *bit.ly* and */42* from *\http://bit.ly/42*,

2. the domaine name is resolved to an IP address, generally by
   asking a DNS server (the blocking network request may be avoided if
   the local resolver maintains the domaine name in a cache).

3. An HTTP get request for the URL is formatted, a socket toward
   the IP address of the web server is opened and the message is
   written in the socket. The urlopen waits for the reply from the
   server.
  
Here is the corresponding simplification of how Twisted operates
(additional abstractions such as the :class:`Factory` interface are
left out in this article):

1. :func:`getPage` is called, it parses the input URL, format the HTTP
   request string, and uses the :meth:`recors.connectTCP` method to
   stack a socket creation and monitoring request to the reactor
   represented by a host, port and :obj:`Protocol` instance, which in
   the case of :func:`getPage` derives from a Twisted HTTP GET class.

   If the host is a domain name and not an IP address,
   :meth:`connectTCP` tranparently inserts the DNS request and
   conditions the HTTP request to the availability of the IP address
   in a non blocking manner.

2. :func:`getPage` returns a :class:`Deferred`, a slot that the developer
   must fill with a function which will be executed when the HTTP
   reply arrives. More on the :class:`deferred` in the next section.

   This function should expect the html body of the response as the
   argument,

3. the reactor is run: for each :obj:`Protocol` object queued: the
   reactor opens a socket, copies the corresponding file descriptor in
   the :attr:`transport` attribute of the :obj:`Protocol` instance,
   and puts the :attr:`transport` under supervision.

   The reactor calls the :meth:`connectionMade` method of the
   :obj:`Protocol` instance which, in the case of :func:`getPage`
   writes the formatted HTTP request to the :attr:`transport` and
   returns to the reactor loop,

4. When the reactor detects the reply bytes in the :attr:`transport`,
   it calls the :meth:`dataReceived` method of the associated
   :class:`Protocol` which, in the case of :func:`getPage`, is written
   to parse in the bytes, the HTTP header from the HTML body. 

   Then, the :meth:`dataReceived` method for this protocol *fires* the
   developer callback with the html as the parameter.


Let's compare two complete scripts, one concurrent, one sequential of
a simple script which, 30 times, prints the html title of the
*http://twistedmatrix.com* web site.

.. include:: concurrent/trivial_sequential.py
   :literal:
   
Note that in the following version, the Twisted main loop started by
*reactor.run* never returns: a line of code below the start of the
reactor loop will never be executed. Ctrl-C can be used to terminate
the script.

.. include:: concurrent/trivial_deferred_dontstop.py
   :literal:

The attention should be drawn on the following snippets, the following
blocking code::

  html = urlopen( url ))
  print  parse( html ).xpath( ... )

becomes with Twisted primitives::

  d = getPage( url )                  
  def getpage_callback( html ):       
      parse( html ).xpath( ... )      

  d.addCallback( getpage_callback )   

It is indeed deconcerting to realize that in Twisted, the calling
function can not manipulate the result of the request. Here is a
shorter form, which might seem harder to read because the callback
code is always presented prior to the request code (more on this on
the section on *yield*)::

  def getpage_callback( html ):       
      parse( html ).xpath( ... )      

  getPage( url ).addCallback( getpage_callback )   


The *Deferred*
==============


Event driven/asynchronous are usually provided with a fixed set of
class with predefined events. To model an HTTP client, we expect to
have to derive a class and implement a method with a specific
name. Something like::

   class Client(HTTP): 
       gotHtml( html ):
           [ ... here my specific client code parsing the html ]

This happens like this in Twisted too, but there is a handy and
cleaner alternative on top which allows to avoid the requirement to
subclass anything. No need for the object oriented programming to
kick, functions will do thank you very much. 

More importantly, it allows the requester code not to specify, knows
or care about the name of the callback function. 

The code which executes the request, instead of blocking and returning
the result: returns immediately a deferred. For the user, it is meant
as a **promise of a result** and is a slot in which to put any
callable whose only condition is to accept one parameter: the result
of the request.

What is the relationship between the reactor and the deferreds? There
is None the interface that the reactor knows from the protocols are
the few hardcoded functions such as the connectionMade, the
dataReceived methods which correpond to the lifecycle of the UDP, TCP
and SSL connections. 

It is up to the job of the protocol implementer to create a deferred,
keep it as a attribute of the protocol instance and execute the
callback which has been set by the protocol user, on this deferred on
the desired event.

Deferred do not require a reactor, here is the equivalent of the
increment counter presented above with the threads:

>>> from twisted.internet.defer import Deferred
>>>
>>> counter = [0]
>>>
>>> def request():
...    return Deferred()
...
>>> def callback( counter ):
...    for i in range(1000):
...       counter[0]+=1
...
>>> def run( counter ):
...     deferreds = [ request().addCallback(callback) for i in range(100) ] 
...     # There is a hundred concurrent actions pending here
...     for d in deferreds:
...         d.callback( counter )
...
>>> run( counter)
>>> counter[0]
100000



In the sequential script, the execution is implicit and so obvious
that it is not even worth mentioning it: the network calls are
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


:obj:`yield` simplifies Twisted code...
=======================================

... once you understand what this crazy statement does

the :obj:`yield` Python statement
---------------------------------

Python offers a really powerful keyword which Twisted uses in a clever
way to simplify the boilerplate of deferred and callback
manipulation. :keyword:`yield` allows for returning from a function
half-way through and restarting later on at the point where the
function returned. The arguments of :keyword:`yield` are returned to
the caller of the function as if the :keyword:`return` statement was
used.

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

On call, a function using :keyword:`yield` returns a :term:`generator`
object i.e.  an object with a :meth:`next` method which, on successive
calls, runs, one after the other, the sections of code delimited by
the :keyword:`yield` statement. A generator object also raises a
:exc`:StopIteration` exception to signal when it has reached the end
of the last code section, and that it is no use calling it again.

:keyword:`Yield` is really powerful: for instance, here is a *lazy*
implementation of the fibonacci suite. 

>>> def fib(max=10):
...     a,b=1,0	
...     for i in range(max):
...          yield b
...          b,a = a+b,b

Lazy in the sense that it behaves like a huge list but the whole list
is never completely computed in one shot and never fully stored in
memory: the next element is computed **on demand**, when the
:meth:`next` method is called:

>>> gen=fib(2)
>>> gen.next(),gen.next()
(0, 1)
>>> gen.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

Generators are integrated with the ``for`` statement which
dutifully call the *next* method on them until they raise the
*StopIteration* exception:

>>> [n for n in fib(16)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

Now back to Twisted, do you see the similarity of concept between the
functions using :keyword:`yield` and the Twisted callback chains? *Both
specify section of codes to be called successively*. 

A limitation of :keyword:`yield` mechanism was lifted_ in Python2.5:
the next section of code can be called with input data if the new
*send* method is used instead of *next*.  :keyword:`yield` must be
used on the right hand side of a variable binding (the *equal* sign),
the sent data is bound in the variable. Calling :method:send* with
*None* as the argument is equivalent to calling the *next* method.

.. _lifted: http://docs.python.org/whatsnew/2.5.html#pep-342-new-generator-features


>>> def func():
...     data = yield 3+5
...     yield "The double of the data I just received", 2*data
... 
>>> t=func()
>>> t.next()
8
>>> t.send( 'Hello' )
('The double of the data I just received', 'HelloHello')

These changes turn generators from one-way producers of information
into both producers and consumers. Now that the generators can be
called with input data, the reactor to call them and give them the
data received as the input.

Decorators in Python
--------------------

A decorator is a function returning another function, usually applied
as a function transformation. For example, it is useful when you want
to debug a series of nested calls, such as ::

   parse( urlopen( url ))

There is a need to know what was returned by urlopen *without
modifying the nested call*. A solution is to insert the following
statement at the previous line::

   parse = log(parse)
   parse( urlopen( url ))

Where :meth:`log` is defined as::

   log(f):
      def foo( args ):
          print "here is the argument", args
	  return f( args )
      return foo

:meth:`log` prints the argument, then :meth:`log` call the decorated
function and return the result. In our example, the html string will
be printed before being passed on to the parse function. Here on a
custom function:

>>> def double(n):
...     return 2*n
... 
>>> double=log(toto)

Python allows some syntactic sugar, with the use of the *@* character,
for applying a decorator on a custom function to simplify the function
definition above:

>>> @log
... def double(n):
...     return 2*n
... 

Both definitions are equivalent:

>>> double(5)
Here is the argument: 5
10

Now, the yield statement and the decoration syntax are clearer, the
integration of yield with the Twisted reactor should not pose
difficulties.


The integration of yield with the Twisted main loop
---------------------------------------------------

The Twisted technical constraint to manipulate the result of a request
in a function different than the function making the request can be
inconvenient in some cases, the integration of yield with the
reactor alleviate this problem. Here are two versions of the *title*
function, the first one has already been presented before, it
repeated here for easy comparison::

   def title( url ):
       d = getPage( url )
   
       def cbGetPage( html_string ):
           print fromstring( html_string ).xpath( '/html/head/title' )[0].text
   
       d.addCallback( cbGetPage )    
       return d

The second one is a rewrite with the :obj:`yield` statement. Because
the :func:`title` is marked with the :func:`inlineCallbacks`
decorator, the reactor knows that the deferred returned by the
function needs to return a Deferred and adds the function itself as a
callback::

   @inlineCallbacks
   def title( url ):
        html = yield getPage( url )
        print fromstring( html ).xpath( '/html/head/title' )[0].text

As soon as the html page is available, the :obj:`reactor` will call the
:func:`send` method on the generator returned by :func:`title`, with
the requested html page as the argument.

This version is shorter, there is no need to create and name a nested
function, and to add a level of indentation to the callback code. The
code appear more like its sequential counterpart.

.. include:: concurrent/trivial_concurrent.py
   :literal:

Also, it is much more efficient than a sequential script (on my
machine, it is 8 times more efficient)::

   ~$ time python trivial_sequential.py
   real	1m22.945s
   ~$ time python trivial_concurrent.py
   real	0m10.315s


A concurrent solution to our original problem
=============================================

Here is a concurrent solution to our original problem, using Twisted,
three times faster than the sequential approach :

.. include:: concurrent/concurrent.py
   :literal:

The Twisted equivalent of *urlopen* is called *getPage* is
asynchronous and returns a deferred. The low level steps composing
:func:`getPage` are asynchronous as well: even the DNS request turning
the url argument into an IP address will not block the
application. 

This article finishes here and left many questions aside. Error
handling is non existent in the scripts: manipulating deferreds
explicitly, though more verbose, help creating clearer failure code
path and help create more robust application and libraries. In our
script, as well as when building network applications or libraries,
the following problems may arise: no network, no dns, no route, no tcp
server, page not found error, html title not found. How easy it is to
handle them gracefully?

.. This "paper_" has more information and pointers and the
.. subject of scalable IO strategies.

.. .. _paper: http://www.kegel.com/c10k.html


.. Twisted use asynchronous functions to solve concurrency, how does it
.. compare to thread or process (the :func:`threading` and
.. :func:`multiprocessing` python module)? What does it mean for shared
.. object and race condition? How does it compare with the *libdispatch*,
.. erlang, haskell, stackless python, greenlet, coroutine or scala ways
.. of doing concurrency?

.. Win95 way of doing things is not adapted for an OS were it is
.. difficult to control taht every code exectuing "behaves" and return
.. fast, it is much more credible at the granularite multicore and process there is still a demand for a process
.. pool.

.. - How to script Twisted versions of telnet, ping, dig, wget, mailx, etc?

.. - What is the best way to layout a Twisted development project, or to
..   write functional tests for the project?


.. Just remember that Python execute one after the other on one
.. core/processor, new system processes needs to be created to make use
.. of every core of the server.

.. threadpool, processpool

