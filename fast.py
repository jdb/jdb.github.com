The last section of this article explains how to get better
performance with Python, when the problem is CPU bound.

Fast number crunching in Python
-------------------------------

Python code is usually transformed on execution into byte compiled
code, which is then interpreted by the Python virtual machine which is
a software directly understood by the processor. For some demanding
computing uses, this extra step is suboptimal. There are many ways to
use more efficiently the CPU from Python:

1. Use a better design, a better algorithm for the problem at hand,
   which reduces the complexity of the computing. This usually implies
   thinking harder about the problem, sometimes making radical changes
   to the project, or having experience or  deep knowledge of math,

2. Use *all* the CPUs, by splitting the running application into
   multiple processes.

   In C, using threads would suffice, but not in Python where all the
   threads run on the same core of one CPU. The Global Interpreter
   Lock (GIL) is a mutex in the Python virtual machine that prevents
   concurrency on multiprocessor or multi-core machines.
   
3. Write the CPU hungry parts in C, and integrate the C function to a
   Python program which handles the rest such as command line options,
   or graphical user interface in other contexts.

4. Use a faster Python. Two projects, at least, aim at compiling
   Python code into binary code directly edible by a processor.

   These projects, Pypy, among other goals, want to skip the intermediate
   Python virtual machine step by producing, for the repeatedly
   executed bytecode, the native machine code, on the fly. It is
   called a just-in-time compiler.

The solutions will be presented in reverse order, which means
approximately correponds to the easiest solution first, and the math
solutions in last.

Using a faster Python
~~~~~~~~~~~~~~~~~~~~~

Integrating parts in C
~~~~~~~~~~~~~~~~~~~~~~

Using several processes to use more core/processors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since Python can not run threads on multiple core/processors, let's
handle the computations to the OS which is capable of using all the
cores of many processors. Python offers the multithreading module
which presents an interface quite similar to the interface of the
threading module:

- **Process*: this object is instantiated with a callable (a function)
  for the keyword argument *target*, and a list of argument for the
  keyword argument *args*.

- process.\ **start()**: forks and executes a Python virtual machines
  which will run the function

- process.\ **join()**: waits for the child process to terminate. If
  you forget to call this method. The child which have terminated will
  completely disappear from your system. They will turn into **zombie
  process** (that is technically the name for processes which have
  terminated but which are still waiting to have their return value
  read).

  For example::

    p=Process(target=lambda:1+1)
    p.start()
    p.join()

Process do not return a result, and by default, they shares no
data. They shares the stdin, stdout and stderr file descriptors and
they report a return code to the parent processwhich is too small to
contain an approximation of Pi. Special objects must be instantiated
to easily communicate each subprocess Pi approximation to the parent
process. Here we will use the **Queue** object from the *multiprocessing*
module:

- queue.\ **put**, queue.\ **get** : respectively pushes and pops an
  elements in and out tof the queue, making sure the queue is safe
  when multiple process read and writes it concurrently.

- queue.\ **size**: returns the size of the queue. It cannot be
  guaranteed correct in the general case but if is clear that the
  queue cannot evolve, when for example, all producers and consumers
  terminated, the size is stable.

Each subprocess will write its approximation in the queue and
terminate, once every child has terminated, the queue is read into a
list of elements returned to the caller, which can compute the
mean of the approximation to aggregate, or *reduce* the list.

.. sourcecode:: sh

   ~$ test_it ./procedural.py 
   An approximation of Pi is : 3.145 
      duration: 0.47 seconds
   An approximation of Pi is : 3.140716 
      duration: 2.44 seconds
   An approximation of Pi is : 3.1421848 
      duration: 11.09 seconds
   
   ~$ test_it ./processes.py 
   An approximation of Pi with 4 process: 39276.5
      duration: 0.26 seconds
   An approximation of Pi with 4 process: 196420.75
      duration: 1.09 seconds
   An approximation of Pi with 4 process: 981729.25
      duration: 5.73 seconds


The version with four system processes, is exactly twice faster: it
uses both core of the laptop.


A less dumb algorithm for approximating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
