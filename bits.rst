
Setting and reading individual bit of a integer
===============================================

The number 42 in decimal is written 101010 in base 2.

Say, you want to know the value of the third bit of 42 (counting from
zero, this is bit number 2) written in binary, you can use:

>>> bit_number = 3 - 1
>>> number = 42
>>> number & 1 << bit_number
0

Now you want to set that bit to one, leaving the other ones untouched:

>>> number = number | 1 << bit_number
>>> number
46

All good: 46 is written 101110 in base two, the third bit has been
changed. Now to set it back to 0, it is 

>>> number = 255 & number & (- 1 << bit_number) -1
>>> number
42

Tricky isn't it? 

Here are two function to convert to and from base 2 (I would be
interested to hear about others ways):

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

This article has more :doc:`bitfields`
