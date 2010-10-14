

Manipulating bitfields in Python (in most language actually)
============================================================

In most language, the smallest variable size available, that is the
smallest memory chunk that you can manipulate, is usually one byte.
That is *small integer*, which is on most architecture, eight bits. It
is not possible to manipulate directly the individual bits. For
example, setting bit number 4 to zero leaving the other bits
untouched.

There might be a day when there is a need to tackle a big computation
problem, or when the application being developed halves the battery
life of the users's mobile phone. It might even be the case (like
right now actually) that the system needs to spin the vent of the
laptop so fast that it wakes up grandma having a nap on the couch
nearby (for real). Well, this is frustrating, because as you see, I am
just typing an article!

That day, one might gets interested at how our fathers (and the
fathers of our fathers) have sent a happy few to the moon with
processors clocked at a few Hz and with a few bytes on memory stored
on punch cards. One might get interested in manipulating bitfields
because they are much lighter in terms of memory and processing than
the Python dictionaries and lists. On the other hand, they are less
flexible, trickier to get right, and not super easy to debug. You
might end putting twice more time into the development that you
originally expected. At this point, you might even want to consider
rewriting the module in C, because by using choosing bitfields over
dicts, sets and list, you are already halfway there !

The example problem is to implement a set of digits from 1 to 9. A use
case is for instance a sudoku resolver: before setting a number at
some position on the sudoku *chessboard*, we must check that the
number is not somewhere else in the line, or the column, etc. With
Python primitives, this is:

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

A difficulty with manipulating binary number in the Python console, is
that the console thinks you are typing decimal numbers. When you type
111, the Python console understands it as 111 in decimal (which is the
right thing most of the time), whereas 111 is actually 1101111 in
binary.

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




How to **create** a bitfield of length nine?

()


How to **get** the nth bit?

Say we have the word *15* and we want to know if the third bit is set
to one or zero:

#. first put the desired bit at the righmost position by shifting the
   binary word w on the right as many times as the position of the
   desired bit

   >>> 1 << 3

#. then, sets all bits except the rightmost one to zero and returns the
   result which is the desired bit and not more. 

   >>> 15 &1<<3

In our case, if it is 1, the number n is present in the set, else

   >>> def is_in(S,number):
   ...    return S >> number & 1

How to **set** the nth bit of the bitfield (set to one)?

Say we have the binary word 15 and we want to make sure the third bit
is set to 1.

#. first 


#. Here is a function which raises the bit number n of a number:

   >>> def setone(num, n):
   ...     return num | 1<<n

How to **unset** the nth bit of the bitfield (set it to zero)?

Say we have the binary word 15 and we want to make sure the third bit
is set to 0.

#. first create a binary whose nth bit is one

   >>> 1<<2

#. invert the bits: ones becomes zeros and zeros become ones: 100
   becomes 011. (Watch the precedence of the minus operator over the
   bitwise shift hence, the need of parenthesis)

   >>> - (1<<2) -1
   -5

#. There is a catch, you need to prefix the expression with the
   bitfield length and a bitwise *and* or Python won't know how many
   leading zeros you want to be turned into ones

   >>> 2**7-1 &- (1<<2) -1
   123       #   1111011

   >>> 2**8-1 &- (1<<2) -1
   251       #  11111011

   >>> 2**9-1 &- (1<<2) -1
   507       # 111111011


#. Now you can and this expression with hte number of you choice to
   set the nth bit to 0

   >>> 4 & 2**9-1 &- (1<<2) -1
   0

#. Here is a function which sets the bit number n (counting from zero,
   from the least significant bit (the rightest bit on an intel
   machine)) to zero in a bitfield of lenght 9:

   >>> def lower(num, n):
   ...     return num & (2**9 - 1) & - (1<<val) - 1



 
>>> class BitFieldSet:
... 
...     _num = 0
... 
...     get      = lambda s, n: (s.num >> n) & 1		  
...     set_one  = lambda s, n: 255 & s.num & ((-1 << n) - 1) 
...     set_zero = lambda s, n: s.num | (1 << n)              
... 
...     def add(self, number):
...         self._num = self.set_one(number-1)
... 
...     def remove(self, number):
...         self.num = self.set_zero(number-1)
... 
...     def __repr__(self):
...         return "set(%s)" % str([i for i in self])
... 	
...     def __iter__(self):
...         for i in range(1,10):
... 	        if self.get(i)
...     	    yield i

>>> line = BitFieldSet()
>>> for i in [1,2,3,4,5]:
...     line.add(i)
>>> 4 in line
True
>>> 9 in line
False
>>> line.add(9)
>>> 9 in line
True

It is possible to optimize the set for our context where the element
to put in the set are special enough to represent the set with a small
number.

def test(s):
>>> for i in [1,2,3,4,5]:
...     line.add(i)
>>> 4 in line
True
>>> 9 in line
False
>>> line.add(9)
>>> 9 in line
True
    
