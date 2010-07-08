
==================================
 Suppressing duplicates in a list
==================================

Each of the following functions returns a list with no duplicates from
the list given as argument. Three approaches: the simplest approach,
faster methods which do not respect the original ordering, and fast
methods which do respect the ordering. All in all, this problem is
easily solved with Python's builtin.

Simplest naive algorithm
========================

The following function checks that the new values in the input list
were not already *seen*:

.. literalinclude:: dup.py
   :pyobject: naive

The *in* operator, operating on a list gets slower when the list
grows. Here is a shorter implementation of the same algorithm which
presents two subtleties with regard to the Python language:

.. literalinclude:: dup.py
   :pyobject: buggy_naive

#. the argument default values are only evaluated once: when the
   function is defined. In our case, the default value for *nodups*
   is a pointer to a list which happens to be empty at the function
   definition. while the pointer to the list will never change, the
   list itself might be updated and modified. Do not be surprised if
   the function's data is not the same between each call: the
   default value is not re-initialiased.

#. *nodups.append()* does not really return a result as it is a side
   effect (*None* is actually returned). The list comprehensions
   will update the *nodups* list, but will also create internally a
   list as long as the input list, filled with *None*.

There are faster methods to get rid of duplicates.

Faster methods, which does not respect input list order
=======================================================

The list gets sorted first, then to check whether a value has been
seen: it is only necessary to check against one value instead of a list.

.. literalinclude:: dup.py
   :pyobject: usort

Another approach is to store the elements behind a checksum: the same
element are quickly found, they are behind the same checksum. The
Python dictionary can do that easily (it is only a matter of storing
an empty value):

.. literalinclude:: dup.py
   :pyobject: dico

Actually a iterable without duplicate is also called a set: another
way to present the problem is to transform a list into a set!

>>> set([1, 2, 3, 4, 3, 4, 3, 4])
set([1, 2, 3, 4])

The Python set is actually implemented with a dictionary whose values
are set to *None*.


Respect the original order
==========================

Returns a list whose *first* occurences of duplicates were removed:
	
.. literalinclude:: dup.py
   :pyobject: keep_last

Same algorithm but the *last* duplicates are removed (pretty much
what is really expected) same performance as dicofirst()

.. literalinclude:: dup.py
   :pyobject: keep_first

Recent Python2.7 and Python3.1 gained a new data structure in the
collections package: the ordered dict which remembers the order of the
input keys:

.. literalinclude:: dup.py
   :pyobject: odict

*Et voila*, set and OrderedDict are Python builtins: the language has
many facilities directly available to solve this problem.


What do you mean by fast?
=========================

Let's build different lists with different characteristics and time
each implementation. *randlist* returns a list according to input
characteristics:

.. literalinclude:: dup.py
   :pyobject: randlist

*make_lists* yields the random lists for all the permutations of the
possible characteristics:

.. literalinclude:: dup.py
   :pyobject: make_lists

From our short benchmark, the *set* and *keep_\** functions are
efficient. The naive algorithm should really be avoided and the
ordered dict, though a builtin, seems four times less efficient than
the keep_* function based on the dict and enumerate functions.
