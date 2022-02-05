|last_commit| |license| |pypi|
==============================================

|opics_logo|

Open Photonic Integrated Circuit Simulator (OPICS)
==================================================

**OPICS** aims at providing open and reliable solutions for designing
and simulating silicon photonic integrated circuits and systems. To know more,
refer to OPICS  `Documentation <https://siepic.github.io/opics>`__

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

The package is available through ``pip``:

.. code:: python

   pip install opics

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


.. |image1| image:: https://img.shields.io/pypi/v/opics.svg
   :target: https://pypi.python.org/pypi/opics
.. |image2| image:: https://img.shields.io/travis/siepic/opics.svg
   :target: https://travis-ci.com/mustafacc/opics
.. |Documentation Status| image:: https://readthedocs.org/projects/opics/badge/?version=latest
   :target: https://opics.readthedocs.io/en/latest/?badge=latest

.. |opics_logo| image:: /docs/_static/opics_logo.png

.. |last_commit| image:: https://badgen.net/github/last-commit/siepic/opics
.. |pypi| image:: https://badgen.net/pypi/v/opics?maxAge=2592000
.. |license| image:: https://badgen.net/pypi/license/opics
