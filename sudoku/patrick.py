
from sudoku import Sudoku, make_generators, stack_assumptions, data

class NativeSet( ...

    # May the force be with u
    # You can haz the sullushun!
    
    [ ... ] 


if __name__=="__main__":

    sudoku = NativeSet(data)
    print "The problem: %s\n" % sudoku

    for _ in stack_assumptions(make_generators(sudoku)):
        print "A solution: %s\n" % sudoku

