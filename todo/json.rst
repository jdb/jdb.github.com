

======
 JSON
======


For the configuration files, we weighted three well known data
formats: INI, JSON and XML. We chose JSON_ [#]_. Google and Yahoo
have blessed the format by making their public webservices available
via JSON which de facto makes JSON a not completely dumb format. Libraries for
most languages are available at http://www.json.org .

.. _JSON: http://www.json.org/fatfree.html


- JSON is brief:
  *<tag>foo<tag/><tag>bar</tag><tag>fubar</tag>* becomes
  *["foo","bar","fubar"]*

  JSON is not perfect as "it" "always" "requires" "quotes" "around"
  "strings", also linefeeds are not a separator, so commas are also
  explicitly required as separators. Quotes in string must be escaped
  with a '\\'.

- JSON expresses complex structures in terms of dictionaries, lists
  and combinations of those, which are native datatypes in most modern
  languages.

  In XML, learn the many concepts, select a complex library, choose
  between DOM, SAX, Xpath or a language specific API, choose between
  attribute oriented or data oriented schema, and troll endlessly
  about everyone of your choice with colleagues about the "right" way
  to do it.

- INI files are simple to read, but difficult to edit programmatically
  (think about keeping the comments, keeping section order).

  INI files only advantage is the simplicity for humans eyes, there is
  virtually no learning step with this format while it is possible to
  be confused by a sequence of nested JSON brackets and braces.

- INI format is less supported by languages. In python


.. [#] http://en.wikipedia.org/wiki/JSON
