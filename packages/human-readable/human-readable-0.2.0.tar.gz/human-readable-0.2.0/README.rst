Human Readable
==============

|Status| |PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |Status| image:: https://badgen.net/badge/status/alpha/d8624d
   :target: https://badgen.net/badge/status/alpha/d8624d
   :alt: Status
.. |PyPI| image:: https://img.shields.io/pypi/v/human-readable.svg
   :target: https://pypi.org/project/human-readable/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/human-readable
   :target: https://pypi.org/project/human-readable
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/human-readable
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/human-readable/latest.svg?label=Read%20the%20Docs
   :target: https://human-readable.readthedocs.io/
   :alt: Read the documentation at https://human-readable.readthedocs.io/
.. |Tests| image:: https://github.com/staticdev/human-readable/workflows/Tests/badge.svg
   :target: https://github.com/staticdev/human-readable/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/staticdev/human-readable/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/staticdev/human-readable
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* File size humanization.
* List humanization.


Requirements
------------

* It works in Python 3.7+.


Installation
------------

You can install *Human Readable* via pip_ from PyPI_:

.. code:: console

   $ pip install human-readable


Usage
-----

Import the lib with:

.. code-block:: python

   import human_readable


File size humanization:

.. code-block:: python

   human_readable.file_size(1000000)
   "1.0 MB"

   human_readable.file_size(1000000, binary=True)
   "976.6 KiB"

   human_readable.file_size(1000000, gnu=True)
   "976.6K"


Lists humanization:

.. code-block:: python

   human_readable.listing(["Alpha", "Bravo"], ",")
   "Alpha, Bravo"

   human_readable.listing(["Alpha", "Bravo", "Charlie"], ";", "or")
   "Alpha; Bravo or Charlie"


Numbers humanization:

.. code-block:: python

   human_readable.int_comma(12345)
   "12,345"

   human_readable.int_word(123455913)
   "123.5 million"

   human_readable.int_word(12345591313)
   "12.3 billion"

   human_readable.ap_number(4)
   "four"

   human_readable.ap_number(41)
   "41"


Floating point number humanization:

.. code-block:: python

   human_readable.fractional(1.5)
   "1 1/2"

   human_readable.fractional(0.3)
   "3/10"


Scientific notation:

.. code-block:: python

   human_readable.scientific_notation(1000)
   "1.00 x 10³"

   human_readable.scientific_notation(5781651000, precision=4)
   "5.7817 x 10⁹"


Click here for more examples and detailed usage_.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT_ license,
*Human Readable* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This lib is based on original humanize_ with some added features such as listing, improved naming, documentation, some more testing, bug fixes and better Portuguese support.

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.


.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _humanize: https://github.com/jmoiron/humanize
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/staticdev/human-readable/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _usage: https://human-readable.readthedocs.io/en/latest/usage.html
