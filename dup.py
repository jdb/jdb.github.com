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
