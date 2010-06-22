
# inverses a adjacency matrix: turns a require dict into a provide
# dict. Not needed here as the end result is reversed...
    
edges.sort(itemgetter(0))
provides = dict(
    (parent,[child for parent,child in group]) 
    for parent, group in groupby(edges, itemgetter(0)))
