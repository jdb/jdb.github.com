
Porting the current documentation to Sphinx
===========================================

The mail documentation chunk is composed of three rst files: two
listings and one sizeable tutorial::

  doc/projects/mail
  |-- examples
  |   `-- index.rst
  |-- index.rst
  `-- tutorial
      `-- smtpclient
          `-- smtpclient.rst

They refere to five Python examples:

- an IMAP4 client
- two SMTP clients (one tutorial, and one example with support for TLS)
- two SMTP servers (unpublished)

The transformation is correct and the corrections are minor:
- in the rst files: superfluous blank lines and paragraph length (lines
  sometimes too short, sometimes too long)
- in html: nothing visible after rendering, nothing outrageous in the
  html sources (what should I have spotted in particular?)

mail/index.rst and mail/examples/index.rst
------------------------------------------

Suppressed 2/3 blank lines under the title, suppressed 4/5 blank lines
under the toctree

Filled the paragraphs of the listing.


mail/tutorial/smtpclient/smtpclient.rst
---------------------------------------

**Problem which show in the html**:

#. missing a space before an underline or preformatted
   string (unpredictable)

#. always extra space between
  
   - an underline or preformatted string, or a link: ("\:ref:\`link` ,")
   - a dot, comma, parenthesis, colon, apostrophy
#. sometimes both two previous at the same time

- "use by <code>twistd</code>.</p>" was transformed in rst in "use
  by``twistd`` ." which is incorrect rst: the space before the dot
  should be before ``twistd``.  "by``twistd`` ." is passed un
  transformed to the html.
- same problem with "imports``twisted.application.service`` ,"
- same pb with "the``Application`` function"
- "*application service* ." space before the dot which shows
- "new*application service*": missing space prevents underline,
- "name``application`` ." missing space prevents preformatted,
- "pass to ``twistd`` ." extra space before the dot (not in the xhtml
  source)
- "of a``.tac``" missing space: passed untransformed to the html
- "using the``twistd``" 
- "is another*application service*"
- "a*protocol class*"
- "a *protocol instance* ."
- ":download:`smtpclient-4.tac` , we"

I stopped counting at "SMTP Client 5"


blank lines are added like crazy:
- suppressed 5/6 blank lines after the page title
- suppressed 2/3 blank lines after the introduction title
- suppressed 3/4 blank lines between the introduction paragraphs
- ...

Also, *paragraph fill* is sometimes inconsistent, lines might be too
short, some others are too long while the xhtml was OK





Enhancing the content
=====================

SMTP client tutorial
--------------------

Each of the different iterations of the smtpclient are explained in
its own restructured text sections, which are subsections (h3 in
lore/xhtml) of the introduction (h2 in lore/xhtml). There is only one
section in the article: the introduction. The iterations title is the
number of the iteration.

I propose that each iterations sections gets promoted at the same
level of the introduction and get a section title meaningful with
regard to the feature added by this iteration.

Acknowledging a comment in the article source, a conclusion/wrap up
section can be added.

tac or tap? which is the prefered way of writing an application? links
towards tac or tap are helpful.

SMTP server tutorial
--------------------

In the Twisted sources, ``twisted/doc/mail/tutorial/smtpserver/``
contains the different iterations of an smtpserver but no article
explaining the steps which prevents the smtpserver to be reachable
from the generated documentation.

Interaction and layout
======================

Articles and links to source codes
----------------------------------

Several tutorial in the Twisted doumentation provide snippets of
formatted code inline as well as a link to the source code in
integrality. Clicking on the link results in the download the source
file in the directory configured for downloaded files and offers to
launch the external default file viewer configured on the host.

In my opinon, when clicking on a link pointing to a code, the reader
would prefer avoiding having to download the file first, especially
when there are 11 iterations of the script which will clutter the
*download* directory. The link to a code could lead to a formatted and
colorized html page. Instead of writing :download:`smtpclient-1.tac`,
it is possible to write :doc:`smtpclient-1` which points to a
boilerplate ``smtpclient-1.rst`` file which should contain::

   A meaningful title
   ==================

   .. literalinclude:: smtpclient-1.tac

Ideally, there is a Sphinx keyword simplifying the boilerplate,
something such as :src:`smtpclient-1.tac`, which would result in the
formatted/colorized HTML page of the code source. Ideally, there would
be a small link, wget friendly, in the top right of the page, to view
the raw text source.

To use the source codes with one's favorite editor, a tarball per
subproject could be provided with links to it on the project page and
on each page which mention a code included in the tarball.

Layout of the documents
-----------------------

I propose that the five documents are all listed directly on the first
page of the Twisted Mail documentation. The first indirection which
lists two categories is not really needed as the two category are not
very populated and overlap somehow. One page listing the five
documents can still differentiate the *tutorial* and *example*
category, if needed.

