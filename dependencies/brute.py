


class Graph(object):
    def __init__(self,nodes=[],edges=[]):
        self.nodes = nodes
        self.edges = edges

    def __repr__(self):
        return "[%s, %s]" % self.name, self.edges

a, b, c = nodes = 'abc'

G = Graph( nodes, edges=[(a,b), (a,c), (c,b)])

def deps(G,node):
    """Given a graph, the *deps* method returns a generator of the
    deps nodes for the given node. Given *a*, *deps* returns *b* and
    *c* etc.

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
    Given a list, a sample of the first list, and a pivot, the
    *are_before* function returns whether the sample is indeed composed
    of elements located in the list, before the *pivot*.
 
    >>> are_before([a,b,c], [a,b], c)
    True
    >>> are_before([a,b,c], [a,c], b)
    False
    """

    return all(L.index(n) < L.index(pivot) for n in sample)



def is_schedule(G, l):
    """
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
    """
    return all( are_before(l,deps(G,pivot),pivot) for pivot in l )
    


from itertools import permutations
def schedule(G):

    """
    Lets test the two examples at the top of this section:
    
    Given a graph, schedule returns the list of list node where the
    requirements are always listed before the node which require them.
    
    >>> sorted(schedule(G))
    [(b, c, a)]
    """

    return list(filter(lambda l:is_schedule(G,l),permutations(G.nodes)))

# loose scoping bit me. use n in a doctest for a temporary variable
# and it will be bound for the rest of the module, even when written
# by error and a unboud exception was expected



#The whole module can effectively be shortened. Let's recap briefly:

if __name__=="__main__":

    from itertools import chain,permutations as perm

    deps        = lambda G,node:(req for (n,req) in G.edges if node==n)
    are_before  = lambda L,l,p: all(L.index(n) < L.index(p) for n in l)
    is_schedule = lambda G,l: all(are_before(l,deps(G,n),n) for n in l)
    schedule    = lambda G:filter(lambda l:is_schedule(G,l),perm(G.nodes))

    print schedule(G)


    class Symbol(object):
        def __init__(self,name):
            self.name = name

            def __repr__(self):
                return self.name

    symbols = lambda l: Symbol(l) if len(l)==1 else [Symbol(n) for n in l] 


    projects = "json snmp common log psi a media avc ts rtp mp4 vod".split()
    (json, snmp, common, log, psi, a, media, avc, 
     ts, rtp, mp4, vod ) = nodes = symbols( projects )

    data = {
        log     : (snmp,json),
        psi     : (common,),
        a       : (log,),
        media   : (a, psi, common),
        avc     : (a, common),
        ts      : (a, psi, avc, media),
        rtp     : (a, psi, common, media),
        mp4     : (common, a, media),
        vod     : (a, media, rtp, mp4, avc, log, ts)}

    reverse_edges = list(chain(*[[ (k,n) for n in v ] for k,v in data.iteritems()]))

    nodes = list(chain(*data.values()))
    nodes.extend(data.keys())

    G = Graph(set(nodes), [(c,p) for p,c in reverse_edges])
    
    s=schedule(G)
    print '\n'.join([str(e) for e in s])
    with open('toto.result','w') as f:
        f.write('\n'.join([str(e) for e in s]))
