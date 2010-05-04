
Problem introduction
====================

Say Amazon wants an updated list of the most frequent shopping
karts. From the data set of last year, they need a data structure
which holds a list of the combination of articles name sorted by the
frequency of the number of sell of this product.

Articles names are long, 50 characters, and we want to be able to keep
track of four billion shopping karts. Can we keep the data structure
running on an average PC?

What are the available structures:

- A *heap* would allows fast sorted insertion, and fast retrieval of
  the n largest, but would not offer fast access. No fast access means
  no fast update to an existing node, nor fast pop of an element prior
  to an eventual fast push you could push it fastly.

  For the initialization from files, of the data structure with
  terabytes of article occurrence, the heap allows fast merges, maybe.

- A *dictionary* {article:frequency} would not sorted. But fast to
  update, and insert.

  The latest *ordered dictionary* which was introduced in Python3.2 is
  ordered by the insertion not by a key. It is useless in our context.

- A *bisect* allows fast ordered insertion but no fast access
  update. To allow fast updates, the position for a hash must be set
  in dictionary hash to position

  The *array* is an efficient way to store data of the same type and
  size which can be combined with bisect.

- An SQL database is adapted for a big indexed tables from hash to
  names, on disk.

What about collisions?

The initialization of the list
==============================

Naive way
---------

::

   from collections import defaultdict
   from operator import itemgetter

   d=defaultdict(int)

   [ d[kart]+=1 for kart in file('karts.txt') ]
   karts = sorted( d.iteritems(), key=itemgetter(1) )[-10**6:]

This version is not going to work out because the PC memory will soon
be exhausted. A sort requires all the strings to be available in
memory. The data set weighs *50 bytes * 10 billion karts recorded =
512 Gb*.

By hand: complete control and memory greedy
-------------------------------------------

The average complexity is noted with regard to memory.

1. the long list of articles names is transformed into a list of
   hashes. *O(1)*. A good size for the hash is one order of magnitude
   more than hte size of the dataset. 10**13 is represented on 45
   bytes, let's say 64 to keep memory words aligned..

2. the list of hashes is aggregated: in a pass, the duplicates are
   suppressed by creating a dictionary of hash:frequency. The worst
   case: no duplicate, still counts *8 bytes * 10 billion = 80 Gb*.
   It is safe to assume that lots of articles are bought in mass
   (Iphone, Harry Potter), 90% may be duplicates.

3. the list of hash/frequencies is sorted on the frequency. O(m), m<<n

4. the million most popular hash is kept.

5. a dictionary of a million entry: hash/articles names is recomputed
   from the file. *1 million hash * 8 bytes + 1 million names * 50
   bytes + one million frequency * 4 byte = approximately 60 Mb*

While it was impossible to study a dataset of half a terabyte easily,
it is much more feasible to study the data set of the most popular
karts.

Note:collision possible. Need to list the articles names with the same
hash to find the correct one.

Also the data set could be simplified with lemmatization, and with
ordering of the article in a kart.

Step 5 implies a second pass on the raw data set, could be avoided if
a disk index (the file positions of each karts) where kept in the
memory data structure.


With a relational database: powerful and simple to express
----------------------------------------------------------

create table
insert into names,id
update hash
select id,hash,sum(hashes) as sum  group by hashes sort by sum into temp
-- aggregate list of ids and find collision
select names join temp on id order by sum


With Unix: hacking pipes with the GNU core-utils
------------------------------------------------

sort -R | uniq -c | sort -k 1,1 -r | sed '1000000q;s///'

# sort --merge

Always up to date: fast invariant insertions
============================================

New client shop every day: in this second phase, we will want the list
to be always updated. The frequent insertions of new articles and the
updates of the number of sell should be fast, and 'invariant': keep
the list sorted.

freq = {hash:array('i', [frequency, sorted position, file position])}
freqsorted = array('i', [frequency])
fileposorted = array('i', [file positions])
How does the recod of a new kart updates the database::

  # compute the new hash
  h = hash(kart)

  # compute the new frequency
  freq[hash(kart)][0]+=1

  # checks if the list must be modified
  def is_inplace (sorted_position, frequency):
      return sort[sorted_position-1][1] =< frequency =< sort[sorted_position+1][1]

  si n'est pas a a place, on le pop, et on l'y replace tres vite avec
  bisect.

.. class:: IPopular( dict )

   .. method:: popular_articles(n, with_frequency=False)

      Returns a list a popular articles, first article is the most
      popular.

.. class:: IDynamicPopular( dict )

   .. method:: incr( article_name, incr=1 )


.. class:: SortedDict( dict )

   .. method:: __init__(dicts,files)

      [SortedDict]   

      [files]

   .. method:: _merge

   .. method:: _push_articles()

      Takes a filename with one article per line and update the
      frequencies accordingly.

   .. method:: merge( sorteddict) 

      In the initi

   .. method:: __init__( dict{article:frequency}, 
                         hashes2names_filename,
                         hashes_frequency_filename)

      it creates :

      - a persisted sqlite table of hashes to names, names indexed by
        hashes
      
      - a dict of hashes to position in the ordered list

      - a list of hashes, frequency sorted by the 

   .. method:: repr()

      returns a dict of article names and frequency

   .. method:: merge (sorteddict) 

   .. method:: __setitem__

   .. method:: __getitem__ 

   .. method:: __incr_hash( hash, incr=1 )

   .. method:: __get_hash( article )

   .. method:: __get_name( hash )

   .. method:: __nlargest_hashes( hash )

   .. method:: nlargest_articles(with_frequency=False)

   .. method:: incr_frequency( article_name, incr=1 )

