
from sudoku import Sudoku, make_generators, stack_assumptions, data

class NativeSet( ...

    # - Ooh noo, we'll never get it out now...

    # - So certain are you. Always with you, it cannot be done
    #   Hear you nothing that I say?

    # - Master, moving stones around is one thing but this is totally
    #   different.

    # - NO! no different. Only different in your mind.
    #   You must unlearn what you have learn.

    # - All right, I'll give it a try...

    # - NO! Do, or do not, there is no try.

    
    [ ... ] 

if __name__=="__main__":

    sudoku = NativeSet(data)
    print "The problem: %s\n" % sudoku

    for _ in stack_assumptions(make_generators(sudoku)):
        print "A solution: %s\n" % sudoku

