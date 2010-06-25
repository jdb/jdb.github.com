
======================
 Sorting dependencies
======================

This article is on different ways to solve a set of dependencies. That
is, given a set of dependencies between nodes (think of projects or
software packages): a needs b, a needs c, c needs b, we want an
**sorted list of nodes where each nodes occurs *after* its
dependencies**. In this simple example, the sorted list is *b, c
a*. *b* is first, because *b* has no dependencies, *c* is next because
it only requires *b* which is already in the list, and *a* is last
since it needs all the rest.

.. toctree::
   :hidden:

   dependencies/brute.py
   dependencies/off_the_shelf
   dependencies/bfs_dfs


Several algorithms will be presented to build this list:

* A naive method which is simple to read and understand: a function
  test if list satisfies the dependencies, and this function is
  applied to all possible permutation of the node list. But is
  computationaly too hard to be useful: it takes much too long to
  solve even simple sets of dependencies:

  :doc:`dependencies/brute.py`

* Finding the sorted list is actually a known problem and the
  solutions are called topological sort. A topological sort
  implementation returns quickly only one of the possible solution. In
  Python, there is one implementation in the package *topsort*,
  derived from a mail in the Python mailing list written by Tim Peters
  and also, another version in the *python-graph* package.

  :doc:`dependencies/off_the_shelf`

  All languages have their advantages: for a recursive algorithm
  dealing and the manipulation of lists, Erlang is particularly
  adapted. Even more, actually, the topsort algorithm is part of
  Erlang standard library.

  :ref:`erlang`

* Yet another way to solve this problem is to consider *the graph of
  the candidates*, that is given the first part of the sorted list of
  nodes, consider as the children of the last node of the list: all
  the nodes which are not yet in the list and whose dependencies are
  in the list. Then, it is just a matter of traversing the graph in
  depth first or breadth first to find the list of all possible
  solutions.

  :doc:`dependencies/bfs_dfs`

  In depth search first (DFS), it is possible to build a generator of
  the solutions: the solution are not computed in a long batch,
  accumulated and returned as a long list, the solutions are available
  as soon as they are found. The processing of the solution alternates
  with the search for the next solution. 

  For instance, a solution can be emitted to a client which draws the
  solution, while the server continues the exhaustion of the
  solutions.

  :ref:`recursive_gen`

  It is actually possible to do a breadth first search traversal of the
  graph in pure SQL (since Postgresql 8.4) using the recent standard
  ``with recurse`` queries available in PostgreSQL 8.4.
  Performance-wise, the SQL query is one hundred time faster that the
  traversal in pure CPython. The SQL query (which find all solutions)
  is actually on par with the topological sort (which finds only one).
  
  :ref:`recursive_query`

.. todo::

   Shows a grok + yui incremental drawing of the solutions.

   Shows a distributed graph traversal.

