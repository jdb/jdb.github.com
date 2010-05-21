
from itertools import permutations, groupby
from operator import itemgetter

def deps(G):
    edges = sorted(G.edges)
    d = dict((e,()) for e in G.nodes)
    l = ((parent,ite) for parent,ite in groupby(edges, itemgetter(0)))
    d.update(dict((parent,list(e[1] for e in ite)) for parent, ite in l))
    n = yield
    while True:
        n = yield d[n]

def are_before(L):
    position = dict((key,pos) for pos,key in enumerate(L))

    dep, pivot = yield
    while True:
        dep, pivot = yield all( position[e] < position[pivot] for e in dep)

def is_schedule(dep):
    sol = yield
    while True:
        a = are_before(sol)
        a.next()
        
        sol = yield all(a.send((dep.send(pivot),pivot)) for pivot in sol)

def schedule(G):
    dep = deps(G)
    dep.next()
    i = is_schedule(dep)
    i.next()
    return filter(i.send,permutations(G.nodes))

class Graph(object):
    def __init__(self,nodes=[],edges=[]):
        self.nodes = nodes
        self.edges = edges

    def __repr__(self):
        return "[%s, %s]" % (self.nodes, self.edges)

a, b, c = nodes = 'abc'
G = Graph( nodes, edges=[(a,b), (a,c), (c,b)])

import json
data = json.load(open('projects.json'))

from itertools import chain
edges = list(chain(*[ [ (k,n) for n in v  ]  for k,v in data.iteritems()]))

nodes = list(chain(*data.values()))
nodes.append(data.keys())
nodes=list(set(nodes))

G = Graph(nodes,edges)

s=schedule(G):
print '\n'.join([str(e) for e in s])
with open('toto.result','w'):
    f.write('\n'.join([str(e) for e in s]))
    
