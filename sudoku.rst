

A sudoku solver
===============

.. todo::

   A real intro and conclusion, differents parts, and partial transitions

.. todo::

   Decide on what to explain: the code on one side, or the
   collaboration and interfaces of three objects

.. todo::

   extend the article with another article on the interfaces

.. Intro
.. Ever since the ancient gods, humans beings have 
.. Problematique
.. Scope
.. Plan

.. Conclusion
   
 

.. todo::

   - Mention the bitfield optimizations,
   
   - Make a variant of a sudoku class with just Python sets

   - Make a variant in C 

   - Profile the variants

 


This module can read the simple representation of a sudoku found in the
newspaper and display the solution. Ex::

  ~$ python sudoku.py
  The problem: 
  
         6        7    4   3 
              9   6      2   
     5        3   4        6 
  
     7 4                 1   
     8   9             3   4 
       1                 5 7 
  
     2        6   3        5 
       3      2   8          
     4   5    7        2     
  
  A solution: 
  
     9 2 6    5 1 7    4 8 3 
     3 7 4    9 8 6    5 2 1 
     5 8 1    3 2 4    7 9 6 
  
     7 4 3    8 6 5    9 1 2 
     8 5 9    1 7 2    3 6 4 
     6 1 2    4 3 9    8 5 7 
  
     2 9 8    6 4 3    1 7 5 
     1 3 7    2 5 8    6 4 9 
     4 6 5    7 9 1    2 3 8 
  

As a human brain usually scans the sudoku board and eventually
**deduces** the right digit in the slots, the algorithm presented
below operates in a different way. The algorithm below starts from the
top left slot and **stacks up assumptions** for which digit is put in
a slot, for each slot all the way to the bottom right slot. Eventually
backtrack to a previous slot to try a different assumption when no
number can be set for the current slot. On the contrary to the human
brain, the algorithm does not do deductions but can easily remember a
full stack of assumptions, which is something hard to do for the human
brain.


.. automodule:: sudoku

.. autoclass:: Sudoku

   .. attribute:: board 
    
      A 9x9 matrix which contains the digits on the sudoku board. An
      empty position is represented by a False value

   .. automethod:: Sudoku.candidates
        
   .. automethod::  Sudoku.attempt
        


.. autofunction:: sudoku.stack_assumptions

It is interesting to note that the backtracking algorithm (the
algorithm whichis able to stack assumptions) really is independant
from the sudoku rules. The algorithm requires an argument with a
precise interface and blindly triggers them, whether the argument is
manipulating a sudoku, the eight queens or the knight problem. When
the algorithm yields, the sudoku board or chessboard manipulated by
the argument has cooked a solution.


.. autofunction:: sudoku.make_generator_functions

