
Setting and reading individual bit of a integer
===============================================

The decimal number 42 is written 101010 in base 2.

Say, you want to check wether the third bit of 42 is 1 or 0 (counting
from zero, this is bit number 2), you can use:

>>> bit_number = 2
>>> number = 42
>>> (number >>  bit_number) & 1
0

Ok, the third bit is zero, now you want to set that bit to one,
leaving the other ones untouched:

>>> number = number | (1 << bit_number)
>>> number
46

All good: 46 is written 101110 in base 2, the third bit has been
correctly set. Now to set it back to 0, it is 

>>> number = number & ~(1 << bit_number)
>>> number
42

Tricky isn't it? you can hide the bit operators behind functions:

>>> get_bit  = lambda num, n: (num >> n) & 1		  
>>> set_zero = lambda num, n: num & ~(1 << n)
>>> set_one  = lambda num, n: num |  (1 << n)              
>>> get_bit(42,2)
0
>>> set_one(42,2)
46
>>> set_zero(46,2)
43

Here are two functions to convert to and from base 2:

>>> def bin2dec(binary):
...     return int(str(binary),2)
...
>>> bin2dec(101010)
42
>>> def dec2bin(decimal):
...     digits = []
...     while decimal>0:
...         decimal, digit = decimal/2, decimal%2
...         digits.append(str(digit))
...     return ''.join(digits[::-1])
>>> dec2bin(42)
'101010'
>>> bin2dec(dec2bin(42))
42
>>> dec2bin(bin2dec(101010))
'101010'
>>> 


This article has more details: :doc:`bitfield`.
