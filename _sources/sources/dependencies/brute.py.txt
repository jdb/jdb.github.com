
A naive, CPU hungry solution
============================



Let's say there are three nodes a, b, c:

::

  a, b, c = nodes = 'abc'
  
They are linked by the following dependencies, a needs b, a needs c,
c needs b.

::

  edges=[(a,b), (a,c), (c,b)]
  
  
Let's build a simple class to hold the nodes and edges as attributes

::

  class Graph(object):
      def __init__(self,nodes=[],edges=[]):
          self.nodes = nodes
          self.edges = edges
  
  G = Graph(nodes, edges)
  
Three primitives: *deps*, *are_before* and *is_winner*
------------------------------------------------------

To solve our problem, three simple primitives are written: *deps()*,
*are_before()* and *is_winner()*. 

**deps()** returns the dependencies for the given graph and node

:: 

  def deps(graph,node):
      return (dep for (n,dep) in graph.edges if node==n)
  
Given *a*, *deps* returns *b* and *c*, given *c*, *deps* returns *b*, etc.

>>> list(deps(G,a))
[b, c]
>>> list(deps(G,c))
[b]
>>> list(deps(G,b))
[]



**are_before()** returns whether the sample is indeed composed of
elements located in the list, before the *pivot*.

::

  def are_before(List, sample, pivot):
      return all(List.index(n) < List.index(pivot) for n in sample)
  

>>> are_before([a,b,c], [a,b], c)
True
>>> are_before([a,b,c], [a,c], b)
False

**is_winner()** checks whether the list satisfies the dependency graph.

::

  def is_winner(graph, List):
      return all(are_before(List,
                            deps(graph, pivot),
                            pivot) 
                 for pivot in L)
  
>>> incorrect_solution = [a, b, c]
>>> is_winner(G, incorrect_solution)
False
   
This solution is not satisfying because a needs b, and on the other
hand, b is located after a (index(a)<index(b)).
   
>>> is_winner( G, [b, c, a] )
True
  
The search() function
---------------------

*search()* combines the previous primitives to process a graph given
as an input and returns the list of the solutions i.e. the list of
permutations of the nodes where the requirements are always listed
before the nodes which requires them

::

  from itertools import permutations
  def search(graph):
      return filter(lambda l:is_winner(graph,l),
                    permutations(graph.nodes))
  
>>> sorted(schedule(G))
[(b, c, a)]
 
Really this algorithm is quite simple and can be expressed in four
lines of Python: let's recap briefly

::

  from itertools import chain, permutations as perm
  deps       = lambda G,node:(req for (n,req) in G.edges if node==n)
  are_before = lambda L,l,p: all(L.index(n) < L.index(p) for n in l)
  is_winner  = lambda G,l: all(are_before(l,deps(G,n),n) for n in l)
  search     = lambda G: filter(lambda l:is_winner(G, l), perm(G.nodes))
  
>>> print search(G)
[b, c, a]

Complexity bites
----------------

Let's try our functions on a real life example, it is not even
really big. There are nine tasks with dependencies::

  >>> from data import deps as data
  >>> from pprint import pprint
  >>> pprint(data)
  {1: [2, 3],
   5: [4],
   6: [1],
   7: [6, 5, 4],
   8: [6, 4],
   9: [6, 5, 8, 7],
   10: [4, 6, 7],
   11: [6, 5, 4, 7],
   12: [6, 7, 11, 10, 8, 1, 9]}

  # Transforming the dictionary into two lists: edges and nodes
  >>> edges = list(
      chain(*[[ (n,k) for n in v ] for k,v in data.iteritems()]))
  >>> nodes = list(set(chain(*data.values())))
  >>> nodes.extend(data.keys())

  >>> print nodes
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

  >>> print edges
  [(2, 1), (3, 1), (4, 5), (1, 6), (6, 7), (5, 7), (4, 7), (6, 8),
  (4, 8), (6, 9), (5, 9), (8, 9), (7, 9), (4, 10), (6, 10), (7, 10),
  (6, 11), (5, 11), (4, 11), (7, 11), (6, 12), (7, 12), (11, 12),
  (10, 12), (8, 12), (1, 12), (9, 12)]

  >>> G = Graph(nodes, edges)
  >>> print search(G)
  [[4, 5, 3, 2, 1, 6, 8, 7, 11, 10, 9, 12], ...

The search seems to never return and actually took a whole night to
be able to finish.  We hit a *complexity wall*. Let's have a look at
the respective algorithmic complexity of the functions::

  O(deps)       = O(n)
  
This notation means that the computations defined in *deps()* is
directly proportional to the size *n*, of the input data. For
*are_before()*, this is worse: the computations are proportional to
the *square* on the input data::

  O(are_before) = O(l * 2 O(index))
                = O(l * O(n))
                = O(n2)
  
The complexity for *is_winner()* and *search()* are also high::

  O(is_winner)  = O(l * O(are_before) + O(l * O(deps))
                = O(l * O(n2)  + O(l* O(n)))
                = O( O(n3)  + O(n2) )
                = O(n3)
  
  O(search)     = O(is_winner) * O(perm)
                = O(n3) * O(n!)
                = O(n!)

On the first hand, *deps()* and *are_before()* can be enhanced to
reduce their complexity:

#. using a list that needs to be unrolled to get the dependencies of
   a node is suboptimal, instead a dictionary data structure is more
   adapted to access the dependencies of a node directly. Complexity
   would come down from O(n) to O(1).

#. *index()*'s execution time depends on the size of the list. Using
   a dictionary where the position of the list value would be
   accessed in constant time is more efficient. *are_before()* would
   operate in O(n) instead of O(n2)

But these improvements are cosmetic with regards to the size fo the
data to test: if 12 nodes needs to be sorted, as with the data part
of the *deps* module below, then 12! = 479 001 600 (half a billion)
permutations needs to be tested. While actually, entire branches do
not need to be tested: see the next article: :doc:`off_the_shelf`,
for better ways to sort dependencies.

