
Graph traversal
===============

Four algorithm are presented here which exhaustively find all the
solutions, two depth search first (DFS) and two breadth search
first (BFS): 

1. After the classic DFS algorithm, an recursive generator is
   presented. It does not return the whole list after a while,
   instead (being a generator), it returns one solution and then yields
   back execution until called again,

2. After the classic BFS algorithm, a recursive SQL query is
   presented. It makes it possible to solve problems directly on the
   SQL server without going to the trouble of extracting the data to
   an SQL client, then finding the solution. This solution is very
   fast.

The algorithms will make use of the following primitives:

**prepare(deps)** adapts the input dictionary of dependencies into the
almost same dictionary: except that 1. the values are turned from list
to sets, and 2. the projects with no dependencies are added to the
dictionary with an empty set as the value. This function is called
once, prior to the algorithm.

.. literalinclude:: bfs_dfs.py
   :pyobject: prepare

**candidates(projects, deps, path)** returns the list of project nodes
satisfying the constraint to be added to the path: not being already
in the path and having all its dependencies in the path. The
constraints are checked using the set operators: ``a <= b`` means *a*
is included in *b*, and ``a - b`` means the element of *a* without the
element from *b*. This function is called in the algorithm, at each
recursion.

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

Thanks to the *yield* keyword, there is no need to accumulate the
solutions, as with the previous algorithm, which leads to a simpler
algorithm:

.. literalinclude:: bfs_dfs.py
   :pyobject: idfs


Breadth first search
--------------------

In breadth first search, at each iteration, it is not one path, but
the list of all possible path which is computed, and there is no
backtracking as with the DFS algorithm. A completely new list of
augmented path is generated from the input list of incomplete paths:
for each incomplete input path, a list of the path augmented with one
candidate is built. 

The *termination condition* is when no path from the input list can be
augmented.

The *initial condition* is a list of one empty path. 

.. literalinclude:: bfs_dfs.py
   :pyobject: bfs

.. _recursive_query:

Recursive SQL queries
---------------------

The recent addition of the **with recurse** statement in Postgresql
makes it possible to delegate complex computing to the database,
without requiring the overhead of extracting the data and processing
it on the database client. The syntax is a bit idiomatic, and is well
explained in the official documentation: here_ and especially there_.

.. _here: http://www.postgresql.org/docs/current/static/sql-select.html#SQL-WITH

.. _there: http://www.postgresql.org/docs/current/static/queries-with.html

Simply put:

#. the ``with recurse`` statement defines a temporary table called
   topsort with three columns: project, dependencies, path,,

#. then, there are two clauses separated by UNION ALL,

   #. the first clause is the *initial condition*: the empty path,

   #. the second clause is the recursive one: it selects from topsort.
      This clause augments each record in the topsort table with the
      project, only the rows statisfying the *candidates* conditions
      above are added to the topsort table.

#. the termination condition is implicit, it is reached when the
   recursive clause produces no more rows, 

#. as the topsort table keeps the incomplete path from each iteration,
   the final restriction keeps only the complete path (those were
   every projects was cited).


.. literalinclude:: topsort.sql
   :language: sql


.. actually the with recurse algorithm does not do much more than
.. manupulating temporary tables, it could be explicity controlled
.. from the client in databases which do not support with recurse ->
.. the gains still is data and most computations stays on the
.. server...



