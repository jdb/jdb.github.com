
.. link to :doc:counters
.. link to queens and knight in the tests
.. (yield 3) is an expression
.. generators allows the superpowerful itertools

.. _yield:

The *yield* keyword simplifies Twisted code
===========================================

... once you understand what this crazy keyword does


:keyword:`yield` is a powerful Python keyword that Twisted uses to
simplify the boilerplate of deferred and callback manipulation.  Also,
the technical constraint, in Twisted, to manipulate the result of a
request in a function different than the function making the request
can be inconvenient: the integration of *yield* with the
:class:`reactor` alleviates this problem. Here are three versions of
the :func:`title` scraping function::

  def title(url):
      d = getPage(url)

      def getpage_callback(html):       
          print parse(html).xpath( ... )      

      d.addCallback(getpage_callback)   

Another *traditional* version, where the callback is defined before
the request. It is easier to read from the bottom::

  def getpage_callback( html )
      print parse(html).xpath( ... )      

  getPage(url).addCallback(getpage_callback)

The third one is a rewrite with the *yield* keyword, and requires
Python 2.5::

   @inlineCallbacks
   def title(url):
       print parse((yield getPage(url))).xpath( ... )

This version is shorter, there is no need to create and name a nested
function, and to add a level of indentation to the callback code. The
callback codes are in the same function that initiated the request,
hence the name of *inline callbacks*. Because :func:`title` is marked
with the :func:`inlineCallbacks` decorator, it will return a deferred,
the :obj:`reactor` will trigger the call to the :func:`send` method on
the generator, with the requested HTML page as the argument.

But let's proceed step by step: first the *yield* keyword, then the
decorator syntax.


the *yield* Python keyword
--------------------------

For a function, *yielding* means *volontarily suspending itself*. When
the function is called again, it is resumed where it was
suspended. The arguments of *yield* are returned to the caller of the
function as if the *return* keyword had been used. If you
already know *yield*, just skip to the next section.

The following examples only include code from the core Python
language, there is no Twistery involved:

>>> def func_with_several_entry_points():
...     yield 'this string is the first return value'
...     val = 1+1
...     yield 'the latest portion of the function was executed',val
...
>>> f=func_with_several_entry_points()
>>> f                                      # doctest:+ELLIPSIS
<generator object func_with_several_entry_points at ...>

On call, a function using *yield* returns a Python *generator*
object. *Generators* always have a *next()* method which, on
successive calls, runs the sections of code delimited by *yield*,
one after the other.

>>> f.next()
'this string is the first return value'
>>> f.next()
('the latest portion of the function was executed', 2)
>>> f.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

Generators object raises a :*StopIteration* exception to
signal when it has reached the end of the last code section, and that
it is no use calling it again.

*yield* is really powerful: for instance, here is a *lazy*
implementation of the fibonacci suite. 

>>> def fib(max=1000000):
...     a,b=1,0	
...     for i in range(max):
...          yield b
...          a,b = b,a+b

Lazy in the sense that it behaves like a huge list but the whole list
is never completely computed in one shot and never fully stored in
memory: the next element is computed **on demand**, when the
*next()* method is called:

>>> gen=fib(2)
>>> gen.next(), gen.next()
(0, 1)
>>> gen.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

Generators are integrated with the *for* keyword which
dutifully call the *next()* method on and on, until the
*for* keyword catches the *StopIteration* exception:

>>> [n for n in fib(16)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
>>> for n in fib(10):
...     print n,
... 
0 1 1 2 3 5 8 13 21 34

But we digress, now back to Twisted, do you see the similarity of
concept between the functions using *yield* and the Twisted
chains of callback? *Both specify section of codes to be called
successively*.

A limitation of *yield* mechanism was lifted_ in Python2.5, enabling
their use with the Twisted reactor: the next section of code of a
generator can be called with input data thanks the new *send()*
method instead of *next()*. *Yield*, enclosed in parenthesis, is
an expression:

.. _lifted: http://docs.python.org/whatsnew/2.5.html#pep-342-new-generator-features

>>> def func():
...     double_received = 2*(yield "Ok, I am ready to receive data")
...     yield "The double of the data I just received", double_received
... 
>>> t=func()
>>> t.next()
'Ok, I am ready to receive data'
>>> t.send('Hello')
('The double of the data I just received', 'HelloHello')

*These changes turn generators from one-way producers of information
into both producers and consumers*. The reactor can build generators
which send network requests the first time they are called, and can
*send* the generator the response data for processing, when it is
available.

Decorators in Python
--------------------

Twisted uses the *decorator syntax* to write callbacks in simpler manner,
this section is just a brief recap of what is a decorator_, skip to the
next section if already comfortable with Python decorators.

.. _decorator: http://wiki.python.org/moin/PythonDecorators

A decorator is a function returning another function, usually applied
as a function transformation. For example, it is useful when you want
to debug a series of nested calls, such as ::

   parse(urlopen(url))

If there is a need to know what was returned by urlopen *without
modifying the nested call*, a solution is to insert the following
statement at the previous line::

   parse = log(parse)
   parse(urlopen(url))

Where :meth:`log` is defined as:

>>> def log(f):
...     def foo(n):
...         print "Here is the argument:", n
... 	    return f(n)
...     return foo

:obj:`log` prints the argument, then :obj:`log` calls the decorated
function and returns the result. In our example, the HTML string will
be printed before being passed on to the parse function. Here on a
custom function:

>>> def double(n):
...     return 2*n
... 
>>> double=log(double)

Python allows some syntactic sugar, with the use of the *@* character,
for applying a decorator on a custom function to simplify the function
definition above (both definitions are equivalent):

>>> @log
... def double(n):
...     return 2*n
... 
>>> double(5)
Here is the argument: 5
10

Now that the *yield* keyword and the decorator syntax are clearer,
understanding the integration of yield with the Twisted reactor should
be easier to apprehend.
