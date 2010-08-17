
class Binary(object):

    @staticmethod
    def d(binary):
        if hasattr(binary,'val'):
            return int( str(binary.val),2)
        else:
            return int( str(binary),2)

    @staticmethod
    def dec2bin(decimal):
        digits = []
        while decimal>0:
            decimal, digit = decimal/2, decimal%2
            digits.append(str(digit))
        return ''.join(digits[::-1]) if digits else '0'

    @staticmethod
    def b(decimal):
        return Binary(int(Binary.dec2bin(decimal)))

    @staticmethod
    def get(val, index):
        return val & 1 << index - 1

    @staticmethod
    def one(val, index):    # roy buchanan, jjkale
        return val | 1  << index - 1

    @staticmethod
    def zero(val, index):
        return val & (2**9 - 1) & (-1 << index - 1) - 1

    def __init__(self,binary):
        self.val = Binary.d(binary)

    def __repr__(self):
        return Binary.dec2bin(self.val)

    __add__    = lambda x,y: Binary.b(x.val + x.guess(y))
    __sub__    = lambda x,y: Binary.b(x.val - x.guess(y))
    __and__    = lambda x,y: Binary.b(x.val & x.guess(y))
    __xor__    = lambda x,y: Binary.b(x.val ^ x.guess(y))
    __or__     = lambda x,y: Binary.b(x.val | x.guess(y))
    __lshift__ = lambda x,y: Binary.b(x.val << y)
    __rshift__ = lambda x,y: Binary.b(x.val >> y)
                
    __pow__ = __divmod__ = __mod__ =  __floordiv__ = \
        __mul__ = lambda self, other: NotImplemented
