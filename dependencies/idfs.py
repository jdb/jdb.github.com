

# Recursive generator
# ===================

# I can hear you say: "I know what generator means and I know what
# recursive means, but I do not see what the combination means". 

# This is a function which returns an object with a *next()* method,
# and each calls to next yields a new element of the graph, depth
# search first. Depending on the candidate function, every nodes, or
# only the leaf nodes or really any user defined list can be yielded


from pprint import pprint
from itertools import chain

# The prepare() and candidates() functions are similar than in the
# previous module_.

# .. _module: :doc:`off_the_shelf`

def prepare(deps):
    
    for p in set(chain(*deps.values())) - set(deps.keys()):
        deps[p]=[]

    for p in deps: 
        deps[p]=set(deps[p])

    return set(deps), deps


def candidates(projects, deps, path):
    return filter( lambda p: deps[p] <= path, projects - path)


# The difficulty is that a generator returns an object with a next()
# method and not a solution, 

# There will be one Python generator for each parent node, nested in
# the tree hierarchy, the function yields whenever the stop condition
# matches.

def idfs(projects, deps):

    class Path(list):
        def __setitem__(self,key,item):
            self.append(item)

    def _idfs(path = Path()):
        if len(path) == len(deps):
            yield path[:]
        else:
            for path[0] in candidates(projects, deps, set(path)):
                for winner in _idfs():
                    yield winner
                path.pop()
                
    return _idfs()

# What's with this private class in the function, which only override
# setitem?


if __name__=="__main__":
    from data import deps
    from timeit import Timer

    # pprint(list(idfs(projects, deps)))

    print Timer(lambda : list(idfs(*prepare(deps)))
                ).timeit(number=1000)
