
Counters in python
==================

Counters serve many purposes in software development. It is sometimes
handy to use a incrementor function which returns the new value every
time it is called, like calling ``count()`` instead of manipulating
directly a variable by using ``count += 1``. It has its uses
especially in Python where binding a variable does not return the
bound value, as in the C langage.

There is a peculiar example_ in the official Python documentation on
*lambda*. The *make_incrementor* function is misleadingly named since
nothing is incremented: the created callable merely returns the
addition of two integers.

.. _example: http://docs.python.org/tutorial/controlflow.html#lambda-forms

>>> def make_incrementor(start):
...     return lambda jump: jump + start
...
>>> f = make_incrementor(42)
>>> f(0)
42
>>> f(1)
43

An incrementor would commonly be called without argument and return
*43* the first time it was called and *44* the second time, etc. With
an incrementor, same cause lead to *different* effects.

In the example, *start* is enclosed in the created callable *f* but it
can not be modified. The following function tries to increment
*start*. But an *unbound exception* concerning *start* is raised when
calling the incrementor:

>>> def make_incrementor(start):
...     def f(jump=1):
...         start+=jump
...         return start
...     return f
...
>>> f = make_incrementor(42)
>>> f()
Traceback (most recent call last):
UnboundLocalError: local variable 'start' referenced before assignment

Ths variable can't be written in this scope, here are four correct
implementations below.

the object oriented way
-----------------------

The counter enclosed in the incrementor instance is an attribute
initialised by the constructor at the instanciation step. When the
instance is called, the attribute is incremented by one, and the value
returned:

>>> class make_incrementor(object):
...     def __init__(self, start):
...         self.count=start
... 
...     def __call__(self, jump=1):
...         self.count += jump
...         return self.count
...
>>> f = make_incrementor(42)
>>> f(), f(), f(10)
(43, 44, 54)

The object oriented version is a bit heavy but is the most explicit:
the three steps of class definition, object instanciation and object
manipulation are clearly separated.

with a function and a function attribute
----------------------------------------

A function can be used, it is a function which returns another
function, but in the end, it is the same as a class instantiating an
object. In Python, functions are also object and as such, can have
attributes too:

>>> def make_incrementor(start):
...     def f(jump=1):
...         f.count+=jump
...         return f.count
...     f.count=start
...     return f
...
>>> f = make_incrementor(42)
>>> f(), f(), f(10)
(43, 44, 54)

It is a bit less clear here, what is executed and when. The rule is
simple, the body of function is parsed but not evaluated until the
function is called, only the function is defined, and its default
value evaluated...

the trick of the argument default value
---------------------------------------

Here we make the closest attempt to build a closure, the counter is
initialised with the default value when the function is defined, and
there is no reference to the counter outside the function.

>>> def make_incrementor(start):
...     def f(jump=1, count=[start]):
...         count[0] += jump
...         return count[0]
...     return f
...
>>> f = make_incrementor(42)
>>> f(), f(), f(10)
(43, 44, 54)

*count* is a reference to a list whose first element is the real
counter integer. In Python, you can't manipulate reference to integer,
so the trick is to pass them enclosed in a list which are passed by
reference. If *count* is a pointer on an integer, in C, the pointer
and the value would be written ``count`` and ``*count``, in Python,
you get a similar result by defining *count* as list of one integer
element, and writing ``count`` and ``count[0]``.


using *yield*
-------------

The following function uses yield. Yielding, for a function, is the
act of voluntarily suspending itsef. Functions using yield returns a
generator which have the *next()* and *send()* methods.

>>> def make_incrementor(start, jump=1):
...     count = start
...     while True:
...         count += jump
...         jump = (yield count) or 1
...
>>> f = make_incrementor(42)
>>> f.next(), f.next(), f.send(10)
(43, 44, 54)

As generators are functions which can be resumed, they keep their
state: they can keep track of a counter. Which one do you prefer?
