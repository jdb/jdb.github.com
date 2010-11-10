
Bash tricks with *find* and *sed*
=================================

This article shows two *bash* tricks with *find* and *sed*. The
problem at hand is computing the number of lines in multiple files
in a directory. There is no subdirectory but the files have a one line
header that should not be part of the count.

- **sed** will help operating on each file to omit the first line,

- **find** will help executing the sed command on every files of a
  directory

Let's create a directory examples with two files:

.. sourcecode:: bash

   ~$ mkdir papa && cd papa
   ~$
   ~$ cat > tata   # Type Ctrl-D to stop editing
   # header
   1
   2
   3
   4
   
   ~$ cat > titi
   # HEAD
   1
   2
   ~$ cat titi
   # HEAD
   1
   2

   

*sed* operates on lines which are specified with an address range:
*first,last*. *sed* counts from one, not zero. The special
character ``$`` means the number of the *last line*. So to operate on
every line except the first one, the address range is ``'2,$'``. Do
not forget the single quotes to prevent bash from messing with the
``$``.

Now that a range is specified, a command must be given: in our case,
it is the command ``p`` (for print).

.. sourcecode:: sh

   ~$ sed '2,$p' tata 
   # header
   1
   1
   2
   2
   3
   3
   4
   4

One more thing, *sed*\ 's default behavior is to print every line it
meets, regardless of what else it may do with it. The ``-n`` option
deactivates this (a.k.a. ``--silent``):

.. sourcecode:: sh

   ~$ sed -n '2,$p' tata 
   1
   2
   3
   4
   ~$ sed --silent '2,$p' tata 
   1
   2
   3
   4

Fine for *sed*, now on to *find*. *find* can be restricted to *find*
only normal files with the option ``-type f``, so that no directory
gets shown. 
 
.. sourcecode:: sh
   
   ~$ find
   .
   ./tata
   ./titi

   ~$ find -type f
   ./tata
   ./titi

Now, for each of these files, the previous *sed* command must be
EXECuted. *find* has the ``-exec`` option whose value is a command to
be executed for each file found. The name of the file found is
inserted e in the command with the ``'{}'`` pattern. A ``;``
*terminator* character must be written at the end of the command so
that *find* knows when the command ends. The semi-colon must be
protected from mangling from bash with either ``\;`` or ``';'``.

.. sourcecode:: sh

   ~$ find -type f -exec echo "I found {}" \;
   I found ./tata
   I found ./titi

Now here is the command to count the lines of every file in the directory,
while omitting the header:

.. sourcecode:: sh

   ~$ find -type f -exec sed -n '2,$p' '{}' \; | wc -l
   6
