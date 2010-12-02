
from sudoku import Sudoku, make_generators, stack_assumptions, data

class NativeSet(Sudoku):

    # - Ooh noo, we'll never get it out now...

    # - So certain are you. Always with you, it cannot be done
    #   Hear you nothing that I say?

    # - Master, moving stones around is one thing but this is totally
    #   different.

    # - NO! no different. Only different in your mind.
    #   You must unlearn what you have learn.

    # - All right, I'll give it a try...

    # - NO! Do, or do not, there is no try.

    _rows   =  [set() for _ in range(9)]
    _columns = [set() for _ in range(9)]
    _squares = [set() for _ in range(9)]

    def set(self, row, col, val):
        self.board[col][row] = val

        self._rows   [  row          ].add(val)
        self._columns[  col          ].add(val)
        self._squares[(row/3)*3+col/3].add(val)

    def free(self, row, col):
        val = self.board[col][row]
        self.board[col][row] = 0

        self._rows   [  row          ].remove(val)
        self._columns[  col          ].remove(val)
        self._squares[(row/3)*3+col/3].remove(val)

    def candidates(self, row, col):
        return filter(
            lambda e:all(
                [e not in s for s in (
                        self._rows[row],
                        self._columns[col],
                        self._squares[(row/3)*3+col/3])]),
            range(1,10))


if __name__=="__main__":

    sudoku = NativeSet(data)
    print "The problem: %s\n" % sudoku

    for _ in stack_assumptions(make_generators(sudoku)):
        print "A solution: %s\n" % sudoku

