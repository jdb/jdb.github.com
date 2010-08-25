
.. _deferred:

The *Deferred*
==============

Advantages and usage
--------------------

Event driven frameworks are usually provided with a set of classes with
predefined events. For example, to model an HTTP client, we expect to
have to derive a class and implement a method with a specific
name. Something like::

   class MyClient(HTTPClient): 
       gotHtml(html):
           "here my specific custom client code parsing the html"

Twisted indeed provides similar pattern, but Twisted also introduces a
powerful abstraction to represent an asynchronous function call: an
event and its pending action. The :class:`Deferred` is an object which
can holds a function. The code creating a request is expected to
return a result, which is unavailable at that point, so instead, it
returns a deferred, for which the requesting code expect the user to
be filled it with a function to process the results. The requester
object which is usually an instance of child class of
:class:`Protocol` also keeps a reference to this deferred and should
call the callback, as soon as it is notified by the reactor that the
data is received. The Twisted documentation calls it a "promise of a
result", here_ and there_.

.. _here: http://twistedmatrix.com/documents/current/core/howto/defer.html

.. _there: http://twistedmatrix.com/documents/current/core/howto/gendefer.html

Here are three great things about the Deferred:

- avoid the requirement to subclass anything to write a callback. No
  need for the object oriented programming to kick in, good old
  functions will do just fine. 

- the code making a request does not have to specify, know or care
  about the name of the callback function, which simplifies the
  writing of new requesting API. The requester calls the method
  :meth:`callback` on a deferred, when the data is
  received. It is up to the user to store the callable it seems
  adapted, in the Deferred returned by asynchronous function.

  It is up to the job of the protocol implementer to create a
  deferred, keep it as a attribute of the protocol instance and
  execute the callback which has been set by the protocol user, on
  this deferred on the desired event.

- the event represented by the deferred, and the pending action it
  fires can be manipulated: stored, listed, passed around, chained or
  cancelled. Take a list of events for example: it is straightforward to
  set a callback when the all events, or the first event have happened.

Synchronisation
---------------

Synchronizing calls means specifying the order and the event at which
actions will take place. In a sequential script, the execution schema
is implicit and so obvious that it is not even worth mentioning it:

- the network calls are executed along with the successive
  :func:`urlopen` function calls 

- and the program stops when the interpreter reaches the end of the
  script. 

So far so good, but now, in a Twisted program, things go differently,
there is no more gravity, and there is a fifth dimension... ok, I am
being a bit dramatic, the differences are more subtle. There are two
phases:

1. the first phase is the specification of the execution steps through
   the stacking of connections request to the reactor, and the
   definition of callbacks path. :func:`getPage` function call does not
   actually trigger a network HTTP request but creates a deferred
   which stacks a step in a callback chain,
 
2. the second phase is inside :meth:`reactor.run` , which triggers the
   execution of the callback chains and synchronizes the callbacks
   depending on when the response are available. 

Just comment out the call to run the reactor in the concurrent script,
and use wireshark to check that :func:`getPage` does not carry out the
network call by itself.

In our last problem, the concurrent script did not stop when the 30
calls completed successfully and require an explicit signal to
terminate. Let's synchronize the end of the script to the completion
of the 30 page download. In Twisted terms, this translates as *gather
the deferred returned from the requests in a list, define a callback
which will stop the reactor when all the deferreds in the list have
completed*.

The code should be modified to create a *DeferredList*
from the list of calls to the title function. *DeferredList* is a
Twisted primitive which returns a deferred which *fires* when all the
deferred have completed. An anonymous function which stop the
reactor is attached as a callback to the *DeferredList*::

  l = [ getPage(url).addCallback(getpage_callback) for i in range(30) ]
  d.DeferredList(l)
  d.addCallback(lambda n:reactor.stop())

Here, the expression ``lambda n:reactor.stop()`` returns a function
whose only action is to call the :meth:`reactor.stop`. This new
function is required because :meth:`reactor.stop` does not comply with
the callback specification: *a callback must have at least one
argument*. The anonymous function created with :keyword:`lambda` is
created to present the correct signature.

Now that the script terminates gracefully, let's clarify a common
misunderstanding: what does the reactor know about the deferreds that
the user manipulate? The answer is: nothing.  The interfaces that the
reactor knows are the few hardcoded functions from the UDP, TCP and
SSL transport protocols such as :meth:`connectionMade`,
:meth:`dataReceived`, and other methods. The reactor maintains a list
of transport instances stored as attributes of protocoles instances
which hold a Deferred created by the request methods and that the
:meth:`dataReceived` methods expects to fire the callback.

Now this concurrent version terminates, its performance can be
compared to a sequential script. It is much more efficient (on my
machine, it is 8 times more efficient). Note that for a threaded
version of the script

.. sourcecode:: sh

   ~$ time python trivial_sequential.py
   real	1m22.945s
   ~$ time python trivial_concurrent.py
   real	0m10.315s

The central mechanisms of Twisted were presented in the previous
sections, you are almost there ! The last section before the
conclusion shows a nicer way to present Twisted code. The two first
subsections are recaps on the standard :keyword:`yield` keyword and
Python decorators.
