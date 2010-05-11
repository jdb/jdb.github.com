
surprising imports
==================

If ``from a import b ; print b.c`` works, shouldn't 
``import a ; print a.b.c`` work too? Not necessarily, here is why.

To use an object in Python, the objects needs to be present in the
namespace. To create a new entry in a module namespace, it is possible
to either define the functions and classes *or import* them from a
package or a module. Packages are also namespaces, **the objects which
are included in the current namespace when the package is imported are
the objects which are defined and imported by the :mod:`__init__.py`**
module of the package. If the :mod:`__init__.py` is empty for a
package, importing the package does not make the modules in the
package available.

Rule of thumb, if you don't want surprises always import modules,
because with packages, it depends on the :mod:`__init__` package.

Here is an example

.. sourcecode:: sh

   ~$ tree package
   package
   |-- blabi.py
   |-- __init__.py
   `-- shbonz
       |-- __init__.py
       `-- shekel.py
   

:mod:`package` and :mod:`shbonz` are packages (:mod:`shbonz` is a
*subpackage*), which means they are filesystem directories with a file
named __init__.py in it. Those can be empty files.

.. sourcecode:: sh
      
   ~$ cat package/__init__.py package/shbonz/__init__.py
   ~$
   ~$  # the __init__.py are just empty files

:mod:`blabi` et :mod:`shekel` are modules, they contain classes,
functions and constants. Fore example, :mod:`shekel` defines a
constant :obj:`pi`

.. sourcecode:: sh
   
   ~$ cat package/shbonz/shekel.py
   pi=3.14

As the *__init__.py* files are empty, they do not import :obj:`pi`, it
is not available when importing the packages:

.. sourcecode:: sh

   ~$ python -c 'import package;  print package.shbonz.shekel.pi'
   Traceback (most recent call last):
   AttributeError: 'module' object has no attribute 'shbonz'
   
   ~$ python -c 'from package import shbonz;  print shbonz.shekel.pi'
   Traceback (most recent call last):
   AttributeError: 'module' object has no attribute 'shekel'
   
The *module*, and not its parent packages must be imported, for the
constant to be available:

   ~$ python -c 'from package.shbonz import shekel; print shekel.pi'
   3.14

Now if the package's :mod:`__init__` module import the constant, it
will be available:

.. sourcecode:: sh
   
   ~$ echo "import shbonz" > package/__init__.py
   ~$ echo "import shekel" > package/shbonz/__init__.py
   ~$ python -c 'import package;print package.shbonz.shekel.pi'
   3.14
   
http://effbot.org/zone/import-confusion.htm
