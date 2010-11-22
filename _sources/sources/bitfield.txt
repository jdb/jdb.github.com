

Manipulating bitfields in Python (in most language actually)
============================================================

Why and when to use a bitfield
------------------------------

In most language, the smallest memory chunk that you can manipulate,
that is the smallest variable size available, is a small integer,
which is, on most architecture, eight bits. It is not possible to
manipulate directly the individual bits, for example, setting bit
number 4 to zero leaving the other bits untouched. There is seldom use
for such a manipulation.

There might be a day when there is a need to tackle a big computation
problem, or when the mobile application under development halves the
battery life of the user' s phone. It might even be the case
(like right now actually) that the system needs to spin the vent of
the laptop so fast that it wakes up my grand mother having a nap on the
couch nearby (true story, this is inconvenient).

That day, one might gets interested in how our fathers (and the
fathers of our fathers) have sent a happy few to the moon with
processors clocked at a few Hz and with a few bytes on memory stored
on punch cards. A technique they most certainly used is the
manipulation of bitfields for some data structures because they are
light and fast, especially much lighter in terms of memory and
processing than the Python dictionaries and lists.

They are not adapted for every use though: they are limited, trickier
to get right, and not super easy to debug. You might end putting twice
more time into the development that you originally expected. At this
point, you might even want to consider rewriting the module in C,
because by using choosing bitfields over dicts, sets and list, you are
already halfway there !

This introductory section is followed by the detailed explanation of
how to manipulate bitfields. The last section shows a real case use: a
heavyweight computation will swap the default Python dictionary for a
dictionary implemented with a bitfield for better performance.

Manipulating a bitfield
-----------------------

.. automodule:: bitfield

The *bitfield* module provides mostly eye candy, the two functions
that are pivotal to the manipulation of binary numbers are
*binary2decimal* and *decimal2binary* functions, whose source code is
presented below:

.. literalinclude:: bitfield.py
   :pyobject: decimal2binary

.. literalinclude:: bitfield.py
   :pyobject: binary2decimal

Now that it is possible to manipulate the bitfields with some ease,
the following subsections details the *get()*, *one()* and *zero()*
functions. The concepts explained here are similar in many programming
languages such as C/C++, Java, Ruby.

How to **get** the nth bit?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the number *1111* in binary, and we want to know if the third
bit is set to one or zero (counting from zero, this is bit number
**2**). Here is the method;:

#. first put the desired bit at the righmost position by shifting the
   binary word on the right as many times as the position of the
   desired bit:

   >>> from bitfield import Binary
   >>> b = Binary(1111)
   >>> b >> 2
   11

#. then, sets all bits except the rightmost one to zero and returns the
   result which is the desired bit and not more. 

   >>> (b >> 2) & 1
   1

   The third bit of the binary number *1111* is actually set
   to 1. Here is another example, where bit #2 is requested in number
   *10000*:

   >>> Binary(10000) >> 2 & 1
   0

..   
  A simple function to wrap the low level manipulation:
  
  >>> get = lambda decimal, position: decimal >> position & 1
  >>> get(1023, 2), get(1024, 2)
  (1, 0)


How to **set** the nth bit of the bitfield?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the binary number *10000* and let's make sure the third bit is
set to 1.

#. First create a number with all the bits equals to zero except for
   the third bit:

   >>> one = Binary(1)
   >>> one << 2
   100

#. The *OR* binary operator, available in Python with the *|*
   character, merges two bitfields: each bit of the resulting bitfield
   is *one* if either bit from one of the two operand is one, *zero* else:

   >>> 1|1, 1|0, 0|1, 0|0
   (1, 1, 1, 0)

   The number to transformed needs to be *ORed* with the number
   created in the previous step:

   >>> (one << 2) | 10000
   10100

..
  >>> set_bit = lambda num, position: (num | 1) << position

How to **unset** the nth bit?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say we have the number *10100* and we want to make sure the third bit is
set to 0. 

..  
  First, let's introduce the negative binary numbers. Positive
  numbers are implicitly prefixed with and infinite sequence of
  *0*. Negative numbers are implicitly prefixed with an infinite
  sequence of *1*. For instance::

    101 = ...00000101,  -10 =...1111111111111111110

  Note that the basic properties of negative numbers hold true:: 
  
     -10 + 10 = ...11110 + 10 = 1... 000000
  
  In the result, the most important bit, the leftmost one is infinitely
  remote and is assimilated to zero, think of an overflow: the counter
  cycles and turns back to zero.
  
  Now, the inversion operator inverts every bit of a number: a binary
  number made of the three bits 101 becomes 010, or the number made of
  six bits: 101010 becomes 010101. The Python numbers have an almost
  infinite size, so 101010 is actually ...000101010 and becomes
  ...111111010101
  
#. First create a binary whose third bit is one, all other are zero:

   >>> one<<2
   100
   
#. Invert the bits with the ~ operator: for every bits, a one becomes
   zero and a zero becomes a one: 100 becomes 011. 

   ..
     The implicit leading zeros will also be transformed into ones,
     this number becomes an long serie of ones except the third bit,
     set to zero.

   *ANDing* the input number and the number created at the previous
   step sets the third bit to zero:

   .. 
     also the superfluous leftmost *ones* will be lowered back to
     zeros with the implicit leading zeros of n.

   >>> ~(one<<2) & 10100
   10000

..
  >>> unset_bit = lambda (num, position): num & ~(1<<n)


Replacing the standard Python set object with a bitfield
--------------------------------------------------------

The example problem is to implement a set of digits from 1 to 9. This
is a data structure which has methods for adding, removing and checking
whether elements are contained in the data structure. Our use case is
a sudoku resolver: before setting a number at some position on the
sudoku *chessboard*, we must check that the number is not somewhere
else in the line, or the column, or in the square. Each column, line
or square can be represented by a set, with Python primitives, this
is:

>>> line = set([1,2,3,4,5])
>>> 4 in line
True
>>> 9 in line
False
>>> line.add(9)
>>> 9 in line
True

A bitfield of length nine is a lighter solution that the Python set
and is adapted to our specific context: when the nth bit is set to 1
then, n is in the set. Conversely, when the nth bit is zero, n is
absent from the set. At this point, the set can be implemented with
just one integer. A Python set object containing 9 digits would be
much bigger in terms of bytes. Also, the operation to set and retrieve
the element of a set are much more heavywight processor-wise than bit
arithmetic.

>>> class BitFieldSet:
... 
...     _num = 0
...     
...     _get  = lambda s, n: (s._num >> n) & 1		  
...     _zero = lambda s, n: s._num & ~(1 << n)
...     _one  = lambda s, n: s._num |  (1 << n)              
... 
...     def add(self, number):
...         self._num = self._one(number-1)
... 
...     def remove(self, number): 
...         self._num = self._zero(number-1)
... 
...     def __iter__(self):
...         for i in range(0,9):
... 	        if self._get(i):
...                 yield i+1
... 	
...     def __repr__(self): 
...         return "set(%s)" % [i for i in self]
...

Let's write a small function which can operate on any data structure
which has the methods *add* and *remove*. The function can not make a
difference between a regular Python set and a
*BitFieldSet*.

>>> def test(line):
...     for i in [1,2,3,4,5]:
...         line.add(i)
...     assert 4 in line
...     assert not 9 in line
...     line.add(9)
...     assert 9 in line
...
>>> test(set())
>>> test(BitFieldSet())
>>> from timeit import Timer
>>> print Timer( lambda : test(set())        ).timeit()     # doctest:+ELLIPSIS
2.52030396461
>>> print Timer( lambda : test(BitFieldSet())).timeit()     # doctest:+ELLIPSIS
28.7120981216

The last time the test function was executed, the BitFieldSet version
would take rougly ten times longer, showing that the data structure
unadapted for an optimized replacement of the Python set. Let's blame
it on a too naive benchmark for now. The article :doc:`sudoku` shows
the efficient use of bitfields for implementing a sudoku solver.
    
