
"""
The *sudoku* module offers a sudoku solver built around three objects: 

#. a Sudoku class with the methods for reading the start state of a
   sudoku board, for representing a board, for setting and freeing a
   slot of the board. 

   The most important functions which embed the rules of the sudoku
   games is the *candidates(col, row)* function: given the current
   state of the sudoku board, returns the list of possible values for
   the slot specified by the arguments.

#. a generic, independent backtrack algorithm function. The argument a
   vector of generator function, the algorithm instantiates the
   generator at the first position of the vector, and pulls the next()
   method:

   - either the method yields, in which case, the algorithm takes the
     second generator function and tries to pull the next() function,

   - or the method raises a StopIteration, in which case, the
     algorithm trigger next() on the previous slot

#.  

"""

import StringIO
import array
from contextlib import contextmanager

class Sudoku(object):

    def __init__(self, data):

        ### Initialisation of the searching algorithm 
        # the termination condition: the empty_slots will come down to zero
        self.empty_slots = 81

        ### Initialisation of the data structures
        newarray = lambda: array.array('i', [0] * 9)

        self.lines   = newarray()  # Lines, columns and
        self.columns = newarray()  # square are bitfields of length 9.
        self.squares = newarray()  # When bit 3 is set in lines[5], 3
                                   # is present in the fifth line.

        self.board  = [newarray() for i in range(9)]
        # a 9x9 matrix of of ints between 1 and 9. 

        k=0
        for i in range(9):
            for j in range(9):
                if int(data[k]) != 0:
                    self.set(i, j, int(data[k]))
                k+=1

    one  = lambda self, val, index: val | 1 << index - 1    
    zero = lambda self, val, index: val & (2**9 - 1) & (-1 << index - 1) - 1
    get  = lambda self, val, index: (val >>  index - 1) & 1
    # Bitfield manipulation...

    def candidates(self, col, row):
        """
        Returns the list of possible candidates for the slot specified
        by the argument col and row.

        The sudoku rules states that the candidates are the numbers
        which are not present neither in the column col, neither in
        the line row, neither in the square identified by col and row."""

        return filter(
            lambda val: all( not self.get(bf, val) for bf in (
                    self.lines[col], 
                    self.columns[row], 
                    self.squares[(row/3)*3+col/3])),
            range(1,10))

    # roy buchanan, jj kale
    def set(self, i, j, val):
        """
        Stores a new value in position i,j (no checks). Updates the
        lines, columns and squares arrays, decrements the number of
        empty slots.
        """
        self.board[i][j]   = val
        self.empty_slots  -= 1

        self.lines[i]             = self.one(self.lines[i],             val)
        self.columns[j]           = self.one(self.columns[j],           val)
        self.squares[(j/3)*3+i/3] = self.one(self.squares[(j/3)*3+i/3], val)

    def free(self, i, j, val=None):
        """
        Frees the i,j slot. Updates the presence arrays, increments the 
        number of empty slots.

        If val is None, then the value to be removed from the lines,
        columns and square is taken from the board.
        """
        val = val if val else self.board[i][j]
            
        self.board[i][j]    =  0
        self.empty_slots   +=  1

        self.lines[i]             = self.zero(self.lines[i],             val)
        self.columns[j]           = self.zero(self.columns[j],           val)
        self.squares[(j/3)*3+i/3] = self.zero(self.squares[(j/3)*3+i/3], val)

    @contextmanager
    def attempt(self, col, row, candidate):
        self.set(col, row, candidate)
        yield
        self.free(col, row, candidate)
        
    def __str__(self):
        s = StringIO.StringIO()
        for i in range(9):
            if i % 3==0:
                s.write('\n')
            for j in range(9):
                if j % 3==0:
                    s.write('   ')
                if self.board[i][j]==0:
                    s.write('  ')
                else:
                    s.write(str(self.board[i][j]) + ' ')
            s.write('\n')
        return s.getvalue()


def make_assumption_generators(sudoku):
    """Returns a vector of candidate generators for use with the backtrack 
    algorithm stack_assumption.

    The sudoku argument must provide two functions: *candidates(i,j)*,
    and *attempt(col, row, candidate)* and a member attribute called
    *board*, which is a 9x9 matrix.

    Once the argument provides the required interface, the vector can
    be created and the stack_assumption function can proceed."""
 
    assumptions_generators = []
    for i in range(9):
        for j in range(9):
            def assumption_generator(col=i,row=j):
                if sudoku.board[col][row] != 0:
                    yield
                else:
                    for candidate in sudoku.candidates(col, row):
                        with sudoku.attempt(col, row, candidate):
                            yield
            assumptions_generators.append(assumption_generator)
    return assumptions_generators


def stack_assumptions(assumption_generators, i=0):
    """
    Yields whenever every generator of the vector has yielded. 

    Each generator in the vector is responsible for a slot of the
    board. Whenever the generator is called, either it yields or it
    raises a StopIteration exception.

    When generator i has yielded, this means that a suitable candidate
    could be found and was set in the board's slot and that an
    assumption can be tried on the next slot, with generator i+1.

    When the generator raise a StopIteration, then a dead end was
    met. A wrong assumption must have been taken in the previous
    recursion: the algorithm backtracks and at the previous recursion,
    another assumption can be attempted.

    Whenever the number of recursion is equal to the number of slots
    on the board, this means an assumption could successfully be made
    for each slot: the board is full, a solution has been reached. At
    this point, stack_assumptions yield, so that the board's solution
    can be processed (printed, recorded, etc).
    """
    if i >= len(assumption_generators):
        yield 
    else:
        for _ in assumption_generators[i]():
            for _ in stack_assumptions(assumption_generators, i+1):
                yield


if __name__=="__main__":

    data=('006007403'
          '000906020'
          '500304006'
          '740000010'
          '809000304'
          '010000057'
          '200603005'
          '030208000'
          '405700200')

    data=('006007403'
          '000906020'
          '500304006'
          '740000010'
          '809000304'
          '010000057'
          '200603005'
          '030208000'
          '405700200')


    sudoku = Sudoku(data)
    gen_vector = make_assumption_generators(sudoku)
    print sudoku
    for _ in stack_assumptions(gen_vector):
        print sudoku

