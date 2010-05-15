

Missing method
==============

I have heard that in Ruby there is a conventional method which is
automatically called when a method is missing. You can put code there
which will be executed whenever you call a missing method. In Python,
there is a similar mechanism exist, but there is one more
indirection. If a missing method is called, *self.__getattr__** will
be called and it needs to return a callable which itself will be
called in place of the missing method.

>>> class toto(object):
...     def method(self,string):
...         return string
... 
...     def missing_method(self,*args):
...         return "Warning: method does not exists (you gave %s)" % args
... 
...     def __getattr__(self, *args):
...         return self.missing_method
... 

>>> t = toto()
>>> print t.method("Hello World")
Hello World
>>> print t.unexisting_method("knock knock knock")
Warning: method does not exists (you gave knock knock knock)


*Jean Daniel Browne, 10 May 2010*
