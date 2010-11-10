
Bash tricks with *find* and *sed*
=================================

This article shows two bash tricks with find and with sed. The problem
at hand is computing the number of the lines in multiple files in a
directory. There is no subdirectory but the files have a one line
header that does not count.

- **sed** will help operating on each files to omit the first lines

- **find** will help executing the sed lines on every files of a directory

Let's create a directory examples with two files:

.. sourcecode:: bash

   ~$ mkdir papa && cd papa
   ~$ cat > tata   # type Ctrl-d to stop editing
   # header
   1
   2
   3
   4
   ~$ cat > titi
   # HEAD
   1
   2
   ~$ cat titi
   # HEAD
   1
   2

   

*sed* operates on lines which are specified with an address range:
*first,last*. There is a comma between the first line number and the
*second line number, sed counts from one, not zero. The special
*character ``$`` means the number of the last line. So to operate on
*every line except the first one, the address range is ``'2,$'``. Do
*not forget the single quotes to prevent bash from messing with the
*``$``.

Now that a range is specified, a command must be given: in our case,
it is the command ``p`` (for print).

.. sourcecode:: bash

   ~$ sed '2,$p' tata 
   # head
   1
   1
   2
   2
   3
   3

One more thing, *sed*\ 's default behavior is to print every line it
meets, regardless of what it does with it. The ``-n`` option
deactivates this (a.k.a ``--silent``).

.. sourcecode:: bash

   ~$ sed -n '2,$p' tata 
   1
   2
   3
   ~$ sed --silent '2,$p' tata 
   1
   2
   3

Fine for *sed*, now on to *find*. find can be restricted to *find*
only normal files with the option ``-type f``, so that no directory
gets shown. 
 
.. sourcecode:: bash
   
   ~$ find
   .
   ./tata
   ./titi

   ~$ find -type f
   ./tata
   ./titi

Now, for each of these file, the previous sed command must be
EXECuted. *find* has the ``-exec`` option whose value is a command to
be executed for each file found. The name of the file found is
inserted in the command with the ``'{}'`` pattern. A ``;``
*terminator* character must be written at the end of the command so
that *find* knows when the command ends. The semi-colon must be
protected from mangling from bash with either ``\;`` or ``';'``.

.. sourcecode:: bash

   ~$ find -type f -exec echo "I found {}" \;
   I found ./tata
   I found ./titi

Now here is the command to count the line of every file in the directory,
while omitting the header:

.. sourcecode:: bash

   ~$ find -type f -exec sed -n '2,$p' '{}' \; | wc -l
   9
