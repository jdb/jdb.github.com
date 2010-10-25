"""
A difficulty with manipulating binary numbers in the Python console,
is that the console does not know the input numbers are to be
interpreted in binary and the output numbers need to be formattedas
binary. The *bitfield* module helps in that once a number is
declared *Binary*, its representation in the console is the binary
representation, not the decimal. Additions and bitshifts uses binary
arithmetics too:

    >>> from bitfield import Binary
    >>> one = Binary(1)
    >>> one + 1
    10
    >>> [one << n for n in range(5)]
    [1, 10, 100, 1000, 10000]

    >>> a = Binary(1000)
    >>> a, a+1, a+1+1, a+10
    (1000, 1001, 1010, 1010)

The second operand must be a binary number or an instance of the
Binary class. It can not be a decimal number, decimal numbers must
first be converted to a binary number with *B()*:

    >>> a + 5
    Traceback (most recent call last):
    ValueError: invalid literal for int() with base 2: '5'
    >>> a + B(5)
    1101

    >>> b = Binary(10)
    >>> a+b, a-b
    (1010, 110)

Logical operators used with a Binary as first operand also return a
Binary:

    >>> a|b,  a&b,  a^b,  a|11,  a^11
    (1010, 0, 1010, 1011, 1011)

The methods *one()*, *zero()* and *get()* operates on an individual
bit of a Binary number, requiring the bit number (counted from zero) as
the argument:

    >>> a.get(3), a.get(2), a.get(1), a.get(0)
    (1, 0, 0, 0)

    >>> a, a.one(1)
    (1000, 1010)

    >>> a.zero(3)
    0

The methods of the Binary class often uses the *decimal2binary*, and
*binary2decimal* module functions. *B* is a shortcut for the
*decimal2binary* and is typically used by Binary when representing a
Binary number :

    >>> B(63), B(64)
    ('111111', '1000000')

*D* is a shortcut for *binary2decimal* and converts a binary number or
string to a decimal number.

    >>> D(111), D(101010)
    (7, 42)

"""

def decimal2binary(decimal):
    """Turns a decimal number into the string representation of a
    binary"""

    # two special cases to "get" right: 0 and negative number

    sign, decimal = ('-', -decimal) if decimal<0 else ('', decimal) 

    digits = []
    while decimal>0:
        decimal, digit = decimal/2, decimal%2
        digits.append(str(digit))

    return sign + ''.join(digits[::-1]) if digits else '0'

def binary2decimal(binary):
    "Turns a binary number into its decimal representation"
    return int(str(binary),2)

B, D = decimal2binary, binary2decimal


class Binary(object):
    """Helps the interactive manipulation of binary numbers by
    providing automated binary representation and methods operating on
    the individual bits of a binary number."""

    def __init__(self, binary, size=None, base=2):
        self.size=size
        if base==2:
            self.decimal = D(binary)
        elif base==10:
            self.decimal=binary
        else:
            raise ValueError

        if self.size and self.decimal >= 2<<self.size:
            raise Exception("Overflow: %s too big for size %s"
                            ) % (self.decimal, self.size)

    def __repr__(self):
        d = self.decimal & (2<<self.size)-1 if self.size else self.decimal
        return B(d)

    __add__    = lambda x,y: Binary(x.decimal + D(y), base=10)
    __sub__    = lambda x,y: Binary(x.decimal - D(y), base=10)
    __xor__    = lambda x,y: Binary(x.decimal ^ D(y), base=10)
    __and__    = lambda x,y: Binary(x.decimal & D(y), base=10)
    __or__     = lambda x,y: Binary(x.decimal | D(y), base=10)
    __neg__    = lambda x:   Binary(-x.decimal,       base=10)
    __invert__ = lambda x:   Binary(~x.decimal,       base=10)
    __lshift__ = lambda x,y: Binary(x.decimal << y,   base=10)
    __rshift__ = lambda x,y: Binary(x.decimal >> y,   base=10)
                
    __pow__ = __divmod__ = __mod__ =  __floordiv__ = \
        __mul__ = lambda self, other: NotImplemented

    def get(self,  index):
        return Binary(self.decimal >> index & 1, base=10)

    def one(self, index):    # roy buchanan, jjkale
        return Binary(self.decimal | 1  << index, base=10)

    def zero(self, index):
        return Binary( 
            self.decimal & ~(1 << index), 
            base=10)

one = Binary(1)

# limits: left to right conversion of the decimal to binary works ok
# a Binary must be on the left of any nested expression

# 1<< 3 is a decimal ... can't help it much in the expressions, need
# to use *one* (one = Binary(1))

# the size is not copied when creating a new Binary 


