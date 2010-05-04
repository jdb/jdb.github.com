
Ok, c'est bon, j'ai trouve mon erreur debile. C'est plus simple que
prevu, en fait, __getattr__ est la specialement pour te renvoyer un
callable seulement quand l'attribut n'a pas ete trouve.

>>> class toto(object):
...     def method(self,string):
...         return string
... 
...     def missing_method(self,*args):
...         return "OMG! you called a method which does not exists with these args: %s" % args
... 
...     def __getattr__(self, *args):
...         return self.missing_method
... 
>>> t = toto()
>>> print t.method("Hello World")
Hello World
>>> print t.unexisting_method("knock knock knock")
OMG! you called a method which does not exists with these args: knock knock knock
