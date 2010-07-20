

Manipulating bitfields in Python (in most language actually)
============================================================

In most language, the smallest memory chunk, the smallest variable
size available is a *small integer* which is usually one byte, which
is on most architecture, eight bits. When you to store and retrieve
efficiently small items, it is perfectly possible ot use list of int
or dictionary of ints.

But there might be a day when there is a need to tackle a big
computation problem, or when one application will halves the battery
life of your mobile phone/set top box.

It might even be the case (like right now actually) that the system
decides to spin the vent of the laptop so fast that it wakes up
grandma having a nap narby. Well this is frustrating for a dual core
with one gigabyte of memory used to type text (sorry grandma, it is
not me it is the browser in the background with a silly javascript
advertisement).

Well, that day, one might gets interested at how our fathers, and the
fathers of our fathers* have sent lucky ones on the moon with
processors clocked at a few Hz and a few bytes on memory stored on
punch cards. And that day, it might come handy to know how to
manipulate bitfields.

The problem of the day is to implement a set of digits from 1 to 9. A
use case is for instance a sudoku resolver: before setting a number at
some position on the *chessboard*, we must check that that number is
not somewhere else in the line, or the column, etc. With Python
primitives, this is:

>>> line = set([1,2,3,4,5])
>>> 4 in line
True
>>> 9 in line
False
>>> line.add(9)
>>> 9 in line
True

The set is a cool primitive of Python but there is a lighter solution
adapted to our specific context: we can have a bit field of length
nine, when the nth bit is set to 1 then, n is in the set. Conversely,
when the nth bit is zero, n is absent from the set. At this point, the
set is implemented with just an int of nine bits, chances are that
this number will occupy two bytes. A Python set containing 9 digits is
much bigger. Also, the operation to set and retrieve the element of a
set are much more complicated than bitwise arithmetic.

How to **create** a bitfield of length nine?



How to **get** the nth bit?

Say we have the word *15* and we want to know if the third bit is set
to one or zero:

#. first put the desired bit at the righmost position by shifting the
   binary word w on the right as many times as the position of the
   desired bit

   >>> w = 15 >> 3

#. then, sets all bits except the rightmost one to zero and returns the
   result which is the desired bit and not more. 

   >>> w & 1

In our case, if it is 1, the number n is present in the set, else

   >>> def is_in(S,number):
   ...    return S >> number & 1

How to **set** the nth bit of the bitfield (set to one)?

Say we have the binary word 15 and we want to make sure the third bit
is set to 1.

#. first 


How to **unset** the nth bit of the bitfield (set it to zero)?

Say we have the binary word 15 and we want to make sure the third bit
is set to 0.

#. first create a binary whose nth bit is one

   >>> 1<<2

#. 'or' it with the negation of the input binary word

   >>> -15 | 1<<2

#. negate the result

   >>> -( -15 | 1<<2)



The problem with manipulating binary number in Python and most
language, is that the console thinks you are typing binary
numbers. When you type 111, the Python console understands it as 111
in decimal ()

How to manipulate bitfields in binary: there is no more decimal number
appearing

>>> 1<<3
1000

>>> def d(binary):
...     return int(str(binary),2)
>>> d(111)
7

>>> def b(decimal):
...     digits = []
...     while decimal>0:
...         decimal, digit = decimal/2, decimal%1
...         digits.append(digit)
...         return int(''.join(reversed(digits)))

>>> def b(7)
111



.. and our mothers and the mothers of our mothers (but they are fewer
   of them on the pictures)

.. except some crazy PDP find a link
