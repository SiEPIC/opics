"""Top-level package for OPICS."""

__author__ = """Jaspreet Jhoja"""
__email__ = 'Jaspreet@siepic.com'
__version__ = '0.1.5'

#initialize OPICS package

name = "opics"
from opics.version_ import __version__
__all__ = ['library', 'network', 'data']
from . import *
