
from itertools import chain

def tims_topsort(deps):

    # 1. data structure preparation
    edges = list(chain(*[[(parent,child) for parent in deps[child]] 
                         for child in deps ]))

    num_childs = dict([ (k,0) for k in chain(*edges) ])
    for parent,_ in edges: 
        num_childs[parent] += 1 

    # 2. initial condition
    answer = filter(lambda x: num_childs[x] == 0, num_childs)

    # 3. traversing the graph
    for child in answer:
        if deps.has_key(child):
            for parent in deps[child]:
                num_childs[parent] -= 1
                if num_childs[parent] == 0:
                    answer.append(parent)

    return list(reversed(answer))

if __name__=="__main__":
    from data import deps
    print tims_topsort(deps)

from pygraph.algorithms.sorting import topological_sorting
from pygraph.classes.digraph import digraph

def prepare(deps):
   
    # As the topsort algorithm expects edges in the form (dependency,
    # project) and not (project, dependency), the dependency
    # dictionary entry 1:[2,3] becomes (3, 1), (2, 1), etc..

    edges = list(chain(*[[(parent,child) for parent in deps[child]]
                         for child in deps]))
    nodes = set(chain(*edges))

    G = digraph()
    for n in nodes: 
        G.add_node(n)
    for e in edges: 
        G.add_edge(e)

    return G

if __name__=="__main__":
    from data import deps
    print topological_sorting(prepare(deps))
