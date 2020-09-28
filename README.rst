|last_commit| |license| |pypi| |Documentation Status|
==============================================

|opics_logo|

Open Photonic Integrated Circuit Simulator (OPICS)
==================================================

**OPICS** aims at providing open and reliable solutions for designing
and simulating silicon photonic integrated circuits and systems. To know more,
refer to `Documentation <https://siepic.github.io/opics>`__

Requirements
~~~~~~~~~~~~

The package is written using ``numpy`` and ``scipy`` packages, and is
compatible with ``python3``. All requirements to run the package can be
obtained by running the following commands in shell:

.. code:: shell

   pip install numpy
   pip install scipy

or

::

   pip install -r requirements.txt

Package setup
~~~~~~~~~~~~~

Currently, the package is not available through ``pip``. Invoke the
following block of code before importing OPICS package in a
script/notebook:

.. code:: python

   import sys
   sys.path.append('path/to/opics')

After this, you should be able to access and import OPICS package using
the

.. code:: python

   import opics

command in python.

Examples
~~~~~~~~

A few circuit examples have been provided in the ``examples`` directory.

Citing
~~~~~~

``OPICS`` is written by Jaspreet Jhoja. You can cite the package as

::

   @misc{jhoja-2020-opics,
     author = {Jaspreet Jhoja},
     title = {OPICS: An Open Photonic Integrated Circuit Solver},
     year = {2020},
     publisher = {GitHub},
     journal = {GitHub repository},
     howpublished = {\url{https://github.com/SiEPIC-Kits/OPICS}}
   }

|dog_gif|

.. |image1| image:: https://img.shields.io/pypi/v/opics.svg
   :target: https://pypi.python.org/pypi/opics
.. |image2| image:: https://img.shields.io/travis/siepic/opics.svg
   :target: https://travis-ci.com/mustafacc/opics
.. |Documentation Status| image:: https://readthedocs.org/projects/opics/badge/?version=latest
   :target: https://opics.readthedocs.io/en/latest/?badge=latest

.. |opics_logo| image:: /docs/_static/opics_logo.png

.. |dog_gif| image:: https://media.giphy.com/media/Y0G6gc8CJu1ynAZ1nr/giphy.gif
.. |last_commit| image:: https://badgen.net/github/last-commit/siepic/opics
.. |pypi| image:: https://badgen.net/pypi/v/opics
.. |license| image:: https://badgen.net/pypi/license/opics
