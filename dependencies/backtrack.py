
# This module prints the lists projects defined below witht 

### raw datas

project_deps = {
  1   : [2,3],
  5   : [4],
  6   : [1],
  7   : [6, 5, 4],
  8   : [6, 4],
  9   : [6, 5, 8, 7],
  11  : [6, 5, 4, 7],
  10  : [4, 6, 7],
  12  : [6, 7, 11, 10, 8, 1, 9]}

project_deps = {
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

### Adapting and building better structures (for consultation):

# Two structures really count:
# 1. project_deps: dependencies for each projects
# 2. projects: exhaustive list of projects (in project_deps' keys AND values)

for k in project_deps:
    project_deps[k] = set(project_deps[k])

from itertools import chain
flatten = lambda l:list(chain(*l))

projects = set(flatten(flatten([
                [(parent,child) for parent in project_deps[child]] 
                for child in project_deps ])))

independents = projects.difference(set(project_deps))
project_deps.update(dict((k,set()) for k in independents))

### The state of the depth first search algorithm is *project_use*

# This dict holds the project name as the key, and its order as value
# When set to False, this means that the projects is not placed yet in
# the solution.

projects_position=dict((p,False) for p in projects)

### The back track algorithm

# the backtrack algorithm needs an array of no-argument returning
# generators.

# Each function is responsible for a "position" in the solution of
# ordonnanced projects. There is a function for the first position,
# another generator for second position , etc, on to twelveth
# generator. 

# The generator are called vendors because, the vendors repetitively
# tries to "sell" an *appropriate* project i,e. a project which is
# available (not placed yet) and whose dependencies have all been placed.


def appropriate(projects=set(projects_position)):
    placed, unplaced = set(), []
    for p in projects:
        unplaced.append(p) if projects_position[p] is False else placed.add(p)

    return [p for p in unplaced if project_deps[p].issubset(placed)]

vendors = []
for position in range(len(projects)):
    def vendor(position=position): 
        for project in appropriate():
            projects_position[project]=position
            yield project
            projects_position[project]=False

    vendors.append(vendor)

# je comprends pas pourquoi la variable de fonction "vendor.position"
# marche pas alors que l'argument par default position=position
# fonctionne...

### The magic conjoin function copied and pasted from
### Python-x.y.z/Lib/test/test_generators.py
### (lots of good explanation there)

def conjoin(gs):

    values = [None] * len(gs)

    def gen(i, values=values):
        # print values
        if i >= len(gs):
            yield values
        else:
            for values[i] in gs[i]():
                for x in gen(i+1):
                    yield x

    for x in gen(0):
        yield x

## Ok, let's go

g=conjoin(vendors)
print g.next()




