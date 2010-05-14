The :mod:`itertools` provides super powerful, and efficient
primitives written in C for manipulating generators. See this
resolution of the `Queen problem`_ (in Python3):

.. _`Queen problem`: http://en.wikipedia.org/wiki/Eight_queens_puzzle

>>> from itertools import permutations as chessboards
>>> size=8; queens = range(size)
>>> safe = lambda rows: size == len({rows[col]+col for col in queens})\
...                          == len({rows[col]-col for col in queens})
>>> list(filter(safe, chessboards(queens)))[:2]
[(0, 4, 7, 5, 2, 6, 1, 3), (0, 5, 7, 2, 6, 3, 1, 4)]

Also the regression tests for Python include an efficient
resolution of the `Knight problem`_ in pure Python. See the
``Python-x.y.z/Lib/test/test_generators.py`` in the python
sources.

.. _`Knight problem`: http://www.imsc.res.in/Computer/lg/110/kapil.html
