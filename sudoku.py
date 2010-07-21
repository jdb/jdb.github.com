
import StringIO
import array


class Binary(object):
    
    @staticmethod
    def dec2bin(decimal):
        digits = []
        while decimal>0:
            decimal, digit = decimal/2, decimal%2
            digits.append(str(digit))
        return digits[::-1]

    @staticmethod
    def d(binary):
        if hasattr(binary,'val'):
            return int( str(binary.val),2)
        else:
            return int( str(binary),2)

    @staticmethod
    def b(decimal):
        digits = []
        while decimal>0:
            decimal, digit = decimal/2, decimal%2
            digits.append(str(digit))
        return Binary(int(''.join(digits[::-1])))

    def guess(self,n):
        return n.val if hasattr(n,'val') else int(str(n),2)

    def __init__(self,binary):
        self.val = Binary.d(binary)

    def __repr__(self):
        return ''.join(Binary.dec2bin(self.val))

    __add__    = lambda x,y: Binary.b(x.val + x.guess(y))
    __sub__    = lambda x,y: Binary.b(x.val - x.guess(y))
    __and__    = lambda x,y: Binary.b(x.val & x.guess(y))
    __xor__    = lambda x,y: Binary.b(x.val ^ x.guess(y))
    __or__     = lambda x,y: Binary.b(x.val | x.guess(y))
    __lshift__ = lambda x,y: Binary.b(x.val << y)
    __rshift__ = lambda x,y: Binary.b(x.val >> y)
                
    __pow__ = __divmod__ = __mod__ =  __floordiv__ = \
        __mul__ = lambda self, other: NotImplemented

# todo: decompose the sudoku in two steps: backtracking on previous
# candidates and backtracking on previous slots

# todo: implement the get, set_one and set_zero in the Binary class

class chessboard(object):

    newarray = lambda: array.array('i',[0] * 9)
    
    # lines, columns and square are bitfields of length 9
    lines       = newarray()
    columns     = newarray()
    squares     = newarray()
    
    # the termination condition
    empty_slots = 81
    # matrix is a 9x9 matrix of ints between 1 and 9
    matrix   = [newarray() for i in range(9)]

    def check(self, i, j, val):
        print "check : %s, %s, %s, %s" % (val,
            self.lines[i] & 1    << val - 1,
            self.columns[j] & 1  << val - 1,
            self.squares[(j/3)*3+i/3] & 1 << val - 1)

        return not self.lines[i] & 1    << val - 1    \
            and not self.columns[j] & 1 << val - 1    \
            and not self.squares[(j/3)*3+i/3] & 1 << val - 1

    def candidates(self, i,j):
        return filter(lambda val:self.check(i,j,val), range(1,10))

    def set(self,i,j,val):
        # print i, j, val, self.lines[i]
        self.matrix[i][j] = val
        self.lines[i]     = self.lines[i]   | 1  << val - 1
        self.columns[j]   = self.columns[j] | 1  << val - 1
        self.squares[(j/3)*3+i/3] = self.squares[(j/3)*3+i/3] | 1 << val - 1
        self.empty_slots -= 1

    def empty(self,i,j):
        val, self.matrix[i][j] = self.matrix[i][j], 0
        print self.lines[i], val
        self.lines[i]   = self.lines[i]   & (2**9 - 1) & (-1 << val - 1)-1
        self.columns[j] = self.columns[j] & (2**9 - 1) & (-1 << val - 1)-1
        self.squares[(j/3)*3+i/3] = \
            self.squares[(j/3)*3+i/3] & (2**9 - 1) & (-1 << val - 1)-1
        self.empty_slots += 1

    def solve():
        if self.empty_slots == 0:
            yield [c.matrix[i][:] for i in range(9)]
        else:
            for i in range(9):
                for j in range(9):
                    if self.matrix[i][j]==0:
                        for c in self.candidates(i,j):
                            self.set(i,j,c)
                            for winner in self.solve():
                                yield winner
                            self.empty(i,j)
                        raise

    def __str__(self):
        
        s = StringIO.StringIO()
        for i in range(9):
            if i % 3==0:
                s.write('\n')
            for j in range(9):
                if j % 3==0:
                    s.write('  ')
                s.write((' ' if self.matrix[i][j]==0 else str(self.matrix[i][j])) + ' ')

            s.write('\n')
        return s.getvalue()

def d(binary):
    return int(str(binary),2)

def b(decimal):
    digits = []
    while decimal>=1:
        decimal, digit = decimal/2, decimal%2
        digits.append(str(digit))
    return ' '.join(reversed(digits))

if __name__=="__main__":

    c = chessboard()

    start = (
        (2,0,1),
        (1,3,3),
        (0,4,5),
        # (0,5,2),
        # (2,5,7),
        # (0,6,8),
        # (1,6,1),
        # (1,7,2),
        # (2,7,6),
        # (0,8,4),
        # (3,0,8),
        # (4,0,5),
        # (4,1,6),
        # (5,2,3),
        # (4,3,8),
        # (5,3,5),
        # (3,5,6),
        # (4,5,1),
        # (3,6,3),
        # (4,7,4),
        # (4,8,9),
        # (5,8,7),
        # (8,0,6),
        # (6,1,8),
        # (7,1,5),
        # (7,2,4),
        # (8,2,2),
        # (6,3,6),
        # (8,3,7),
        # (8,4,1),
        # (7,5,8),
        # (6,8,2),
        )

    for i,j,val in start:
        c.set(i,j,val)

    print "  9 8 7 6 5 4 3 2 1"
    for i in range(9):
        print "%s %17s" % (i,b(c.squares[i]))

    # print c
    c.empty(1,3)
    # print c

    print "  9 8 7 6 5 4 3 2 1"
    for i in range(9):
        print "%s %17s" % (i,b(c.squares[i]))

