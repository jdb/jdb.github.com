from pprint import pprint

deps = {
  1   : [2,3],
  5   : [4],
  6   : [1],
  7   : [6, 5, 4],
  8   : [6, 4],
  9   : [6, 5, 8, 7],
  11  : [6, 5, 4, 7],
  10  : [4, 6, 7],
  12  : [6, 7, 11, 10, 8, 1, 9]}

deps = {
  "log"     : ["snmp","json"],
  "psi"     : ["common"],
  "a"       : ["log"],
  "media"   : ["a", "psi", "common"],
  "avc"     : ["a", "common"],
  "ts"      : ["a", "psi", "avc", "media"],
  "rtp"     : ["a", "psi", "common", "media"],
  "mp4"     : ["common", "a", "media"],
  "vod"     : ["a", "media", "rtp", "mp4", "avc", "log", "ts"]
}


def reverse_dependencies(deps):

    from itertools import chain
    flatten = lambda l:list(chain(*l))

    edges = flatten([[(parent,child) for parent in deps[child]] for child in deps])
    nodes = set(flatten(edges))
    return edges, nodes




# def reverse_dependencies(project_deps):

#     from itertools import chain
#     flatten = lambda l:list(chain(*l))

#     edges = flatten([
#             [(parent,child) for parent in project_deps[child]] 
#             for child in project_deps ])

#     edges.sort()

#     provides = dict(
#         (parent,[child for parent,child in group]) 
#         for _,group in groupby(edges, itemgetter(0)))

#     return provides


def topsort(edges, nodes):

    from itertools import chain,groupby
    from operator import itemgetter
    
    edges.sort()
    provides = dict((parent,[child for parent,child in group]) for parent,group in groupby(edges, itemgetter(0)))

    num_parents = dict([ (k,0) for k in nodes ])
    for _,child in edges: 
        num_parents[child]+=1 

    answer = filter(lambda x: num_parents[x] == 0, num_parents)

    for parent in answer:
        del num_parents[parent]
        if provides.has_key(parent):
            for child in provides[parent]:
                num_parents[child]-=1
                if num_parents[child]==0:
                    answer.append(child)

    return answer

def topsort_from_pygraph(edges, nodes):

    from pygraph.algorithms.sorting import topological_sorting
    from pygraph.classes.digraph import digraph

    G = digraph()
    for n in nodes: 
        G.add_node(n)

    for e in edges: 
        G.add_edge(e)

    return topological_sorting(G)


if __name__=="__main__":
    edges, nodes = reverse_dependencies(deps)
    print topsort (edges, nodes)
    # print topsort_from_pygraph (edges, nodes)

