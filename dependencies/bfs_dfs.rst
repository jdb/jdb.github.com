
Graph traversal
===============

Four algorithm are presented here which exhaustively find all the
solutions, two depth search first (DFS) and two breadth search
first (BFS): 

1. After the classic DFS algorithm, an recursive generator is
   presented. It does not return the whole list after a while,
   instead (being a generator), it returns one solution and then yield
   back execution until called again.

2. After the classic BFS algorithm, a recursive SQL query is
   presented. It makes it possible to solve problems directly on the
   SQL server without going to the trouble of extracting the data to
   an SQL client, then finding the solution. This solution is very
   fast.

The algorithms will make use of the following primitives.

**prepare()** function adapts the input dictionary of dependencies
into the almost same dictionary: except that 1. the values are set
and that also that 2. the project with no dependencies are also set
as keys with an empty set as the value

.. literalinclude:: bfs_dfs.py
   :pyobject: prepare

**candidates(projects, deps, path)** returns the list of project nodes
satisfying the constraint to be added to the path: not being already
in the path and having all its dependencies in the path. The
constraints are checked using the set operators: ``a <= b`` means *a* is
included in *b*, and ``a - b`` means the element of *a* without the
element from *b*.

.. literalinclude:: bfs_dfs.py
   :pyobject: candidates


Depth first search
------------------

The candidates are computed for the current path, and for each
candidate, the function is called with the path augmented with the
candidate.

The *initial condition* is the empty path for which the candidates
will be the nodes without dependencies. 

The *termination condition* is the absence of any more candidates
nodes: there is no dead-end path when only the correct candidates
nodes are explored. Whenever the termination condition is met, the
current path is added to the accumulator, and the function returns.

.. literalinclude:: bfs_dfs.py
   :pyobject: dfs

.. _recursive_gen:

Recursive generator
-------------------

It is inspired by ... the Python regression test suite for the yield
keyword (here_).

here

#. functions are objects with their own namespace: the idfs declares a
   private function *_idfs* and a private class *Path*. The only real
   code embedded in the function is the call to the private function:
   ``return _idfs()``

#. *_idfs* will need to append elements to a list, but it *must* use
   the *binding interface* of this object (elements will be *set* to
   it instead of appended to it). A special class *Path* is designed
   to do that which can be used like this
 
   >>> obj = Path()
   >>> obj
   []
   >>> obj[0] = 1
   >>> obj[0] = 2
   >>> obj[0] = 3
   >>> obj
   [1, 2, 3]
   >>> obj.pop()
   3
   >>> obj
   [1, 2]

   This class derives from list: when *setitem* is called with a new
   element, it is the append function which is called.

#. 


.. literalinclude:: bfs_dfs.py
   :pyobject: idfs


Breadth first search
--------------------

.. literalinclude:: bfs_dfs.py
   :pyobject: bfs


.. _recursive_query:

Recursive SQL queries
---------------------

.. literalinclude:: topsort.sql
   :language: sql




