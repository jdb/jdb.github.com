

A sudoku solver
===============

Compared to a sudoku solved by a human, the algorithm presented below
operates in a different way. A human brain usually scans the sudoku
board in a seemingly random way and eventually *deduces* the right
number in the slots. On the other hand, the automated algorithm below
start from the top left slot, stack up assumptions, all the way to the
bottom right slot: take such candidate from the list of possible
number in such slot, and eventually backtrack the assumptions when a
dead end is met. The algorithm does not do deduction but remembers the
levels of assumptions, which is something hard to do for the human
brain.


The Sudoku class
----------------

.. autodoc, autoclass

The backtrack algorithm
-----------------------

It is interesting to note that the backtracking algorithm (the
algorithm whichis able to stack assumptions) really is independant
from the sudoku rules. The algorithm requires a vector of generators,
and blindly triggers them in a standard way, whether the generators
are solving a sudoku, the eight queens or the knight problem. When the
algorithm yields, the data structure: i.e. the sudoku board or
chessboard manipulated by the generators has cooked a solution.

It goes like this: generator i is called, if the generator yields,
then an assumption could be made, the generator i+1 is called, on and
on until the last generator of the vector is called. When a generator
raises an iteration exception, the board is in a dead end, and
the algorithm should backtrack: which means unstack the latest
assumption and call again the previous generator.

.. literalinclude:: sudoku.py
   :pyobject: conjoin


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

.. literalinclude:: sudoku.py
   :pyobject: Sudoku._make_assumption_generators


The bitfield optimization
-------------------------

The sudoku rules that ... : the data structure which first comes to
mind should be the set. Here is an optimization for created a set of
numbers from 1 to 9: uses bitfield.

.. literalinclude:: sudoku.py
   :lines: 55-67

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.set

.. literalinclude:: sudoku.py
   :pyobject: Sudoku.free


.. It is possible to do without if we keep a vector of
.. emptiness of the slots and if self.free takes the val to
.. suppress as an input, and if the conjoin keeps track of the
.. candidates
