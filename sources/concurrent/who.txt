
Who runs Twisted?
=================

Twisted is run by a dedicated team of roughly 20 developers and is
funded by individuals and companies organised as a foundation_. The
developers are higly available by means of IRC (*#twisted*), `mailing
list`_, and `bug tracker`_. Their `quality standards`_ are high and
sophisticated. 

Twisted is used in production_ in the datacenters of the
Canonical or Fluendo corporations, for example, but also as the IO
engine of the Zope Toolkit or as an embedded webserver by smaller
applications such as the desktop edition of the Moinmoin wiki.

.. _foundation: http://twistedmatrix.com/trac/wiki/TwistedSoftwareFoundation

.. _`mailing list`: http://twistedmatrix.com/cgi-bin/mailman/listinfo/twisted-python

.. _`bug tracker`: http://twistedmatrix.com/trac/report/1

.. _`quality standards`: http://twistedmatrix.com/trac/wiki/ContributingToTwistedLabs

.. _production: http://twistedmatrix.com/trac/wiki/SuccessStories


Is Twisted perfect?
===================

Depends on what you means by perfect :) There are tough points that
might need to be considered before using Twisted. For example, Twisted
requires to design the application around the core powerful concepts
of the framework: incremental project migration to Twisted is not
straightforward. Second point, Twisted does not, at this time, make a
seamless use of multicore: the application must be designed to use
multiple processes. Twisted only recently shown a processpool_ and
multicore *mapreduce* proof-of-concept.

.. _processpool: https://launchpad.net/ampoule


These serie of articles is available in pdf_.

.. _pdf: http://jdb.github.com/static/concurrent.pdf
