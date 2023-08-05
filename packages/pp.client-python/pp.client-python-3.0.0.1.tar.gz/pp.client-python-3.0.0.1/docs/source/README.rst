pp.client-python
================

Produce & Publish bindings for Python.

The ``pp.client-python`` bindings can be used to communicate
with the Produce & Publish server ``pp.server`` for generating
PDF from Python applications .

Requirements
------------

- Python 3.7 or higher

Source code
-----------

https://bitbucket.org/ajung/pp.client-python

Bug tracker
-----------

https://bitbucket.org/ajung/pp.client-python/issues

Documentation
-------------

https://pythonhosted.org/pp.client-python

API
---

pdf API 
+++++++

The ``pdf`` API supports the conversion of HTML/XML to PDF
through the following PDFconverters:

- PDFreactor 
- PrinceXML 
- Speedata Publisher 
- Vivliostyle Formatter 
- PagedJS
- Typeset.sh
- Weasyprint
- Antennahouse

The PDF conversion process is based on the "CSS Paged Media" approach
where the input documents (XML or HTML) are styled using CSS only.

The ``pdf`` API of ``pp.client-python`` expects that the input
file and all related assets (images, stylesheets, font files etc.)
are placed within a working directory. The input file must be named 
``index.html``.

Using the commandline frontend::

    $ ../bin/pp-pdf  --help
    usage: pp-pdf [-h] [-f princexml] [-o] [-a] [-s http://localhost:6543]
                  [-t None] [-c] [-v]
                  source_directory [cmd_options]

    positional arguments:
      source_directory      Source directory containing content and assets to be
                            converted
      cmd_options           []

    optional arguments:
      -h, --help            show this help message and exit
      -f prince, --converter prince
                            PDF converter to be used (prince, pdfreactor, publisher)
      -o , --output         Write result ZIP to given .zip filename
      -s http://localhost:6543, --server-url http://localhost:6543
                            URL of Produce & Publish server)
      -t None, --authorization-token None
                            Authorization token for P&P server
      -v, --verbose         Verbose mode


The same functionality is available to any Python application through the 
``pdf()`` API of the ``pp.client-python`` module::


    from pp.client.python.pdf import pdf

    def pdf(source_directory,
            converter='prince', 
            output='',
            cmd_options='',
            server_url='http://localhost:8000',
            authorization_token=None,
            verbose=False):

Support
-------

Support for Produce & Publish Server and components is currently only available
on a project basis.

License
-------
``pp.client-python`` is published under the GNU Public License V2 (GPL 2).

Contact
-------

| Andreas Jung/ZOPYX 
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com
