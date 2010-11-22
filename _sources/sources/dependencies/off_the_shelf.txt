
Topsort in available packages
=============================

Topsort is a fast algorithm operating on a set of dependencies, it
only returns one of the solutions. This is usually what is actually
needed: as for a labyrinth for instance, the problem usually is to
find the exit, not exhaustively list every possible way out.

The *topsort* package
---------------------

This package, available_ on Pypi, does not successfully installs at
this time (*june 2010*), but a working simplified version of the
algorithm is reproduced here (the graph cycle detection was suppressed
: make sure there are no circular dependencies in the input graph).

.. _available: http://pypi.python.org/pypi/topsort

The function has been written_ by Tim Peters, author of the
super efficient timsort_ algorithm. The function is in three steps :

.. _timsort: http://en.wikipedia.org/wiki/Timsort

.. _written: http://groups.google.com/group/comp.lang.python/msg/16d99cd6e9fe0302?dmode=source


#. the preparation of a small data structure: every nodes is
   associated to its number of child in a dictionary called
   *num_childs*,

#. the initial condition: the nodes without children (their
   *num_childs*' value is zero) are stored in the *answer* list, 

#. the loop iterates on the nodes in the *answer* list.  At
   each iteration, each current node's parents see its child count
   decremented by one. Whenever a child has zero parents, it is
   appended to the answer list. 

   The iteration stops when all nodes in the answer list has been
   processed.

At each iteration, the num_parents shrinks and the algorithm crunches
a smaller graph. The memory use of this algorithm does not increase
along the execution. Here is the code of this topsort:

.. literalinclude:: off_the_shelf.py
   :pyobject: tims_topsort


Let's try it on the small real world data used previously:

>>> from data import deps
>>> print tims_topsort(deps)
[3, 2, 4, 1, 5, 6, 7, 8, 9, 10, 11, 12] 

From the Pygraph package
------------------------

The topsort algorithm from the `Pygraph project`_ is imported from the
*sorting* algorithms package:

.. _`Pygraph project`: http://code.google.com/p/python-graph/

>>> from pygraph.algorithms.sorting import topological_sorting

This alogrithm requires a digraph as the input. *prepare()* takes a
dictionary of dependencies, detects the list of edges and the set of
nodes and returns an adapted digraph:

>>> from pygraph.classes.digraph import digraph

.. literalinclude:: off_the_shelf.py
   :pyobject: prepare

Then, it is just a matter of calling *topsort* on the digraph output:

>>> from data import deps
>>> print topological_sorting(prepare(deps))
[4, 5, 3, 2, 1, 6, 8, 7, 11, 10, 9, 12]

The simplified topsort runs four times faster than the implementation
in the pygraph packages, but most importantly it is a **million time
faster than the naive implementation**

>>> from timeit import Timer
>>> print Timer(lambda : tims_topsort(deps)).timeit(number=1000)
0.0732760429382
>>> print Timer(lambda : topological_sorting(prepare(deps))
...             ).timeit(number=1000)
0.333679914474
   
The unit is the second, a thousand executions of *tim(deps)* took 7
hundredths of a second that is *tim(deps)* took 7 microseconds.The
*topsort* from python-grapgh took 33 microseconds.

A big difference between the two algorithm it that the naive solution
will check every permutation possible while topsort starts with a small list
and only append correct nodes.

.. _erlang:

Topsort in Erlang
-----------------

Erlang actually provides a module in the standard library offering
several algorithm dealing with graphs. The ``digraph`` package offers
the primitives to manages graphs, the ``digraph_utils`` package offers
the algorithm. The code presented below is actually very similar to
our script based on the Pygraph project: first the construction of the
digraph, then the execution of the algorithm.
 
.. literalinclude:: topsort_stdlib.erl
   :language: erlang

The next part of this article, :doc:`bfs_dfs` presents several "by
hand" implementations of topsort as graph traversal. The generic
method of graph traversal can be adapted to build high performance or
distributed implementations.
