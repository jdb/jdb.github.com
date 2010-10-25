

A sudoku solver
===============

This module can read the simple representation of a sudoku found in the
newspaper such as this one::

  problem = ('006007403'  
             '000906020'  
             '500304006'  
             '740000010'  
             '809000304'  
             '010000057'  
             '200603005'  
             '030208000'  
             '405700200') 
			  
Empty slots are represented by a zero. The module can display the
solution::

   9 2 6    5 1 7    4 8 3 
   3 7 4    9 8 6    5 2 1 
   5 8 1    3 2 4    7 9 6 

   7 4 3    8 6 5    9 1 2 
   8 5 9    1 7 2    3 6 4 
   6 1 2    4 3 9    8 5 7 

   2 9 8    6 4 3    1 7 5 
   1 3 7    2 5 8    6 4 9 
   4 6 5    7 9 1    2 3 8 



A human brain usually scans the sudoku board and eventually *deduces*
the right number in the slots. The algorithm presented below operates
in a different way. The algorithm below start from the top left slot,
stack up assumptions for which number in the current slot, all the way
to the bottom right slot. Eventually backtrack to the previous slot to
try a different assumption when no number can be set for the current
slot.

The algorithm does not do deductions but can remembers a full stack of
assumptions, which is something hard to do for the human brain.


The Sudoku class
----------------

.. automodule:: sudoku

The backtrack algorithm
-----------------------

It is interesting to note that the backtracking algorithm (the
algorithm whichis able to stack assumptions) really is independant
from the sudoku rules. The algorithm requires an argument with a
precise interface and blindly triggers them, whether the argument is
manipulating a sudoku, the eight queens or the knight problem. When
the algorithm yields, the sudoku board or chessboard manipulated by
the argument has cooked a solution.

It goes like this: generator i is called, if the generator yields,
then an assumption could be made, the generator i+1 is called, on and
on until the last generator of the vector is called. When a generator
raises an iteration exception, the board is in a dead end, and
the algorithm should backtrack: which means unstack the latest
assumption and call again the previous generator.

.. autofunction:: sudoku.stack_assumptions


The generators vector
---------------------

There are as many generator than there are slots on the sudoku board,
they are stored in a vector. Each generator is specific to a slot, it
actually *stores* the coordinates of the slot, like a closure. When
called for the first time, the generator computes the list of
candidate numbers for the slot, according to the current sudoku
board. The list of candidates depends on the state of the board at the
time the generator is called for the first time.

Only the function that provides the candidates for a slot implements
the sudoku rules: no number appears more than once on the same column,
on the same line and on the same square.

.. autofunction:: sudoku.make_assumption_generators


The bitfield optimization
-------------------------

The sudoku rules that ... : the data structure which first comes to
mind should be the set. Here is an optimization for created a set of
numbers from 1 to 9: uses bitfield.

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.__init__

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.candidates

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.set

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.free

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.attempt

