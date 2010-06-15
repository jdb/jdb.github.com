
# Let's say there are three nodes a, b, c:

a, b, c = nodes = 'abc'

# They are linked by the following dependencies, a needs b, a needs c,
# c needs b.

edges=[(a,b), (a,c), (c,b)]


# Let's build a simple class to hold the nodes and edges as attributes

class Graph(object):
    def __init__(self,nodes=[],edges=[]):
        self.nodes = nodes
        self.edges = edges

G = Graph( nodes, edges)


# To solve our problem, three simple primitives are written: *deps()*,
# *are_before()* and *is_winner()*. *search()* combines these
# primitives and from a Graph given as an input, returns the list of
# solution

def deps(G,node):
    """returns the dependencies for the given graph and node.

    Given *a*, *deps* returns *b* and *c* etc.

    >>> list(deps(G,a))
    [b, c]
    >>> list(deps(G,c))
    [b]
    >>> list(deps(G,b))
    []
    """   
    return (dep for (n,dep) in G.edges if node==n)


def are_before(L, sample, pivot):
    """
    returns whether the sample is indeed composed of elements located
    in the list, before the *pivot*.
 
    >>> are_before([a,b,c], [a,b], c)
    True
    >>> are_before([a,b,c], [a,c], b)
    False
    """
    return all(L.index(n) < L.index(pivot) for n in sample)


def is_winner(G, L):
    """
    checks whether the list satisfies the dependency graph.

    >>> incorrect_solution = [a, b, c]
    >>> is_winner(G, incorrect_solution)
    False
    
    This solution is not satisfying because a needs b, and on the other
    hand, b is located after a (index(a)<index(b)).
    
    >>> is_winner( G, [b, c, a] )
    True
    
    Given a graph and a ordered list of nodes of the graph, *is_winner*
    returns whether for each element of the list, the dependency liste in
    the given graph, are listed before the current element.
    """
    return all( are_before(L,deps(G,pivot),pivot) for pivot in L )
    


from itertools import permutations
def search(G):

    """
    returns the list of list node where the requirements are always
    listed before the node which require them.

    >>> sorted(schedule(G))
    [(b, c, a)]
    """
    return list(filter(lambda l:is_winner(G,l),permutations(G.nodes)))



if __name__=="__main__":

    from itertools import chain, permutations as perm

    # Let's recap briefly:
    deps       = lambda G,node:(req for (n,req) in G.edges if node==n)
    are_before = lambda L,l,p: all(L.index(n) < L.index(p) for n in l)
    is_winner  = lambda G,l: all(are_before(l,deps(G,n),n) for n in l)
    search     = lambda G: filter(lambda l:is_winner(G, l), perm(G.nodes))

    print search(G)

    # Death by complexity: this code eats the maximum of CPU and seems
    # to never return. Let's have a look at the respective complexity
    # of the functions:

    # deps       : O(edges)                              = O(n)
    # are_before : O(l * 2 O(index)) = O(l * O(n))       = O(n2)
    # is_winner  : O(l * O(are_before) ) + O(l* O(deps)) = O(n3)
    # search     : O(is_winner) * O(perm) = O(n3) *O(n!) = O(n!)

    # There is nothing you can really do with an algorithm in O(n!),
    # if 12 nodes needs to be sorted, then 12! = 479 001 600
    # permutations needs to be tested.

    # from data import deps

    # edges = list(
    #     chain(*[[ (n,k) for n in v ] for k,v in data.iteritems()]))
    # nodes = list(chain(*data.values()))
    # nodes.extend(data.keys())

    # G = Graph(set(nodes), edges)
    
    # with open('brute.result', 'w') as f:
    #     f.write('\n'.join([str(e) for e in search(G)]))
