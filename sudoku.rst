

A sudoku solver
===============


Here is an algorithm:

#. create a new chessboard

#. add the existing data

#. loop 
   
   #. if there are no empty slots, yield the chessboard which is a
      solution, else

   #. take an empty slot and compute the candidates

   #. for each candidate

      #. put the candidate in the empty slot and yield loop

The chessboard is composed of a matrix of positions of 9x9 as well as
27 sets (9 line sets, 9 columns sets, 9 squares), and several
validation fonctions:

- in matrix[i][j] there is either None which means empty or a digit
  between 1 and 9

- to find the candidates for a given slot i,j, filter the the list 1
  to 9 on the absence in all  line[i], column[j] and square[10*i+j]
  
  It is completely possible to represents each of the 27 sets as
  bitfield of length(9): if bit number 4 in the bitfield/set line[6]
  is set to True, then line number 6 already has the number 4 (you
  can't know the position, the matrix is here for that ). 

