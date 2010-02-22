
Generating forms from schemas
=============================

introduction
------------

.. context

Web forms are a very common way to request input from the user. In a
blog application for example, a form to add an article contains the
title, date and body fields with the 'Ok' button at the bottom, which
submit the details of the article back to the server. Because an
article needs to be *written*, *modified* and finally *published and
read*, the blog application needs three Web pages with few
differences: the page to add, to display and to edit: both the edit
and add pages are forms.

.. what the issue is:  where grok really helps in the area of forms

Given a definition of the article object, Grok simplifies the work of
the developer by generating the three pages. The definition of an
application object is defined in Grok thanks to a **schema**. It is
defined by the developer via the powerful ``zope.schema`` and
``zope.interface`` packages, and these, as the name suggests, are part
of the Zope Toolkit.

Validation of user input is also a hot topic of forms. Grok leverage
the schema's attribute properties to indicate to the user a field
input error like a typo in an email, in a date, etc.

.. Widgets represent form fields in a way which guides and facilitates
.. user input. For example, a date field can be represented with a
.. tooltip calendar widget, an article body can be presented for editing
.. with a rich text editor widget. Grok can add various widgets to a Web
.. application.

.. an overview of the article ( overview of the table of content)

Part one of this article introduces schemas manipulation and
validation, by hand, on the command line. Many kinds of objects can be
validated with schemas completely independently of the Grok framework,
we will validate dictionaries, json objects, named tuples and classes.

Part two will show how it is integrated with Grok, and how to generate
Web forms which can protect the application from unexpected data and
which can effectively notice the user that a form was incorrectly
filled.

.. prerequisite for the article

To follow this howto, it is easier if you have completed followed the
Grok tutorial.  You need to be familiar with the *buildout*,
*setup.py*, *app.py*.


Schema describes the application objects
----------------------------------------

Several data types
~~~~~~~~~~~~~~~~~~

Take the example of a blog application, the application will process
articles which can be described::

    from zope.interface import Interface
    from zope.schema import *
    
    class Article( Interface ):

        title = TextLine(
                    description="The title of the article",
		    minlength=20,
		    maxlentgh=200)
	
	synopsis = Text(
	           default="type one or two sentence describing the article")

	body = Text(default="type the body of the character here")

	author_email = TextLine()

Another example is a configuration file can be described with the
following schema::

    class IGlobals(Interface):
        udp_address = TextLine( maxlength=15 )
	udp_port = Int( max=65535 )
	min_connection = Int()
	max_connection = Int()

    class Section( Interface ):
        name = TextLine( maxlength=256 )
	match = TextLine()
	filename = TextLine()

Here we validate values before creating an object which respect the
schema and the fields datatypes::

    class globals(object):
    
        def __init__(udp_address='127.0.0.1', udp_port=0):
	    self.udp_address = udp_address
	    self.port = udp_port

    IGlobals.udp_address.validate( '192.168.0.1' )
    IGlobals.udp_port.validate( 512 )

    # Ok: the values passed,
    g=globals( '192.168.0.1', 512 )

Incorrect values raise an exception::

  TooBig
  WrongType

Constraints and Invariants are expressive validators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fields data types are usually quite generic while a field in an
application is more constrained to its specific use: for instance, a
*TextLine* might hold an IP address and should not be an email
address. The ``constraint`` parameter given to field at the creation
of the field can be set with a callable (a function) which is called
by the *validate()* method of the field. The function should accept
the value for the field as an input and should return *True* or
*False* depending on the correctness of the value with regard to the
use of the field

For instance, take the IP address, you see how I was so smart put the
limit of 15 characters to embed the specificity of the nature of an IP
address. This does not help us very far, an there is a better way to
be express the specificity of the type of object.

The schema fields have the constraint parameters which can point to a
function which must raise an exception whenever a field is found
invalid. The schema can be extended::

    class IGlobals(Interface):
        udp_address = TextLine( constraint=validate_ipaddress )
	udp_port = Int( max=65535 )

	def validate_ipaddress( str ):
	    return true if re.compile('.*').match( str) else False

Same goes for the email address::

    class IArticle( Interface ):

	author_email = TextLine( constraint=validate_email )

	def validate_email( str ):
	    return true if re.compile( '.*' ).match( str ) else False

Invariants are functions which have access to every fields values and
can validate constraints which apply to several related fields

How Grok uses the schema
------------------------

what and where to declare it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fields and widgets
~~~~~~~~~~~~~~~~~~

Conclusion 
-----------

Extend schema with custom fields, validate composited objects.

Powerful Widgets

Ajax forms

Unsolved difficulties
