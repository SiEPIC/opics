=====
OPICS
=====



.. image:: https://img.shields.io/pypi/v/opics.svg
        :target: https://pypi.python.org/pypi/opics

.. image:: https://img.shields.io/travis/siepic/opics.svg
        :target: https://travis-ci.com/mustafacc/opics

.. image:: https://readthedocs.org/projects/opics/badge/?version=latest
        :target: https://opics.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/siepic/opics/shield.svg
     :target: https://pyup.io/repos/github/mustafacc/opics/
     :alt: Updates



.. image:: docs/opics_logo.svg
		:target: https://www.aperturephotonics.com/

# Open Photonic Integrated Circuit Simulator (OPICS)

<img src="/icons/opics_logo.svg" title="opics" alt="opics">


**OPICS** aims at providing open and reliable solutions for designing and simulating silicon photonic integrated circuits and systems. 

### Requirements
The package is written using `numpy` and `scipy` packages, and is compatible with `python3`. All requirements to run the package can be obtained by running the following commands in shell:
```shell
pip install numpy
pip install scipy
```

or

```
pip install -r requirements.txt
```

### Package setup
Currently, the package is not available through `pip`. Invoke the following block of code before importing OPICS package in a script/notebook:

```python
import sys
sys.path.append('path/to/opics')
```

After this, you should be able to access and import OPICS package using the 
```python 
import opics
```
command in python. 

### Examples

A few circuit examples have been provided in the `examples` directory.

### Citing

`OPICS` is written by Jaspreet Jhoja. You can cite the package as

```
@misc{jhoja-2020-opics,
  author = {Jaspreet Jhoja},
  title = {OPICS: An Open Photonic Integrated Circuit Solver},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/SiEPIC-Kits/OPICS}}
}
```
<img src="https://media.giphy.com/media/Y0G6gc8CJu1ynAZ1nr/giphy.gif">
