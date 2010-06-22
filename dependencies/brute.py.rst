
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
  
  G = Graph( nodes, edges)
  
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
  
  print search(G)
  
Complexity bites
----------------

::

  # Death by complexity: this code seems to never return. Let's have a
  # look at the respective complexity of the functions::
  # 
  #   O(edges)      = O(n)
  #   
  #   O(are_before) = O(l * 2 O(index))
  #                 = O(l * O(n))
  #                 = O(n2)
  #   
  #   O(is_winner)  = O(l * O(are_before) + O(l * O(deps) )
  #                 = O(l * O(n2)  + O(l* O(n)))
  #                 = O( O(n3)  + O(n2) )
  #                 = O(n3)
  #   
  #   O(search)     = O(is_winner) * O(perm)
  #                 = O(n3) * O(n!)
  #                 = O(n!)
  # 
  # There is nothing you can really do with an algorithm in O(n!), if 12
  # nodes needs to be sorted, as with the data part of the *deps* module
  # below, then 12! = 479 001 600 permutations needs to be tested. The
  # follozing lines import a dictionary of dependencies and transform it
  # into a graph
  # 
  # .. sourcecode:: python
  #
  #   from data import deps
  #   
  #   edges = list(
  #       chain(*[[ (n,k) for n in v ] for k,v in data.iteritems()]))
  #   nodes = list(chain(*data.values()))
  #   nodes.extend(data.keys())
  #   
  #   G = Graph(set(nodes), edges)
  #   
  # The following resolution took the whole night to be able to compute 
  # 
  # .. sourcecode:: python
  #
  #   print "Warning: long computation ahead, be patient"
  #   with open('brute.result', 'w') as f:
  #       f.write('\n'.join([str(e) for e in search(G)]))
  # 
  # No really, we can't use such a costly algorithm, see the next article:  
  # :doc:`dependencies/off_the_shelf`, for better results
  d
