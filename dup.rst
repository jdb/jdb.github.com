
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

>>> dict( (i,None) for i in [1, 2, 3, 4, 3, 4, 3, 4] ).keys()

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

>>> from collections import OrderedDict
>>> list(OrderedDict((i,None) for i in [1, 2, 3, 4, 3, 4, 3, 4]).keys())
[1, 4, 3, 2]


.. it seems it is not adapted to declare function in doctests, they
.. are not available for other snippets. 

.. doc difficulties: reference each other easily, structure doc and
.. code orthogonally, test documentation

What do you mean by fast?
=========================

>>> from random import randint
>>> def randlist(size, freq, almost_sorted=False):
...     d = {'short': 10, 'long': 500, 'few': 3, 'tons': 0.5}
...     l = [ randint(1, int( d[size]*d[freq])) for _ in range(d[size]) ]
...     if almost_sorted:
...         l.sort()
...         for _ in range(int(d[size] * 0.01)):
...             n, m = randint(0, d[size]-1), randint(0, d[size]-1)
...             l[n], l[m] = l[m], l[n]
...     return l


>>> liste = dict([ ((s, f, a), randlist(s, f, a)) for s in ('short', 'long') for f in ('few', 'tons' ) for a in (True, False)])

>>> if __name__ == '__main__':
...    from timeit import Timer
...    for k,v in liste.items():
...       for cmd in "forloop oneline dicodsu dico dicofirst listexp genexp".split():
...          t=Timer( 'dup.%s(dup.liste[%s])' % (cmd,k), "import dup").timeit(number=10)
...          print ';'.join([cmd, k[0], k[1], k[2] and "shuffle" or "almost_sorted", str(t)]) # .replace('.',',')


Here are the results computed on a laptop. The size for the long lists
was 100 000::
  
  forloop	long	few	shuffle		1.23025918007
  oneline	long	few	shuffle		0.466639995575
  dicodsu	long	few	shuffle		3.7867770195
  dico		long	few	shuffle		2.11409592628
  dicofirst	long	few	shuffle		2.12672519684
  listexp	long	few	shuffle		1683.45610189
  genexp	long	few	shuffle		1687.05760503
  forloop	long	tons	almost_sorted	0.596557855606
  oneline	long	tons	almost_sorted	0.464272022247
  dicodsu	long	tons	almost_sorted	1.32849097252
  dico		long	tons	almost_sorted	0.931100845337
  dicofirst	long	tons	almost_sorted	0.938807964325
  listexp	long	tons	almost_sorted	3163.15273285
  genexp	long	tons	almost_sorted	3197.41649318
  forloop	long	few	almost_sorted	0.807441949844
  oneline	long	few	almost_sorted	0.492161035538
  dicodsu	long	few	almost_sorted	2.99654698372
  dico		long	few	almost_sorted	1.69496893883
  dicofirst	long	few	almost_sorted	1.68966412544
  listexp	long	few	almost_sorted	4815.66312003
  genexp	long	few	almost_sorted	4811.47094703
  forloop	long	tons	shuffle		1.55969285965
  oneline	long	tons	shuffle		0.436213970184
  dicodsu	long	tons	shuffle		2.12376403809
  dico		long	tons	shuffle		1.31656694412
  dicofirst	long	tons	shuffle		1.3203151226
  listexp	long	tons	shuffle		3476.23947001
  genexp	long	tons	shuffle		3506.11089492
  forloop	short	tons	shuffle		0.507568836212
  oneline	short	tons	shuffle		8.58306884766e-05
  dicodsu	short	tons	shuffle		0.000180006027222
  dico		short	tons	shuffle		0.000163078308105
  dicofirst	short	tons	shuffle		0.000141143798828
  listexp	short	tons	shuffle		0.297842979431
  genexp	short	tons	shuffle		0.301390886307
  forloop	short	few	almost_sorted	0.508334875107
  oneline	short	few	almost_sorted	9.08374786377e-05
  dicodsu	short	few	almost_sorted	0.000224113464355
  dico		short	few	almost_sorted	0.000182867050171
  dicofirst	short	few	almost_sorted	0.00016188621521
  listexp	short	few	almost_sorted	0.278187036514
  genexp	short	few	almost_sorted	0.281796216965
  forloop	short	tons	almost_sorted	0.512351036072
  oneline	short	tons	almost_sorted	8.48770141602e-05
  dicodsu	short	tons	almost_sorted	0.000176906585693
  dico		short	tons	almost_sorted	0.000161170959473
  dicofirst	short	tons	almost_sorted	0.000136852264404
  listexp	short	tons	almost_sorted	0.272169113159
  genexp	short	tons	almost_sorted	0.275593042374
  forloop	short	few	shuffle		0.511206865311
  oneline	short	few	shuffle		9.10758972168e-05
  dicodsu	short	few	shuffle		0.000253200531006
  dico		short	few	shuffle		0.000255107879639
  dicofirst	short	few	shuffle		0.000176906585693
  listexp	short	few	shuffle		0.345485925674
  genexp	short	few	shuffle		0.349174022675
  
