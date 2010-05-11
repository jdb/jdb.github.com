#!/usr/bin/env python

"""
This script outputs random shopping karts as could be recorded on
Amazon webservers. Lots of combination of articles and lots of
duplicate shopping karts. Most people buy one article or two articles,
some buys up to 6 articles in one go.
"""

from random import sample, random, shuffle, paretovariate
from optparse import OptionParser
from itertools import chain

def kart_length():
    "Returns a random integer between 1 and 5 (slanted mostly toward 1s and 2s)"
    r=random()
    for t in kart_length.distribution:
        if r<t:
            return kart_length.distribution[t]
kart_length.distribution={0.40:1, 0.75:2, 0.85:3, 0.93:4, 1:5}

def kart_frequency():
    """Returns a random frequency, between 1 (most of the time) and a
    and big int (more rarely)"""
    return int(paretovariate(.5))

def kart():
    """Returns a tuple of frequency for a kart and a random kart"""
    req  = " ".join(sample(words,kart_length()))
    return kart_frequency(), req

words = [w.strip() for w in file('/usr/share/dict/american-english') if "'s" not in w ]
shuffle( words )


p=OptionParser()
p.add_option('-n', type='int',default=20)
p.add_option('-r',action="store_true")
o,a = p.parse_args()

if o.r:
    req = [f*(r,) for f,r in [ kart() for i in xrange(o.n)]]
    req = list(chain(*req))
    shuffle( req )
    for r in req: print r

else:
    for i in xrange(o.n): print "%5s\t%s" %  kart()
        
