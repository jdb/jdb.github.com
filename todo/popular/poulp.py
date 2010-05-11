
from zop.interface import Interface, implements

class IPopular( Interface ):
   def popular_articles(n, with_frequency=False):
       """Returns a sorted list of popular articles, first article:
       most popular.

       Returns a list of pairs of (articles, frequency) when
       with_frequency is True."""

class IDynamicPopular( Interface )
   def incr( article_name, incr=1 ):
       "Update the frequency of an article"

import hashlib


class Article():

    __storm_table_ = article

    primary_key, 

    hash

    frequency

    

class Popular():
    
    implements([IPopular])
    
    def __call__(self, n, with_frequency=False):
        return self.freq.iteritems()
    
    def incr(self, incr=1):
        pass

    def __init__( self, fn):
        self.freq  = []   # hash, freq, last line number
                          # self.hash2names = sqlite via storm
        for l in fn:
            self.incr(l)

    def _hash( article ):
        h=hashlib.sha1()
        h.update(article)
        return int(h.hexdigest[:16],16)

    def incr( article , id):
        h=self._hash( article)
        self.freq[h]= (self.freq[h][0]+1,id) if self.freq.hasattr(h) else (1,id)



from operator import getattr
sorted(Popular(file('articles.txt')), key=itemgetter(1))
