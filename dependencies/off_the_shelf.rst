
Topsort in available Python packages
====================================

Topsort is a fast operating on a set of dependencies, and only returns
one of the solutions. This is usually what is acutally needed: as for a
labyrinth, the problem really is to find the exit, not exhaustively
list every available way out.


The *topsort* package
---------------------

This package, available_ on Pypi, does not successfully installs at
this time (*june 2010*), but a working simplified version of the
algorithm is reproduced here (the graph cycle detection was suppressed
: make sure there are no circular dependencies in the input graph).

.. _available: http://pypi.python.org/pypi/topsort

The function seems_ to have been written by Tim Peters, authors of the
super efficient timsort_ algorithm. The function is in three steps :

.. _timsort: http://en.wikipedia.org/wiki/Timsort

.. _seems: http://groups.google.com/group/comp.lang.python/msg/16d99cd6e9fe0302?dmode=source


#. the preparation of a small data structure: every nodes is
   associated to its number of child in a dictionary called *num_parents*

#. the initial condition: the nodes without parents (their
   num_parents' value is zero) are appended to the *answer* list and
   suppressed from the num_parents dictionary, 

#. the iteration operates on the nodes without parents in the .  At each iteration, each current
   node's children see its parent count decremented by one, whenever a
   children has no more parents, it is appended at the end of the
   answer and suppress from num_parents. At each iteration, the
   num_parents shrinks and the algorithm crunches a smaller graph.

Here is the code of this topsort:

.. literalinclude:: off_the_shelf.py
   :pyobject: tims_topsort

Topsort actually computes the path from the most dependent tasks to
the most independent task, we'll want to reverse the list to suits
our context.

  return list(reversed(answer))

Let's try it on a small real world graph in the data package:

>>> from data import deps
>>> from pprint import pprint
>>> pprint(deps)
{1: [2, 3],
 5: [4],
 6: [1],
 7: [6, 5, 4],
 8: [6, 4],
 9: [6, 5, 8, 7],
 10: [4, 6, 7],
 11: [6, 5, 4, 7],
 12: [6, 7, 11, 10, 8, 1, 9]}

>>> print tims_topsort(deps)
[3, 2, 4, 1, 5, 6, 7, 8, 9, 10, 11, 12] 

From the Pygraph package
------------------------

The algorithm is imported from the *sorting* algorithm, and operates
on digraphs

>>> from pygraph.algorithms.sorting import topological_sorting
>>> from pygraph.classes.digraph import digraph

Before using the algorithm, the input digraph must be built:
*prepare()* takes a dictionary of dependencies, detects the list of
edges and the set of nodes and returns an adapted digraph:

.. literalinclude:: off_the_shelf.py
   :pyobject: prepare

>>> from data import deps
>>> print topological_sorting(prepare(deps))
[4, 5, 3, 2, 1, 6, 8, 7, 11, 10, 9, 12]

The simplified topsort runs four times faster than the implementation
in the pygraph packages::

   >>> from timeit import Timer
   >>> print Timer(lambda : tims_topsort(deps)).timeit(number=1000)
   0.0732760429382
   >>> print Timer(lambda : topological_sorting(prepare(deps))
   ...             ).timeit(number=1000)
   0.333679914474
   
The unit is the second, a thousand execution of *tim(deps)* last 7
hundredth of a second: *tim(deps)* executes in 7 microseconds.
