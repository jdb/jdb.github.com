
from itertools import chain

def topsort(projects):

    def prepare(deps):
        no_deps = set(chain(*deps.values())).difference(set(deps))
        
        for p in no_deps:
            projects[p]=[]
    
        return projects

    def candidates(projects, path=[]):
        deps_seen = lambda p: all(d in path for d in projects[p]) 
        return [p for p in projects if p not in path and deps_seen(p)]

    def _topsort(projects, project, path, sorts):
        path = path + [project]
        if len(path)==len(projects):
            sorts.append(path)

        for p in candidates(projects, path):
            _topsort(projects,p , path, sorts)

    projects = prepare(projects)
    sorts = []
    for p in candidates(projects, sorts):
        _topsort(projects, p, [], sorts)

    return sorts

if __name__=="__main__":
    from data import deps
    print topsort(deps)[1]

