
Graph traversal
===============

Four algorithm are presented here which exhaustively find all the
solutions, first the basic depth search first and breadth search
first. Then two variations of each which both present interesting
features:

1. the iterative generator based on a depth search first algorithm does
   not return the whole list after a while, instead, (being a
   generator) it returns one solution and then yield back execution
   until called again. 

2. the recursive SQL query makes it possible to solve problems
   directly on the SQL server without going to the trouble of
   extracting the data to an SQL client, then finding the
   solution. This solution is very fast.

They Python algorithm will make use of these primitives.

**prepare()** function adapts the input dictionary of dependencies
into the almost same dictionary: except that 1. the values are set
and that also that 2. the project with no dependencies are also set
as keys with an empty set as the value

.. literalinclude:: bfs_dfs.py
   :pyobject: prepare

**candidates()** returns the list of nodes satisfying the constraint
to be added to the path.

.. literalinclude:: bfs_dfs.py
   :pyobject: candidates


Depth first search
------------------

.. literalinclude:: bfs_dfs.py
   :pyobject: dfs


Breadth first search
--------------------

.. literalinclude:: bfs_dfs.py
   :pyobject: bfs

.. _recursive_gen:

Recursive generator
-------------------

.. literalinclude:: bfs_dfs.py
   :pyobject: idfs

.. _recursive_query:

Recursive SQL queries
---------------------

.. literalinclude:: topsort.sql
   :language: sql




