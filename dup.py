def naive(liste):
    seen = []
    for i in liste:
        if i not in seen:
            seen.append(i)
    return seen


def buggy_naive(liste, nodups = []):
    [nodups.append(i) for i in liste if i not in nodups]
    return nodups


def usort(liste):
  l = sorted(liste)
  nodups = [l[0]]
  for e in l:
       if e != nodups[-1]:
           nodups.append(e)
  return nodups


def keep_last(liste):
   d = dict((v,i) for (i,v) in enumerate(liste))
   return sorted( d.keys(), key = d.get )


def keep_first(liste):
   d = dict( (v,i) for (i,v) in enumerate(reversed(liste)))
   return sorted( d.keys(), key = d.get, reverse=True)


def dico(l):
    return dict((i,None) for i in l).keys()


from collections import OrderedDict
def odict(l):
    return OrderedDict((i,None) for i in l).keys()


from random import randint

def randlist(size, freq, almost_sorted=False):
    """Returns a list of int according to three parameters: 

    - size of the list: either *short* or *long*, 
    - whether there are *few* or *tons* of duplicates in the list,
    - either the list is completely shuffled of almost sorted.
    """

    d = {'short': 10, 'long': 5000, 'few': 3, 'tons': 0.5}
    l = [randint(1, int( d[size]*d[freq])) for _ in range(d[size])]
    if almost_sorted:
        l.sort()
        for _ in range(int(d[size] * 0.01)):
            n, m = randint(0, d[size]-1), randint(0, d[size]-1)
            l[n], l[m] = l[m], l[n]
    return l


def make_lists():
    for size in 'short', 'long':
        for freq in 'few', 'tons':
            for almost_sorted in True, False:
                yield (size, freq, almost_sorted), randlist(size, 
                                                            freq, 
                                                            almost_sorted)

if __name__ == '__main__':
    from timeit import Timer

    for fun in [ naive, usort, keep_last, keep_first, set, dico, odict]:
        for (s, f, a), l in make_lists():
            print("%s\t%s\t%s\t%s\t%s" % (fun, s, f, a ,
                                   Timer(lambda:fun(l)).timeit(number=100)))

