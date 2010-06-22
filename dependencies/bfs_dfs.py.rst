
Graph traversal
===============

::

  from pprint import pprint
  from itertools import chain
  
**prepare()** function adapts the input dictionary of dependencies
into the almost same dictionary: except that 1. the values are set
and that also that 2. the project with no dependencies are also set
as keys with an empty set as the value

::

  def prepare(deps):
      
      for p in set(chain(*deps.values())) - set(deps.keys()):
          deps[p]=[]
  
      for p in deps: 
          deps[p]=set(deps[p])
  
      return set(deps), deps
  
**candidates()** returns the list of nodes which are not in path yet
and whose dependencies are already in the list

::

  def candidates(projects, deps, path):
      return filter( lambda p: deps[p] <= path, projects - path)
  
  
Depth first search
------------------

::

  def dfs(projects, deps):
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
  
Breadth first search
--------------------

::

  def bfs(projects, deps, paths=[[]]):
      cands_lists= [ candidates(projects, deps, set(p)) for p in paths]
      if any(cands_lists):
          newpaths=[]
          for p,cands in zip(paths,cands_lists): 
              newpaths.extend([p+[c] for c in cands])
          return bfs(projects, deps, newpaths)
      else: 
          return paths
  
Testing our algorithms
----------------------

::

  if __name__=="__main__":
      from data import deps
      from timeit import Timer
  
      projects, deps = prepare(deps)
  
      # pprint(dfs(projects, deps))
      # pprint(bfs(projects, deps))
  
      # print Timer(lambda : dfs(projects,deps)).timeit(number=1000)
      # print Timer(lambda : bfs(projects,deps)).timeit(number=1000)
  
  
