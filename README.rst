
|build_badge| |license| |pypi|
==============================================

|opics_logo|

Open Photonic Integrated Circuit Simulator (OPICS)
==================================================

**OPICS** is an S-parameter based photonic integrated circuit simulator. To know more,
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

License
~~~~~~~

Copyright © 2022, Jaspreet Jhoja, `MIT License <https://github.com/jaspreetj/opics/blob/master/LICENSE>`__



.. |opics_logo| image:: /docs/_static/images/opics_logo.png

.. |pypi| image:: https://img.shields.io/pypi/v/opics?color=blue
          :target: https://pypi.python.org/pypi/opics
.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
            :target: https://github.com/jaspreetj/opics/blob/master/LICENSE
.. |build_badge| image:: https://github.com/jaspreetj/opics/actions/workflows/CI.yml/badge.svg?branch=master
                 :target: https://github.com/jaspreetj/opics/actions/workflows/CI.yml
