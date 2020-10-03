"""Top-level package for OPICS."""

from opics import libs
from opics.network import Network
from opics.utils import universal_sparam_filereader, LUT_processor, LUT_reader, netlistParser
from opics.globals import c, f

"Register ebeam library"
import opics.libs.ebeam

__author__ = 'Jaspreet Jhoja'
__email__ = 'Jaspreet@siepic.com'
__version__ = '0.1.6'

#initialize OPICS package

name = "opics"

__all__ = ['Network', 'libs', "globals"]


print("OPICS version", __version__)
