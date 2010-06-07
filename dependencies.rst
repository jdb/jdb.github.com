


=========================
 Scheduling dependencies
=========================

How to solve a set of dependencies? That is, given a set of
dependencies between nodes: a needs b, a needs c, c needs b, we want
an **sorted list of nodes where each nodes occurs *after* its
dependencies**. In this simple example, the sorted list is *b, c
a*. *b* is first, because *b* has no dependencies, *c* is next because
it only requires *a*, and *b* is last since it needs all the rest.

Several algorithms will be presented to compute the list:

* a naive method which presents but is computationaly to hard to be
  useful,

* graph methods: in this context, the list is called a topological
  sort. In Python, there is one implementation derived from the Python
  mailing list archive, written by Tim Peters, and another version in
  the *python-graph* package 

* finally


This problem can be represented as a graph:

>>> class Graph(object):
...     def __init__(self,nodes=[],edges=[]):
...         self.nodes = nodes
...         self.edges = edges
...
...     def __repr__(self):
...         return "[%s, %s]" % self.name, self.edges

>>> a, b, c = nodes = 'abc'
>>> # in this representation, (a,b) is read *a requires b*
>>> G = Graph( nodes, edges=[(a,b), (a,c), (c,b)])


We want a function which validates the cited constraint on a given
sorted list of nodes::

   prompt> G.sort()
   [b, c, a]

Now there are many ways to solve this problem: 

1. We can test each *permutation* of the list of node against the
   a function that verify that the constraint is respected

2. it is also possible to build a algorithm which explores the graph
   and builds what is actually called a *topological sort*

3. a *backtrack algorithm* can be build for this problem. As I can't
   briefly summarize the method, I'll invite you to the third section
   of this articles to the details of the method.

Testing each permutations
=========================

.. currentmodule:: brute

.. autosummary::
   :toctree:

   brute.deps
   brute.are_before
   brute.schedule

.. autofunction:: deps

*deps* is implemented in one line: ``return (dep for (n,dep) in 
G.edges if node==n)``


.. autofunction:: are_before

>>> def is_schedule(G, l):
...     return all( are_before(l,required(G,pivot),pivot) for pivot in l )
...
>>> incorrect_solution = [a, b, c]
>>> is_schedule(G, incorrect_solution)
False

This solution is not satisfying because a needs b, and on the other
hand, b is located after a (index(a)<index(b)).

>>> is_schedule( G, [b, c, a] )
True

Given a graph and a ordered list of nodes of the graph, *is_schedule*
returns whether for each element of the list, the dependency liste in
the given graph, are listed before the current element.

>>> from itertools import chain
>>> nodes = lambda G:( n for n in set(chain(*G)))
>>> sorted(list(nodes(G)))
[b, a, c]

*nodes* is function which returns a generator of the nodes of a graph.

>>> from itertools import permutations
>>> def schedule(G):
...     return list(filter(lambda l:is_schedule(G,l),permutations(nodes(G))))

Lets test the two examples at the top of this section:

Given a graph, schedule returns the list of list node where the
requirements are always listed before the node which require them.

>>> sorted(schedule(G))
[(b, c, a)]

This was long, documented and tested but this can be written in a much
shorter way:

>>> from itertools import chain,permutations as perm
>>> required = lambda G,node:(requirement for (n,requirement) in G if node==n)
>>> are_before = lambda L,l,p: all(L.index(n) < L.index(p) for n in l)
>>> is_schedule = lambda G,l: all(are_before(l,required(G,n),n) for n in l)
>>> nodes = lambda G:(n for n in set(chain(*G)))
>>> schedule = lambda G:list(filter(lambda l:is_schedule(G,l),perm(nodes(G))))
>>> sorted(schedule(G))
[(b, c, a)]

Now would this code works well on a simple and real life example?

>>> symbol = lambda l: Symbol(l) if len(l)==1 else [Symbol(n) for n in l] 
>>> jansson, libasnmp, libcommon, liblog = symbol("jansson libasnmp libcommon liblog".split())
>>> libapsi, libanevia, mediadescr, libts = symbol("libapsi libanevia mediadescr libts".split())
>>> rtplib, mp4lib, vodrtp = symbol("rtplib mp4lib vodrtp".split())
>>> deps = (
...   (liblog,(libasnmp,jansson),
...   (libapsi,(libcommon)),
...   (libanevia,(liblog)),
...   (mediadescr,(libanevia, libapsi, libcommon)),
...   (libavc,(libanevia, libcommon)),
...   (libts,(libanevia, libapsi, libavc, mediadescr)),
...   (rtplib,(libanevia, libapsi, libcommon, mediadescr)),
...   (mp4lib, libcommon, libanevia, mediadescr),
...   (vodrtp,libanevia, mediadescr, rtplib, mp4lib, libavc,liblog, libts))
>>> G =  chain(*(((n,r) for r in req)  for n,req in deps))
>>> print schedule(G)

