The Reactor and the Protocols
=============================

How does Twisted do away with the thread problems in the context of
network connections? Twisted runs a main loop called the reactor which
schedules the callbacks. It is the *coach* of our prior
comparison. **The reactor scheduling decisions derive directly from
the availability of the data received in the supervised file
descriptors**. The reactor is twofold:

- it is a wrapper around a specialised system calls which monitors
  events on an array of sockets. Instead of supervising sockets from
  userland, Twisted delegates_ this hard work to the kernel, via the
  best system call available on the platform: epoll_ on Linux, kqueue
  on BSD, etc

  .. _epoll: http://www.kernel.org/doc/man-pages/online/pages/man4/epoll.4.html

  .. _delegates: http://twistedmatrix.com/documents/current/core/howto/choosing-reactor.html

  In a nutshell, these system calls return after either a timeout or
  after the reception of data in one of the socket. The system call
  returns an array of events received, for each supervised socket\
  [#]_.

  There is a big bonus for a developer to be able to leverage
  efficient advanced system calls on diverse operating with the same
  code. Another bonus is the delegation of concurrent supervision
  of the sockets to the kernel. As the kernel offers to do it, why
  should developers re-invent the wheel in userland?

- the reactor maintains a list of Twisted :class:`Protocol`
  instances. In Twisted, a :class:`Protocol` serves many purposes, and
  in particular it holds a reference to a socket supervised by epoll
  and a method :meth:`dataReceived`. When *epoll* returns and presents
  an array of events for each socket, the reactor dutifully runs the
  :meth:`dataReceived` method of the :obj:`protocol` associated to the
  socket.

The reactor is the runtime hub of the Twisted framework, it handles
the network connections and triggers the processing of the received
data as soon as it arrives by calling specific methods of the
:obj:`Protocol` associated to the socket. Let's focus on a single page
download, first, with the sequential :meth:`urlopen` function:

1. urlopen parses the domain name from the URL and resolves it to an
   IP address (this blocking network request may be avoided if the
   local resolver maintains the domain name in a cache).

2. An HTTP get request for the URL is formatted, a socket toward the
   IP address of the web server is opened and the message is written
   in the socket's file descriptor. :func:`urlopen`, then waits for
   the reply from the server and returns.
  
Here is the corresponding steps of how Twisted operates with
the :func:`getPage` function:

1. :func:`getPage` parses the input URL, format the HTTP request
   string, and uses the :meth:`reactor.connectTCP` method to stack a
   socket creation and monitoring request to the reactor. The argument
   of :func:`connectTCP` are a host, a port and an instance of the
   :class:`HTTPGetClient` class, deriving from the :class:`Protocol`
   class.

   :meth:`connectTCP` tranparently inserts a DNS request if the
   host is a domain name and not an IP address. This conditions the
   HTTP request to the availability of the IP address, in a non
   blocking manner,

2. :func:`getPage` returns a deferred, a slot that the developer must
   fill with a function which will be executed when the HTTP reply
   arrives (more on the deferred in the next :ref:`section
   <deferred>`). This function should expect the HTML body of the
   response as the argument,

3. the reactor is run: for each :obj:`Protocol` object queued: the
   reactor opens a socket, copies the corresponding file descriptor in
   the :attr:`transport` attribute of the :obj:`Protocol` instance,
   and puts the socket under supervision.

   The reactor calls the :meth:`connectionMade` method of the
   :obj:`Protocol` instance which, in the case of :func:`getPage`
   writes the formatted HTTP request to the :attr:`transport` and
   returns immediately to the reactor loop,

4. when the reactor detects the reply bytes in the socket associated
   to :attr:`transport`, it calls the :meth:`dataReceived` method of
   the associated :class:`Protocol` which, in the case of
   :func:`getPage`, is written to parse the HTTP header
   from the HTML body.

   Finally, the :meth:`dataReceived` method for this protocol *fires*
   the developer callback attached to the instance deferred, with the
   HTML as the parameter.

Additional abstractions such as the :class:`Factory` interface are
left out in this article to ease the learning curve , they are are
described in the official_ documentation_. For our third problem,
let's compare two complete versions, one concurrent, one sequential of
a simple script which, 30 times, prints the HTML title of the
*http://twistedmatrix.com* web site.

.. _official: http://twistedmatrix.com/documents/current/core/howto/servers.html

.. _documentation: http://twistedmatrix.com/documents/current/core/howto/clients.html

.. include:: trivial_sequential.py
   :literal:
   
Note that in the following version, the Twisted main loop started by
:meth:`reactor.run` never returns: a line of code below the start of the
reactor loop will never be executed.

.. include:: trivial_deferred_dontstop.py
   :literal:

The attention should be drawn on the following
blocking snippet::

  html = urlopen(url))
  print  parse(html).xpath( ... )

which becomes, with Twisted primitives::


  def getpage_callback(html):       
      parse(html).xpath( ... )      

  getPage(url).addCallback(getpage_callback)   

It is indeed bewildering to realize that in Twisted, **the calling
function can not manipulate the result of the request**. Here is a
longer form, which might seem simpler to read because the callback
code is presented after the request code::

  d = getPage(url)                  
  def getpage_callback(html):       
      parse(html).xpath( ... )      

  d.addCallback(getpage_callback)   

If you don't like neither these style, stay tuned, you will appreciate
the section :ref:`yield`. There is something unexplained in the last
code snippet: what is the object to which *d* is bound? What does
:func:`getPage` returns if it's not the server reply? you will find
out in the next section.

.. [#] the `C10K problem`_ is a reference on server handling
       concurrently ten thousands of clients.

.. _`C10K problem`: http://www.kegel.com/c10k.html

