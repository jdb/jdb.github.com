
import StringIO
import array

class Sudoku(object):

    def __init__(self, data):

        ### Initialisation of the searching algorithm 
        # the termination condition: the empty_slots will come down to zero
        self.empty_slots = 81

        # creation of the vector of candidates required by "conjoin"
        self.candidates = []
        for i in range(9):
            for j in range(9):
                def candidate(col=i,row=j):
                    if self.matrix[col][row] != 0:
                        yield self.matrix[col][row]
                    else:
                        vals = filter(lambda val:self.check(col,row,val), 
                                      range(1,10))
                        for val in vals:
                            self.set(col,row,val)
                            yield val
                            self.empty(col,row)
                self.candidates.append(candidate)

        ### Initialisation of the data structures
        newarray = lambda: array.array('i',[0] * 9)

        self.lines   = newarray()  # Lines, columns and
        self.columns = newarray()  # square are bitfields of length 9
        self.squares = newarray()  # When bit 3 is set in lines[5], 3
                                   # is present in the fifth line.

        self.matrix  = [newarray() for i in range(9)]  # a 9x9 matrix of
                                                       # of ints between 
                                                       # 1 and 9
        k=0
        for i in range(9):
            for j in range(9):
                if int(data[k])!=0:
                    self.set(i, j, int(data[k]))
                k+=1

    # Bitfield manipulation:
    get  = lambda self, val, index: val & 1 << index - 1
    one  = lambda self, val, index: val | 1 << index - 1    
    zero = lambda self, val, index: val & (2**9 - 1) & (-1 << index - 1) - 1
    # roy buchanan, jj kale

    def check(self, i, j, val):
        """
        Checks if val in position i,j complies with the sudoku rules:
        the value is present neither on the line, on the column and on
        the square.
        """

        l = self.get( self.lines[i]            , val)
        c = self.get( self.columns[j]          , val)
        s = self.get( self.squares[(j/3)*3+i/3], val)

        return not l and not c and not s

    def set(self,i,j,val):
        """
        Stores a new value in position i,j (no checks). Updates the
        lines, columns and squares arrays, decrements the number of
        empty slots.
        """
        self.matrix[i][j]         = val
        self.empty_slots         -= 1

        self.lines[i]             = self.one(self.lines[i],             val)
        self.columns[j]           = self.one(self.columns[j],           val)
        self.squares[(j/3)*3+i/3] = self.one(self.squares[(j/3)*3+i/3], val)

    def empty(self,i,j):
        """
        Frees the i,j slot. Updates the presence arrays, increments the 
        number of empty slots.
        """
        val, self.matrix[i][j]    = self.matrix[i][j], 0
        self.empty_slots         += 1

        self.lines[i]             = self.zero(self.lines[i],             val)
        self.columns[j]           = self.zero(self.columns[j],           val)
        self.squares[(j/3)*3+i/3] = self.zero(self.squares[(j/3)*3+i/3], val)

    def solve(self):
        for solution in conjoin(self.candidates):
            yield solution

    def __str__(self):
        s = StringIO.StringIO()
        for i in range(9):
            if i % 3==0:
                s.write('\n')
            for j in range(9):
                if j % 3==0:
                    s.write('   ')
                if self.matrix[i][j]==0:
                    s.write('  ')
                else:
                    s.write(str(self.matrix[i][j]) + ' ')
            s.write('\n')
        return s.getvalue()

def conjoin(gs):

    values = [None] * len(gs)
    def gen(i, values=values):
        if i >= len(gs):
            yield values
        else:
            for values[i] in gs[i]():
                for x in gen(i+1):
                    yield x

    for x in gen(0):
        yield x

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

    print sudoku
    for solution in sudoku.solve():
        print sudoku
