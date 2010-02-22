
Does programming style really matters
-------------------------------------

Speed of execution is not so much relevant as the tests only
shows less than 10% difference. Speed and ease of development
also counts in the real world there is limited amount of time in
a day and a limited mental space for algorithm and constraints

If in the same amount of time and effort you can do more, you can
maybe add new features, or reduce confusion with documentation,
detect bugs early with more testing. With the ease of development
comes the possibility to tackle more difficult problems such as
scalability, corner cases, etc.

For speed and ease of development, readability, re-usability,
robustness, ease of testing and maintenance and fitness for
distribution also matters:

Readability depends on the number of symbols, on the number of source
line of code, on straightforward names and on experience and personal
preferences. For instance, ``len( list )`` is easier to read than
``sum( ( 1 for element in list ) )``. Code is written once or twice by
one developper, but it may be read several times by the developer and
other over the course of month. The procedural code is easier to read
than the smart functional code.

Re-usability is the ability to use some code with known input and
ouput without really having to care to what is inside. Here the
functional code offers two easy to re-use functions:

.. function:: points( number of points) -> list of random points

.. function:: in_circle( a point ) -> true or false 

They are simple to rewrite in our example but if you compare to the
procedural code, it is difficult to extract any independent
element. You have to debug the whole loop entirely while in the
functional code, when every building block is correct, the composition
of the building blocks is also correct which allows you to debug each
building block independently.

The fitness for distribution and scalability is maybe the most
interesting problem. The whole for loop will be executed on the same
server.

