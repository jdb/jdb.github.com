from pprint import pprint
from itertools import chain

def tims(provides):

    edges = list(chain(*[
                [(child,parent) for parent in deps[child]] 
                for child in deps ]))

    nodes = set(chain(*edges))

    # inverses a adjacency matrix: turns a require dict into a provide
    # dict. Not needed here as the end result is reversed...
    
    # edges.sort(itemgetter(0))
    # provides = dict(
    #     (parent,[child for parent,child in group]) 
    #     for parent, group in groupby(edges, itemgetter(0)))

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

    return list(reversed(answer))

if __name__=="__main__":
    from data import deps
    from timeit import Timer
    # print tims(deps)

    print Timer(lambda : tims(deps)).timeit(number=1000)
