
from data import deps
from itertools import chain,groupby
from operator import itemgetter

def prepare(dependencies):

    edges = list(chain(*[
                [(parent,child) for parent in dependencies[child]] 
                for child in dependencies ]))
    edges.sort()

    provides = dict(
        (parent,[child for parent,child in group]) 
        for parent, group in groupby(edges, itemgetter(0)))

    nodes = set(chain(*edges))
    num_parents = dict([ (k,0) for k in nodes ])
    for _,child in edges: 
        num_parents[child]+=1 

    return provides, num_parents


def topsort(provides, num_parents):

    answer = filter(lambda x: num_parents[x] == 0, num_parents)

    for parent in answer:
        del num_parents[parent]
        if provides.has_key(parent):
            for child in provides[parent]:
                num_parents[child]-=1
                if num_parents[child]==0:
                    answer.append(child)

    return answer


print topsort(*prepare(deps))




