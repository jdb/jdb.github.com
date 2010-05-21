

Class method and static method
==============================

A class method is a method bound to a class and not an instance:

>>> import time
>>> class MyFantasticClass(object):
...     def interrupt(self):
...         print 'Or a woman !'
>>> m = MyFantasticClass()
>>> m.interrupt()
Or a woman !

The *time* function is an instance function, it receives self as an
argument. This is not adapted here, because for the function to be
used, an instance must be created: even though the *time* method does
not make use of the instance, it is passed as an input parameter to
the function.

**How to define the *interrupt* method so that it is called directly on
the class without having to create an instance?** 

Example : ::

     MyFantasticClass.interrupt()

Answer: use a *class method* or even better a *static method*. The
class method:

>>> class MyFantasticClass(object):
...     @classmethod
...     def interrupt( klass):
...         print 'Or a woman !'
>>> MyFantasticClass.interrupt()
Or a woman !

For the user of the class, it dos not make much of a difference if the
function is bound to the class or just static, but it changes the
definition. The class method is passed the class as the first argument
(and not *self*, the instance). In our example, the best choice is a
*static* method since the function uses neither the instance nor the
class:

>>> class MyFantasticClass(object):
...     @staticmethod
...     def interrupt():
...         print 'Or a woman !'
>>> MyFantasticClass.interrupt()
Or a woman !

