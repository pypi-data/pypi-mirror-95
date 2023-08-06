================
scottbrian-utils
================

Intro
=====

This is a collection of generally useful functions for use with any application.

1. The diag_msg function allows you to print a message with the time and caller sequence added for you.
2. The FileCatalog item allows you to map file names to their paths.
3. The @time_box decorator allows you to print start, stop, and execution times.
4. The print_flower_box_msg function allows you to print text in a flower box (i.e., surrounded by asterisks).


With **diag_msg** you can print messages with the time and caller info added automatically.

:Example: print a diagnostic message (<input> appears as the module name when run from the console)

>>> from scottbrian_utils.diag_msg import diag_msg
>>> diag_msg('this is a diagnostic message')
16:20:05.909260 <input>:1 this is a diagnostic message


With **FileCatalog**, you can code your application with file names and retrieve their paths at run time
from a catalog. This allows you to use different catalogs for the same set of files, such as one catalog for production
and another for testing. Here's as example:

>>> from scottbrian_utils.file_catalog import FileCatalog
>>> prod_cat = FileCatalog({'file1': Path('/prod_files/file1.csv')})
>>> print(prod_cat.get_path('file1'))
/prod_files/file1.csv

>>> test_cat = FileCatalog({'file1': Path('/test_files/test_file1.csv')})
>>> print(test_cat.get_path('file1'))
/test_files/test_file1.csv


With **@time_box**, you can decorate a function to be sandwiched between start
time and end time messages like this:

>>> from scottbrian_utils.time_hdr import time_box

>>> @time_box
... def func2() -> None:
...      print('2 * 3 =', 2*3)

>>> func2()
<BLANKLINE>
**********************************************
* Starting func2 on Mon Jun 29 2020 18:22:50 *
**********************************************
2 * 3 = 6
<BLANKLINE>
********************************************
* Ending func2 on Mon Jun 29 2020 18:22:51 *
* Elapsed time: 0:00:00.001204             *
********************************************



.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://readthedocs.org/projects/pip/badge/?version=stable
    :target: https://pip.pypa.io/en/stable/?badge=stable
    :alt: Documentation Status


Installation
============

Linux:

``pip install scottbrian-utils``


Development setup
=================

See tox.ini

Release History
===============

* 1.0.0
    * Initial release

* 1.0.1
    * Added doc link to setup.py
    * Added version number to __init__.py
    * Added code in setup.py to get version number from __init__.py
    * Added licence to setup.py classifiers

* 1.1.0
    * Added FileCatalog

* 1.2.0
    * Added diag_msg

Meta
====

Scott Tuttle

Distributed under the MIT license. See ``LICENSE`` for more information.


Contributing
============

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


