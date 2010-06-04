
from itertools import chain

projects = {
  1   : [2,3],
  5   : [4],
  6   : [1],
  7   : [6, 5, 4],
  8   : [6, 4],
  9   : [6, 5, 8, 7],
  11  : [6, 5, 4, 7],
  10  : [4, 6, 7],
  12  : [6, 7, 11, 10, 8, 1, 9]}


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

print topsort(projects)[1]

