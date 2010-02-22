

from zope.interface import Interface
from zope import schema

class Basil(Interface):

    port = schema.Int(title=u'UDP port', default=8080)
    address = schema.TextLine(title=u'IP address', default=u'127.0.0.1')
    verbosity = schema.Bool(title=u'Verbosity', default=False)
