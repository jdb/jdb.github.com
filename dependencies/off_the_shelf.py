

# Topsort in available packages
# =============================

# Topsort are fast functions which finds only one of the available
# solutions. This is usually wha is needed: as for a labyrinth, the
# problem really to find the exit, not exhaustively list every
# available way out.


# The topsort package
# -------------------

# This package is not installable at this time (June 2010), but the
# algorithm is reproduced here and simplified. The simplification
# consist of suppressing the graph cycle detection (make sure, there
# are no circular dependencies in the input graph).


# Prerequisite: chain() can turn a list of list into a flat list,
# sometimes called flatten in other langages
from itertools import chain

def tims(deps):


# The first step of the algorithm is preparing a small data structure:
# it  associates to every nodes its number of
# child: it is the *num_parents* dictionary

    edges = list(chain(*[
                [(child,parent) for parent in deps[child]] 
                for child in deps ]))

    num_parents = dict([ (k,0) for k in chain(*edges) ])
    for _,child in edges: 
        num_parents[child]+=1 

# Here is how the algorithm unfolds:
#
# The graph roots are the nodes without parents, their num_parents'
# value is zero. These roots are appended to the answer list and
# suppressed from the num_parents dictionary. The iteration begins on
# the list of nodes without parents.

# At each iteration, each current node's children see its parent count
# decremented by one, whenever a children has no more parents, it is
# appended at the end of the answer and suppress from num_parents.

# At each iteration, the num_parents shrinks and the algorithm
# crunches a smaller graph.

    answer = filter(lambda x: num_parents[x] == 0, num_parents)

    for parent in answer:
        del num_parents[parent]
        if deps.has_key(parent):
            for child in deps[parent]:
                num_parents[child] -= 1
                if num_parents[child] == 0:
                    answer.append(child)

# Topsort actually computes the path from the most dependent tasks to
# the most independent task, we'll want to reverse the list to suits
# our context.

    return list(reversed(answer))

from data import deps
print tims(deps)



# From the Pygraph package
# =======================

# The algorithm is import imported form the *sorting* algorithm, and
# operates on digraphs.

from pygraph.algorithms.sorting import topological_sorting
from pygraph.classes.digraph import digraph

# *prepare()* takes a dictionary of dependencies and prepares a list of
# edges and a set of nodes and returns an adapted digraph:

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

print topological_sorting(prepare(deps))

# Performances
# ============

from timeit import Timer
print Timer(lambda : tims(deps)).timeit(number=1000)

