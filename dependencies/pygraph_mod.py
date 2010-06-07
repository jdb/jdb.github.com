
from pygraph.algorithms.sorting import topological_sorting
from pygraph.classes.digraph import digraph
from data import deps

from itertools import chain

def prepare(dependencies):
   
    # As the topsort algorithm expects edges in the form (dependency,
    # project) and not (project, dependency), the dependency
    # dictionary entry 1:[2,3] becomes (3, 1), (2, 1), etc..

    edges = list(chain(*[[(dep,proj) for dep in dependencies[proj]]
                         for proj in dependencies]))

    nodes = set(chain(*edges))
    return edges, nodes


def topsort(edges, nodes):

    G = digraph()
    for n in nodes: 
        G.add_node(n)

    for e in edges: 
        G.add_edge(e)

    return topological_sorting(G)

if __name__=="__main__":
    print topsort(*prepare(deps))

