The Reactor and the Protocols
=============================

How does Twisted do away with the thread in the context of network
connections? Twisted runs a main loop called the reactor which
schedules the callbacks, it is the *coach* of our prior
comparison. **The reactor's scheduling decisions derive directly from
the availability of the data received in the supervised file
descriptors**. The reactor is twofold:

- it is a wrapper around a fast system call which monitors events on
  an array of sockets. Instead of supervising a pool of sockets from
  userland, Twisted delegates_ this hard work to the kernel, via the
  best system call available on the platform: epoll_ on Linux, kqueue
  on BSD, etc.  It is a big bonus for a developer to be able to
  leverage advanced system calls on diverse operating with the same
  code.

  .. _epoll: http://www.kernel.org/doc/man-pages/online/pages/man4/epoll.4.html

  .. _delegates: http://twistedmatrix.com/documents/current/core/howto/choosing-reactor.html

  In a nutshell, these system calls wrapped by the reactor return
  after either a timeout or after the reception of data in one of the
  socket. The system call returns an array of events received, for
  each supervised socket\ [#]_.

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
:obj:`Protocol` associated to the socket [#]_. 

Let's illustrate the reactor by detailing the steps of a single page
download. First, with the sequential :meth:`urlopen` function:

#. urlopen parses the domain name from the URL and resolves it to an
   IP address (this blocking network request is usually avoided by
   the local resolver maintains which keep the domain names in a cache).

#. An HTTP get request for the URL is formatted, a socket toward the
   IP address of the web server is opened and the message is written
   in the socket's file descriptor. :func:`urlopen`, then waits for
   the response from the server and returns the response.
  
Here is the corresponding steps of how Twisted operates with
the :func:`getPage` function:

#. :func:`getPage` parses the input URL, format the HTTP request
   string, and calls:

#. :meth:`reactor.connectTCP` method to stack a socket creation and
   monitoring request to the reactor. The argument of
   :func:`connectTCP` is a host, a port and an instance of the
   :class:`HTTPGetClient` class, deriving from the :class:`Protocol`
   class.

   :meth:`connectTCP` tranparently inserts a DNS request if the
   host is a domain name and not an IP address. This conditions the
   HTTP request to the availability of the IP address, in a non
   blocking manner.

#. :func:`getPage` returns a deferred, a slot that the developer must
   fill with a function which will be executed when the HTTP response
   arrives (more on the deferred in the next :ref:`section
   <deferred>`). This function should expect the HTML body of the
   response as the argument.

   At this point, the flow of request and callbacks has been
   connected, but no actual network request have been made.

#. the reactor is run: for each :obj:`Protocol` object queued: the
   reactor opens a socket, and stores the corresponding file descriptor in
   the :attr:`transport` attribute of the :obj:`Protocol` instance,
   and puts the socket under supervision.

   The reactor calls the :meth:`connectionMade` method of the
   :obj:`Protocol` instance which, in the case of :func:`getPage`
   writes the formatted HTTP request to the :attr:`transport` and
   returns immediately to the reactor loop,

#. when the reactor detects the response bytes in the socket associated
   to :attr:`transport`, it calls the :meth:`dataReceived` method of
   the associated :class:`Protocol` which, in the case of
   :func:`getPage`, is written to parse the HTTP header
   from the HTML body.

   Finally, the :meth:`dataReceived` method for this protocol *fires*
   the developer callback attached to the instance deferred, with the
   HTML string as the parameter.

Here are the two snippets of code corresponding to the description
above. The sequential version comes first, imports are not shown:

.. literalinclude:: reactor/trivial_sequential.py
   :lines: 7-12
   
The version using the reactor:

.. literalinclude:: reactor/trivial_deferred_dontstop.py
   :lines: 9-17

The attention should be drawn on the following
blocking snippet::

  html = urlopen(url))
  print parse(html).xpath( ... )

which becomes, with Twisted primitives::


  def getpage_callback(html):       
      print parse(html).xpath( ... )      

  getPage(url).addCallback(getpage_callback)   

It is indeed bewildering to realize that in Twisted, **the calling
function can not manipulate the result of the request** (after
all, the function is designed to return before the response comes
back). Here is a longer form, often used in Twisted code, which might
seem simpler to read because the callback code is presented after the
request code, *chronologically*::

  d = getPage(url)                  
  def getpage_callback(html):       
      parse(html).xpath( ... )      

  d.addCallback(getpage_callback)   

If you don't like neither these style, stay tuned, you will appreciate
the section :ref:`yield`. Also, there is something unexplained in the last
code snippet: what is the object to which *d* is bound? What does
:func:`getPage` returns if it's not the server reply? you will find
out in the next section on the :doc:`deferreds <deferred>`.

.. [#] the `C10K problem`_ is a reference on server handling
       concurrently ten thousands of clients.

.. _`C10K problem`: http://www.kegel.com/c10k.html

.. [#] Additional abstractions such as the :class:`Factory` interface  are
       left out in this article , they are are described in the official_
       documentation_.

       .. _official: http://twistedmatrix.com/documents/current/core/howto/servers.htm 

       .. _documentation: http://twistedmatrix.com/documents/current/core/howto/clients.html
