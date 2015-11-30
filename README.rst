Poogle
======

|Build Status| |Coverage Status| |Code Health|

Poogle is a Google scraping library and command line utility for Python.

Currently, it only offers the ability to scrape Google search results.
Future functionality will enable retrieving of image links, similar
search queries, and even the ability to retrieve direct answers to
questions you can ask Google.

Installation
------------

To install Poogle, simply:

::

    $ pip install poogle

Usage
-----

Poogle provides both a librry for use in your own Python applications,
as well as a CLI utility for executing search queries in the command
line.

Library
~~~~~~~

google\_search()
^^^^^^^^^^^^^^^^

Using the Poogle search library is pretty straightforward. If you all
you want is a set number of Google search results returned in list
format, use the ``google_search`` function,

.. code:: python

    from poogle import google_search

    results = google_search('Python', results=2)
    for result in results:
        print(result.title)
        print(result.url.as_string() + '\n')

The above code will result in output like the following:

::

    Welcome to Python.org
    https://www.python.org/

    Python (programming language) - Wikipedia, the free encyclopedia
    https://en.wikipedia.org/wiki/Python_(programming_language)

URL's are returned as `Yurl <https://pypi.python.org/pypi/YURL>`__
objects out of the box.

Poogle
^^^^^^

For more advanced usage, you will want to work with the Poogle class
object directly.

.. code:: python

    from poogle import Poogle

    search = Poogle('Python', per_page=10, start_page=1, lazy=True)

    print(search.total_results)  # Estimated number of total search results reported by Google
    print(search.results)

    print(search.next_page())  # Returns an object containing the search results for the next page only
    print(search.results)

The above code will result in output like the following:

::

    159000000

    [<PoogleResult Container: "u'Welcome to Python.org'">, <PoogleResult Container: "u'Python (programming language) - Wikipedia, the free encyclopedia'">, <Poog
    leResult Container: "u'Python | Codecademy'">, <PoogleResult Container: "u'Python tutorial - TutorialsPoint'">, <PoogleResult Container: "u'Python - Reddit'"
    >, <PoogleResult Container: "u'Learn Python The Hard Way'">]

    <PoogleResultsPage Container: Page 2>

    [<PoogleResult Container: "u'Welcome to Python.org'">, <PoogleResult Container: "u'Python (programming language) - Wikipedia, the free encyclopedia'">, <Poog
    leResult Container: "u'Python | Codecademy'">, <PoogleResult Container: "u'Python tutorial - TutorialsPoint'">, <PoogleResult Container: "u'Python - Reddit'"
    >, <PoogleResult Container: "u'Learn Python The Hard Way'">, <PoogleResult Container: "u'Python (programming language) - Wikipedia, the free encyclopedia'">,
     <PoogleResult Container: "u'Python | Codecademy'">, <PoogleResult Container: "u'Python tutorial - TutorialsPoint'">, <PoogleResult Container: "u'Python - Re
    ddit'">, <PoogleResult Container: "u'Learn Python The Hard Way'">, <PoogleResult Container: "u'Learn Python'">, <PoogleResult Container: "u"Newest 'python' Q
    uestions - Stack Overflow"">, <PoogleResult Container: "u'Programming for Everybody (Getting Started with Python ... - Coursera'">, <PoogleResult Container: 
    "u"Python - Programming - Books & Videos - O'Reilly Media"">]

The only major difference between using the google\_search() function
and the Poogle class object at the moment is the ability to fetch more
search result pages after a query has already been executed.

CLI
~~~

For documentation on how to use the Poogle command line utility, run
``poogle --help``.

The only command available at the moment is ``search``,

::

    Usage: poogle search [OPTIONS] QUERY

      Execute a Google search query and display the results

    Options:
      -r, --results INTEGER  The number of search results to retrieve
      --plain                Disables bolding and keyword highlighting
      --help                 Show this message and exit.

Using it is pretty straightfoward. Just be sure to quote your search
query if it contains more than one word.

::

    $ poogle search -r 2 "Python"
    Executing search query for Python

    Welcome to Python.org
    ==============================
    https://www.python.org/

    Python (programming language) - Wikipedia, the free encyclopedia
    ==============================
    https://en.wikipedia.org/wiki/Python_(programming_language)

.. |Build Status| image:: https://travis-ci.org/FujiMakoto/Poogle.svg?branch=master
   :target: https://travis-ci.org/FujiMakoto/Poogle
.. |Coverage Status| image:: https://coveralls.io/repos/FujiMakoto/Poogle/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/FujiMakoto/Poogle?branch=master
.. |Code Health| image:: https://landscape.io/github/FujiMakoto/Poogle/master/landscape.svg?style=flat
   :target: https://landscape.io/github/FujiMakoto/Poogle/master
