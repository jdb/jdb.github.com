
Counter and more on yield
=========================

There is a peculiar example_ in the official Python documentation on
*lambda*. The make_incrementor function is misleadingly named since
nothing is incremented: the created callable merely returns the addition of
two integers. 

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
*43* the first time it was called and *44* the second time, etc.
      
With an incrementor, same cause lead to *different* effects: it
returns almost the same integer as the last time the incrementor was
called, except that the integer has been incremented by one. It
usually serves as a counter but it is a function instead of being a
variable: instead of using ``count+=1``, ``count()`` is used
instead. It has its uses in Python where binding a variable does not
return the bound value, as in the C langage.

In the example, *start* is enclosed in the created callable but it can
not be modified. The following function tries to increment
*start*. But an *unbound exception* concerning *start* is raised when
calling the incrementor:

>>> def make_incrementor(start):
...     def f(jump=1):
...         start+=jump
...         return jump
...     return f
...
>>> f = make_incrementor(42)
>>> f()
Traceback (most recent call last):
UnboundLocalError: local variable 'start' referenced before assignment

This is not the way to do it in Python, here are four correct
implementations of *make_incrementor*.

Class based
-----------

The counter enclosed in the instance is an attribute initialised by
the constructor at the instanciation step. When the instance is
called, the attribute is incremented by one, and the value returned:

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

The object oriented version is a bit heavy and the most explicit: the
three steps of class definition, object instanciation and object
manipulation are clearly separated.

With function and function attribute
------------------------------------

In Python, functions are object and as such, can have attributes too:


>>> def f(jump=1):
...     f.count+=jump
...     return f.count
...
>>> f.count=42
>>> f(), f(), f(10)
(43, 44, 54)


With function and the argument default value
--------------------------------------------

A simple function can be used. There are also two steps (function
definition and function call) instead of three (class definition,
instance creation and function call), the counter is initialised when
the function is defined. 

>>> def f(jump=1, count=[42]):
...     count[0]+=jump
...     return count[0]
... 
>>> f(), f(), f(10)
(43, 44, 54)

*count* is a reference to a list whose first element is the real
counter integer. In Python, you can't manipulate reference to integer,
so the trick is to pass them enclosed in a list which are passed by
reference. If *count* is a pointer on an integer, in C, the pointer
and the value would be written ``count`` and ``*count``, in Python,
you get a similar result by defining *count* as list of one integer
element, and writing ``count`` and ``count[0]``.

The version is the shortest of the four.



Using generator
---------------

The following function uses yield. Such functions returns a generator
which have the *next()* and *send()* methods.

>>> def make_incrementor(start):
...     count,jump = start, 1
...     while True:
...         count+=jump
...         jump=(yield count) or 1
...
>>> f = make_incrementor(42)
>>> f.next(), f.next(), f.send(10)
(43, 44, 54)

Yielding, for a function, is the act of voluntarily suspending
itsef. As generators are functions which can be resumed, they keep a
state: they can keep track of a counter.
