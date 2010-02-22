


I wrote the most basic client/server the other day, the client
connects to the server and receives 16 random bytes which it
interprets as four points in the square [-1,1], [-1,1]. 

The server role is just to send 4 random bytes, and we will compare two
methods for the network machinery, the traditional version and an
asynchronous version. The experiment shows that the asynchronous
version is more robust and work under greater constraints.

There are two versions of the server against: a blocking version
written with the :mod:`socket` low level module of the python standard
library and a asynchronous written with the primitives of the Twisted
Python project. Both servers are less than 20 lines.


The client transforms 16 random bytes into 2 points
===================================================

The script executes the well known *client socket dance*:

#. import the :mod:`socket` module so its functions are available to
   the script,

#. create an instance of the :class:`~socket.socket` object,

#. :meth:`~socket.connect` to the address passed as an argument,

#. from now on, :meth:`~socket.recv` or :meth:`~socket.send`
   messages. In our context, the client will receive the 16 random
   bytes and exit.

To transform the 16 bytes into four long integers, we can use the
:meth:`struct.unpack` function which has two parameters the first
one is the bytes to be interpreted, and the second parameter is a
string of letters describing the sequence of types expected in the
bytes: for example, ``I`` means an unsigned integer (4 bytes i.e. from
0 to 2**32-1), ``i`` means an integer (4 bytes i.e. from -2**31 to
2**31-1), or ``f`` which means a floating point number. We will
interpret the 16 bytes as four random integers so our specification
string is ``IIII``. The function, in our context, will return a tuple
of four integers.

The :func:`map` function returns the unpacked list of integers to which
a proportionality factor has been applied to each elements to reduce
the segment to [-1,1].  The list of coordinates is then printed to the
screen::

  #!/usr/bin/env python

  import socket, struct

  s=socket.socket()
  s.connect( ('localhost',5000) )
  message = s.recv(128)

  coords = map( lambda i: i / (2.0)**31 , struct.unpack('LLLL', message[34:50]))

  print( "First point:  A ( %s, %s )" % (coords[0], coords[1]) )
  print( "Second point: B ( %s, %s )" % (coords[2], coords[3]) )


The blocking code with the socket module
========================================

The *socket* version imports the socket module and requests to the
kernel the creation of a socket. The standard system calls of :func:`binding`
to a port and switching the socket to the :func:`listening` state are
performed. As soon as the socket is listening, client connections are
possible. When a client connection is initiated, the kernel puts it in
a queue of the socket kernel object, and the application decides to
process the connection with the *accept* system call which returns a
the connection which supports the receive and send system calls. When
the exchange with the client is finished, the connection can be shut
with the :meth:`close` method to continue processing another client
connection::

  #!/usr/bin/env python
  # random_server_socket.py

  import socket, os
  s=socket.socket()
  s.bind(('',5000))
  s.listen(1)

  while True:
      transport, _ = s.accept()

      transport.send("%s\n\n%s  \n\n%s\n\n" % (
                  "You requested some random bytes:",
                  os.urandom(16), 
                  "You want fries with that?"))

      transport.close()

To test it, open two terminals, in the first one execute the server,
in the other one execute the client::

   ~$ # First terminal : the server
   ~$ python random_server_blocking.py 

   ~$ # Second terminal : the client
   ~$ python random_client.py 
   First point:  A ( -0.602543241252, 0.697890207567 )
   Second point: B ( 0.244899004988, -0.202252262552 )

Ok, the code works as expected. Now, does it work reliably when
hundreds of clients connect at the same time? I will use the bash
``for`` loop to execute a thousand times client. The clients are
executed in parallele without waiting for the termination of the
previous one. In bash, executing *in parallel* (bash says they are
executed as *jobs* in the background) is done by terminating the
command by an *ampersand* sign. To correctly measure the duration of
the whole process, the wait command is used which is a synchronization
primitive (some say a barrier): it returns when all childs are
finished.::

    ~$ # from the client terminal
    ~$ time ( for i in `seq 10000` ; do python random_client.py & done ; wait )


It is obGiven a hundred simultaneous connectionsThe technical merits of the Twisted versions
are obvious while


