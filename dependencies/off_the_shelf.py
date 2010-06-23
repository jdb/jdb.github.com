
from itertools import chain

def tims_topsort(deps):

    # 1. data structure preparation
    edges = list(chain(*[
                [(child,parent) for parent in deps[child]] 
                for child in deps ]))

    num_parents = dict([ (k,0) for k in chain(*edges) ])
    for _,child in edges: 
        num_parents[child]+=1 

    # 2. initial condition
    answer = filter(lambda x: num_parents[x] == 0, num_parents)

    # 3. running over the graph
    for parent in answer:
        del num_parents[parent]
        if deps.has_key(parent):
            for child in deps[parent]:
                num_parents[child] -= 1
                if num_parents[child] == 0:
                    answer.append(child)

    return list(reversed(answer))


from pygraph.algorithms.sorting import topological_sorting
from pygraph.classes.digraph import digraph

def prepare(deps):
   
    # As the topsort algorithm expects edges in the form (dependency,
    # project) and not (project, dependency), the dependency
    # dictionary entry 1:[2,3] becomes (3, 1), (2, 1), etc..

    edges = list(chain(*[[(dep,proj) for dep in deps[proj]]
                         for proj in deps]))
    nodes = set(chain(*edges))

    G = digraph()
    for n in nodes: 
        G.add_node(n)
    for e in edges: 
        G.add_edge(e)

    return G
