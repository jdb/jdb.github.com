

Twisted's network concurrency model as compared with sockets and threads
========================================================================

Twisted's concurrency model is *cooperative* instead of being
*preemptive* as is the model with threads or processes. This has two
advantages over the thread model: it is safer and faster on one
processor. On the other hand, this model does not automatically takes
advantage of the multiple core or processors available on the host:
there is only one thread in one process, which is stuck on only one
processor.


Safer: no need to worry about locking shared ressources
-------------------------------------------------------

Let's take the example of a simple shared ressource : a
global counter updated by many threads.

>>> counter = 0
>>> def incr(n=0):
...     global counter
...     for i in range(1000):
...         counter += 1 

A thread scheduler decides the execution of a thread for a time slice,
then pauses the thread at an unpredictable point of a computation to
let another thread run. This is problematic, see the following code
(using threads) which is incorrect.

>>>
>>> from threading import Thread
>>> def execute(f):
...     threads = [ Thread(target=f) for i in range(100)]
...     for t in threads: t.start()
...     for t in threads: t.join()
...
>>> execute(incr)
>>> counter > 0
True

:func:`incr` increments the counter one thousand times. Below, the
:func:`execute` function creates 100 threads to run the :func:`incr`
function. When the threads are run, the counter has been incremented
but curiously, it is different from *100 threads \* 1000 increments =
100000*.

>>> counter == 100000
False

The value of counter was 96733 last time this article was checked, which
means that 3% of the counter increments went wrong. Here is what happened:

1. thread *x* reads the counter: say 5000, then gets paused *before* writing it back,

2. thread *y* reads the counter: 5000, increments, then writes the data : 5001

3. thread *x* continues on from where it paused : increments and writes
   the counter: 5001. Thread y incrementation was missed. 

From the Python virtual machine, via the libc, down to the processor
instructions, an increment is composed of a read, an addition and a
write; it is not atomic by default, there is nothing to prevent the
interruption of a thread in the middle of ``counter += 1``. To avoid
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

Shared ressources and critical sections must be controlled by code
which is difficult to get right. Even using *print* discretly makes
use of a shared ressource: 100 threads writing to stdout will steps on
each other foot and will corrupt the report. 

In Twisted, there are no threads, therefore there is only one function
executing at any given time, and it will run without interruption
until it returns. The function running has an exclusive access to all
the ressources, avoiding the danger of concurrent accesses, and
misuses of locks.

Twisted network concurrency model is called *cooperative multitasking*
in the sense that developers write functions with the constraint in
mind, that they need to return fast to let other processing occur: a
function which takes too long block every other. Especially after
having emitted a network request, Twisted's function immediately
return. Conversely, as threads are interrupted by the scheduler,
function running isolated in a thread or process have the latitude to
take as long the developer see fit, without impacting the other
threads or process.

As the thread scheduler can be compared to a blind chainsaw, Twisted
functions are more like relay sprinters who choose when to pass the
baton. They decide to pass the baton to the *coach* (see the reactor
:doc:`reactor<reactor>` page) who, at when he gets the baton,
decides which sprinters to run. If a sprinter keeps the baton
indefinitely, there is no one to interrupt him, and the other
sprinters do not get to run: Twisted concurrent model is safer as long
as everyone behave as a gentlemen.

Here are, for comparision, a hundred Twisted concurrent pending
increments on a global variable, using deferreds:

>>> from twisted.internet.defer import Deferred
>>>
>>> counter = 0  
>>> deferreds = [Deferred().addCallback(incr) for i in xrange(100)] 
>>>
>>> # There is a hundred concurrent pending actions at this point ...
>>>
>>> # ... fire NOW !
>>> for d in deferreds:
...     d.callback(None)
...
>>> counter
100000

Note that, though the pending action are concurrent, the callbacks are
called sequentially, one after the other. There is no socket, nor
blocking wait involved which makes this example ill-suited for a use
case for Twisted.



Faster: data received does not sit in a buffer while a thread is paused
-----------------------------------------------------------------------

Once a network packet is received by the module of a kernel and made
available to the application via a file descriptor, this data might
actually sit there until the thread which takes care of this file
descriptor gets a chance to run again. 

Event driven frameworks can alleviate this problem, the callback for a
request is launched as soon as the response is available. Concurrent
callbacks are not scheduled on a algorithm based on time sharing and
fairness: in Twisted, callbacks are executed because a response has
arrived and Twisted's main loop was idling, or the callback is queued
to be executed as soon as the current processing returns.

.. Need to back up this affirmation with some code, this is unconvincing and
   might be wrong

.. 
   does requesting the acquisition of a lock puts the process/thread
   in TASK_INTERRUPTIBLE mode (and the effective acquisition puts the
   process back in TASK_RUNNING)?

   does the blocking wait on a file descriptor puts the process/thread
   in TASK_INTERRUPTIBLE mode (and the reception of new data puts the
   process back in TASK_RUNNING)?


Faster: no overhead due to scheduling the threads
-------------------------------------------------

The previous threaded code using a shared ressource is less and less
efficient as the number of threads increases: the ressource is a
bottleneck and every thread must acquire it before proceeding. The
locked version of the variable increment is roughly 10% slower than
the version without locks.

The decision by the OS thread scheduler to run a particular thread is
based on an algorithm which has no knowledge of the existing
locks. When a thread is run, the thread context and stack are copied
back which costs CPU cycles and data transfer, and it might actually
be in vain, as the thread may not have the lock that it needs to
execute. Any such threads will be get re-scheduled again and again
until it can own the ressource.

The scheduling overhead does not occur with Twisted. I assume the
reader is curious to see the Twisted can have many increment pending
on a global variable and the associated performance, it is shown
as soon as the required Twisted concepts have been presented.

.. note::

   Well, the latest measurements shows the opposite, both threaded
   version, safe and unsafe are faster than the deferred version. The
   overhead must be negligible. The only real advantage is simplicity
   at this point. Glyph mostly emphasizes the deterministic execution
   as an advantage, which makes it easier to avoid race
   conditions. Must find a way to illustrate that... O_o
