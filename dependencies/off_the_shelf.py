

# Topsort in available Python packages
# ====================================

# Topsort is fast, and only returns one of the available
# solutions. This is usually what is needed: as for a labyrinth, the
# problem really is to find the exit, not exhaustively list every
# available way out.


# The topsort package
# -------------------

# This package available on Pypi does not successfully installs at
# this time (*june 2010*), but the algorithm is reproduced here and
# simplified (suppression of the graph cycle detection: make sure,
# there are no circular dependencies in the input graph).

# Prerequisite: *itertools.chain()* can turn a list of list into a
# flat list (sometimes called flatten in other langages)

from itertools import chain

# The funtion is named after Tim Peters who also wrote the super
# efficient timsort_ algorithm. The first step of the algorithm is
# preparing a small data structure: it associates to every nodes its
# number of child: it is the *num_parents* dictionary

# .. _timsort: http://en.wikipedia.org/wiki/Timsort

def tim(deps):

    edges = list(chain(*[
                [(child,parent) for parent in deps[child]] 
                for child in deps ]))

    num_parents = dict([ (k,0) for k in chain(*edges) ])
    for _,child in edges: 
        num_parents[child]+=1 

# Now, here is how the algorithm unfolds: the graph roots are the
# nodes without parents: their num_parents' value is zero. These roots
# are appended to the answer list and suppressed from the num_parents
# dictionary. The iteration operates on this list of nodes without
# parents.

# At each iteration, each current node's children see its parent count
# decremented by one, whenever a children has no more parents, it is
# appended at the end of the answer and suppress from num_parents. At
# each iteration, the num_parents shrinks and the algorithm crunches a
# smaller graph.

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

# Let's try it on a small real world graph in the data package:

# >>> from data import deps
# >>> from pprint import pprint
# >>> pprint(deps)
# {1: [2, 3],
#  5: [4],
#  6: [1],
#  7: [6, 5, 4],
#  8: [6, 4],
#  9: [6, 5, 8, 7],
#  10: [4, 6, 7],
#  11: [6, 5, 4, 7],
#  12: [6, 7, 11, 10, 8, 1, 9]}

# >>> print tim(deps)
# [3, 2, 4, 1, 5, 6, 7, 8, 9, 10, 11, 12] 

# From the Pygraph package
# ------------------------

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

# >>> from data import deps
# >>> print topological_sorting(prepare(deps))
# [4, 5, 3, 2, 1, 6, 8, 7, 11, 10, 9, 12]


# The simplified topsort runs four times faster than the
# implementation in the pygraph packages.

# >>> from timeit import Timer
# >>> print Timer(lambda : tim(deps)).timeit(number=1000)
# 0.0732760429382
# >>> print Timer(lambda : topological_sorting(prepare(deps))
# ...             ).timeit(number=1000)
# 0.333679914474

# The unit is the second, a thousand execution of *tim(deps)* last 7
# hundredth of a second: *tim(deps)* executes in 7 microseconds.
