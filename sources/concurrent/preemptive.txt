

Twisted's network concurrency model as compared with sockets and threads
========================================================================

Twisted's concurrency model of is called *cooperative multitasking*
and is really different from a traditional "one socket in one thread"
scheduler. Twisted has three advantages over the thread model: it is
safer, faster and faster. The advantages are illustrated around a
second simple problem: it is the traditional example of a global
counter updated by many threads.

Safer: no need to worry about locking shared ressources
-------------------------------------------------------

A thread scheduler decides the execution of a thread for a time slice,
then pauses the thread at an unpredictable point of a computation to
let another thread run. This is problematic, see the following code
(using threads) which is incorrect.

>>> counter = 0
>>> def incr(n=0):
...     global counter
...     for i in range(1000):
...         counter += 1 

:func:`incr` increments the counter one thousand times. Below, the
:func:`execute` function creates 100 threads to run the :func:`incr`
function.

>>> from threading import Thread
>>> def execute(f):
...     threads = [ Thread(target=f) for i in range(100)]
...     for t in threads: t.start()
...     for t in threads: t.join()
...
>>> execute(incr)
>>> counter > 0
True

When the threads are run, the counter has been incremented but
curiously, it is different from *100 threads \* 1000 increments =
100000*.

>>> counter == 100000
False

The value of counter was 96733 last time this article was checked, which
means that 3% of the counter increments went wrong. Here is what happened:

1. thread *x* reads the counter: say 5000, then gets paused

2. thread *y* reads the counter: 5000, increments, then writes the data : 5001

3. thread *x* continues on from where it paused : increments and writes
   the counter: 5001. Thread y incrementation was missed. 

From the Python virtual machine, via the libc, down to the processor
instructions, an increment is composed of a variable read and an
addition and is not atomic by default, there is nothing to prevent the
interruption of a thread in the middle of ``counter +=1``. To avoid
the effect of a big blind chainsaw messing with a subtle variable
increment, threads must use defensive techniques: they define
*critical sections* using locks and refuse to enter one until every
other thread has left the critical section. Here is a correct version
of the *incr* version using a lock dedicated to the *counter*
ressource.

>>> from threading import Lock
>>> lock = Lock()
>>> def safe_incr():
...     global counter,lock
...     for i in range(1000):
...         with lock:
...             counter+=1 
>>> counter = 0  
>>> execute(safe_incr)

At this point, the counter is correct:

>>> counter
100000

Note that the :class:`Lock` class abide by the :keyword:`with`
interface. :keyword:`with` will dutifully call :func:`Lock.__enter__`
when entering the indented block, and will call :func:`Lock.__exit__`,
when exiting the block, *even* if the block is exited on an
exception. These functions are implemented in :class:`Lock` to
respectively *acquire* and *release* the lock instance.

Shared ressources and critical sections must be controlled by code
which is difficult to get right. In Twisted, there are no threads, and
no thread scheduler, therefore there is only one function executing at
any given time, and it will run without interruption until it
returns. The function running has an exclusive access to all the
ressources, avoiding the danger of concurrent accesses, and misuses of
locks.

Twisted network concurrency model is called *cooperative multitasking*
in the sense that developers write functions with a goal that they
return, as they block each other. Especially, after having emitted a
network request, they return. As threads are interrupted by the
scheduler, function enclosed have the latitude to take as long the
developer see fit, without impacting the other processing, which can
tabke place.

As the thread scheduler can be compared to a blind chainsaw, Twisted
functions are more like relay sprinters who choose when to pass the
baton. They decide to pass the baton to the coach who, at the time
when he gets the baton, decides which sprinters is the fittest to
run. If a sprinter keeps the baton indefinitely, there is no one to
interrupt him, and the other sprinters do not get to run: Twisted
concurrent model is safer as long as everyone behave as a gentlemen.

Faster: no overhead due to scheduling the threads
-------------------------------------------------

The previous threaded code using a shared ressource is less and less
efficient as the number of threads increases: the ressource is a
bottleneck. :func:`chrono` times the multithreaded execution of the
function passed as a parameter:

>>> from timeit import Timer
>>> chrono = lambda f: Timer(lambda :execute(f)).timeit(number=10)

Now, let's compare the execution time of :func:`incr` and
:func:`safe_incr`. The safe, locked code is at least 10 times less
efficient than the unsafe.

>>> no_lock = chrono(incr)
>>> 10 * no_lock < chrono(safe_incr)
True

The decision by the OS thread scheduler to run a particular thread is
based on an algorithm which has no idea of the existing locks. When a
thread is run, the thread context and stack are copied back which
costs CPU cycles and data transfer, and it might actually be in vain,
as the thread may not have the lock that it needs to execute. Any such
threads will be get re-scheduled again and again until it can own the
ressource.

The scheduling overhead does not occur with Twisted. I assume the
reader is curious to see the Twisted can have many increment pending
on a global variable and the associated performance, it is be shown
as soon as the required Twisted concepts have been presented (Spoiler_:
Twisted is twice as fast as even the fast unsafe code).


   

Faster: data received does not sit in a buffer while a thread is paused
-----------------------------------------------------------------------

In an OS, once the data is received by the network module of a kernel
and made available to the application via a file descriptor, this data
might actually sit there until the thread which takes care of this
file descriptor gets a chance to run again. Event driven frameworks
can alleviate this problem: the next section introduces the
:attr:`reactor` and the :class:`Protocol`, which are a pre-requisites
for understanding how Twisted eliminates this delay.
e **xpath**  to find urls or page titles
  in a HTML document.

And here is the script which brings all this together (and includes a
design problem):

.. include:: sequential.py
   :literal:
   
When there are *n* element in the blog list, there will be *2n* page
downloaded, one after the other, and this will take *2n * time to
download a page*. When the time taken by an algorithm the algo
directly proportional to the number of inputs, this is called a linear
complexity and this will rightful
