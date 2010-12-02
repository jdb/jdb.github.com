
"""
The *sudoku* module offers three objects building a sudoku solver: 

- the *Sudoku* class modelling the sudoku board and sudoku rules,

- the *stack_assumptions* generic backtracking algorithm. The function
  takes a list of generator functions as argument,

- the *make_generators* function returning a list of
  generator functions suited for manipulating a sudoku and compatible
  with the bactracking algorithm.

"""

class Sudoku(object):
    """The *Sudoku* board class has the methods for reading the start
    state of a sudoku board, for representing a board. It also has the
    methods for setting and freeing a digit in a slot of the board,
    according to the rules of the sudoku game."""

    board  = [[0] * 9 for _ in range(9)]
    # a 9x9 matrix of of ints between 1 and 9, an empty position
    # is represented by a false value.

    def __init__(self, problem):    
        # Reading the problem
        i=0
        for row in range(9):
            for column in range(9):
                if int(problem[i]) != 0:
                    self.set(row, column, int(problem[i]))
                i+=1

    def __str__(self):
        # The matrix is transformed into a list of characters
        l = [str(self.board[col][row]) if self.board[col][row] else ' '
                    for row in range(9) for col in range(9)]

        l = ['\n   '+e if i%9 ==0 else e for (i,e) in enumerate(l)] # 1.
        l = ['  '+e    if i%3 ==0 else e for (i,e) in enumerate(l)] # 2.
        l = ['\n'+e    if i%27==0 else e for (i,e) in enumerate(l)] # 3.

        # 1.   New lines every 9 elements
        # 2,3. Squares are represented by extra spaces and another
        #      newline

        return ' '.join(l) 

    def candidates(self, row, col):
        """Returns the list of possible values for the slot specified by
        the arguments, according to the current state of the sudoku
        board and according to the rules of the sudoku game.
        
        The sudoku rules states that the candidates are the numbers
        which are not present neither in the column *col*, neither in
        the line *row*, neither in the square identified by *col* and
        *row*."""
        raise NotImplementedError

    def set(self, row, col, val):
        """Sets a new digit on the board in position *row,col*. This only
        updates the board *without* checking first if the rules of the
        sudo game are respected"""
        raise NotImplementedError

    def free(self, row, col):
        "Frees the slot in position row,col"
        raise NotImplementedError


class BitField(Sudoku):
    """Optimized implementation of the Sudoku interfaces. The
    "presence sets()" i.e. the efficient data structure which stores
    the information of which numbers are present in which
    rows/columns/squares are, each, represented with a single int
    instead of with a native Python dict"""

    # Private bitfield presence sets
    _rows   =  [0] * 9  # Lines, columns and
    _columns = [0] * 9  # square are bitfields of length 9.
    _squares = [0] * 9  # When bit 3 is set in lines[5], 3
                        # is present in the fifth line.

    _one  = lambda self, val, index: val |   1 << index - 1    
    _zero = lambda self, val, index: val & ~(1 << index - 1)
    _get  = lambda self, val, index: (val >>  index - 1) & 1
    # Bitfield manipulation

    def set(self, row, col, val):
        self.board[col][row] = val

        # Not only update the board but also the lines, columns and
        # squares arrays
        self._rows[row]    = self._one(self._rows[row],   val)
        self._columns[col] = self._one(self._columns[col], val)
        self._squares[(col/3)*3+row/3] = self._one(
            self._squares[(col/3)*3+row/3], val)

    def free(self, row, col):
        # The value to be removed from the lines, columns and square
        # presence set is found in the *board* member attribute
        val, self.board[col][row] = self.board[col][row], 0
            
        # Also update the line, column and square presence sets.
        self._rows[row]  = self._zero(self._rows[row],  val)
        self._columns[col] = self._zero(self._columns[col], val)
        self._squares[(col/3)*3+row/3] = self._zero(
            self._squares[(col/3)*3+row/3], val)

    def candidates(self, row, col):
        """Returns the list of possible values for the slot specified by
        the arguments, according to the current state of the sudoku
        board and according to the rules of the sudoku game.
        
        The sudoku rules states that the candidates are the numbers
        which are not present neither in the column *col*, neither in
        the line *row*, neither in the square identified by *col* and
        *row*."""

        return filter(
            lambda val: all( not self._get(bf, val) for bf in (
                    self._rows[row], 
                    self._columns[col], 
                    self._squares[(col/3)*3+row/3])),
            range(1,10))


def make_generators(sudoku):
    """Returns a list of candidate generators for use with the
    backtrack algorithm stack_assumptions.  The sudoku argument must
    provide two functions: *candidates(row,col)*, and *attempt(row, col,
    candidate)* and a member attribute called *board*, which is a 9x9
    matrix.

    There are as many generator functions than there are slots on the
    sudoku board, they are stored in a list. Each generator function
    is specific to a slot: it actually *stores* the coordinates of
    the slot, like a closure.

    When called for the first time, the generator computes the list of
    candidate numbers for the slot, according to the current sudoku
    board. The list of candidates depends on the state of the board at
    the time the generator is called for the first time."""

    generators = []
    for row in range(9):
        for col in range(9):
            def gen_func(row=row,col=col):
                if sudoku.board[col][row] != 0:
                    yield
                else:
                    for candidate in sudoku.candidates(row, col):
                        sudoku.set(row, col, candidate)
                        yield
                        sudoku.free(row, col)
            generators.append(gen_func)
    return generators


def stack_assumptions(generators, i=0):
    """Takes a list of generators. This list is assumed to manipulate
    a shared representation of the problem. When this algorithm
    yields, a solution has been found and can be printed.

    The algorithm works by calling the generator at the *nth* position
    of the list, and pulls the *next()* method on the iterator
    returned:

    #. either *next()* returns, in which case, the algorithm
       instantiates the generator from position **n+1** of the input
       list function and tries to pull its *next()* method,

    #. or the method raises a StopIteration, in which case, the
       algorithm trigger *next()* on the generator at position **n-1**,

    This algorithm yields whenever every generator of the list has
    yielded, at this point, every position of the board is filled with
    a digit according to the sudoku rules: a solution has been
    reached and the board can be printed.

    When a generator has yielded, this means that a suitable candidate
    could be found and was set in the board's slot and that an
    assumption can be tried on the next slot, with generator i+1.

    When a generator raises a StopIteration, then a dead-end was
    met. A wrong assumption must have been taken somewhere along the
    stack of the previous recursion: the algorithm backtracks at the
    previous recursion, another assumption can be attempted."""

    if i >= len(generators):
        yield 
    else:
        for _ in generators[i]():
            for _ in stack_assumptions(generators, i+1):
                yield

data=('006000090'
      '000501700'
      '200900300'
      '070030050'
      '020090060'
      '040080020'
      '001003004'
      '005207000'
      '030000800')

data=('006007403'
      '000906020'
      '500304006'
      '740000010'
      '809000304'
      '010000057'
      '200603005'
      '030208000'
      '405700200')


if __name__=="__main__":

    sudoku = BitField(data)
    print "The problem: %s\n" % sudoku

    for _ in stack_assumptions(make_generators(sudoku)):
       print "A solution: %s\n" % sudoku


# A run of this script shows the following result::
# 
#    ~$ python sudoku.py
#    The problem: 
#      
#           6       7   4   3   
#               9   6     2     
#       5       3   4       6 
#      
#       7 4               1     
#       8   9           3   4   
#         1               5 7 
#      
#       2       6   3       5   
#         3     2   8           
#       4   5   7       2    
#    
#    A solution: 
#      
#       9 2 6   5 1 7   4 8 3   
#       3 7 4   9 8 6   5 2 1   
#       5 8 1   3 2 4   7 9 6 
#      
#       7 4 3   8 6 5   9 1 2   
#       8 5 9   1 7 2   3 6 4   
#       6 1 2   4 3 9   8 5 7 
#      
#       2 9 8   6 4 3   1 7 5   
#       1 3 7   2 5 8   6 4 9   
#       4 6 5   7 9 1   2 3 8


