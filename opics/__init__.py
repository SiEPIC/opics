"""Top-level package for OPICS."""

from opics import libs
from opics.network import Network
from opics.globals import *

import opics.libs.ebeam

__author__ = 'Jaspreet Jhoja'
__email__ = 'Jaspreet@siepic.com'
__version__ = '0.1.5'

#initialize OPICS package

name = "opics"

__all__ = ['Network', 'libs']

