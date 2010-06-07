from pprint import pprint
from itertools import chain

def prepare(deps):
    no_deps = set(chain(*deps.values())).difference(set(deps))
        
    for p in no_deps:
        deps[p]=[]
    
    return deps

def candidates(path, projects):
    deps_seen = lambda p: all(d in path for d in projects[p]) 
    return [p for p in projects if p not in path and deps_seen(p)]


def bfs(projects):

    def _bfs(projects, sorts, level):
        new_sorts=[]
        for s in sorts:
            nexts = candidates(s, projects)
            if nexts:
                new_sorts.extend([s + [c] for c in nexts])

    # Python is particularly unpure concerning functions and objects,
    # and particularly unpure concerning xpressions and side effects.

        if level==len(projects)-1:
            return new_sorts
        
        return _bfs(projects, new_sorts, level+1)

    projects = prepare(projects)
    sorts = [[]]
    return _bfs(projects, sorts, 0)
    
if __name__=="__main__":
    from data import deps
    pprint(bfs(deps))
