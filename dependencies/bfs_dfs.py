
from pprint import pprint
from itertools import chain


def prepare(deps):
    """Returns the set of projects, the input dictionnary is also
    updated with project without dependencies"""
    
    for p in set(chain(*deps.values())) - set(deps.keys()):
        deps[p]=[]

    for p in deps: 
        deps[p]=set(deps[p])

    return set(deps), deps


def candidates(projects, deps, path):
    "Returns project not in the path, but whose dependencies are"
    return filter( lambda p: deps[p] <= path, projects - path)


def dfs(projects, deps):
    "Returns a sorted list of the dependencies - depth first traversal"
    def _dfs(projects, deps, path, acc):
        candids = candidates(projects, deps, set(path))
        if candids:
            for c in candids:
                _dfs(projects, deps, path + [c], acc)
        else:
            acc.append(path)
    acc = []
    _dfs(projects, deps, [], acc)
    return acc

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

def idfs(projects, deps, path=[]):
    if len(path) == len(deps):
        yield path[:]
    else:
        for c in candidates(projects, deps, set(path)):
            path.append(c)
            for winner in idfs(projects, deps, path):
                yield winner
            path.pop()


def bfs(projects, deps, paths=[[]]):
    "Returns a sorted list of the dependencies - breadth first traversal"
    cands_lists= [ candidates(projects, deps, set(p)) for p in paths]
    if any(cands_lists):
        newpaths=[]
        for p,cands in zip(paths,cands_lists): 
            newpaths.extend([p+[c] for c in cands])
        return bfs(projects, deps, newpaths)
    else: 
        return paths


if __name__=="__main__":
    from data import deps
    from timeit import Timer

    projects, deps = prepare(deps)

    # pprint(dfs(projects, deps))
    # pprint(bfs(projects, deps))
    #for l in idfs(projects, deps):
    #    print l

    print Timer(lambda : dfs(projects,deps)).timeit(number=1000)
    # print Timer(lambda : bfs(projects,deps)).timeit(number=1000)
    print Timer(lambda : list(idfs(projects,deps))
               ).timeit(number=1000)


