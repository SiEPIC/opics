"""Top-level package for OPICS."""

from opics import libraries
from opics.network import Network
from opics.utils import universal_sparam_filereader
from opics.utils import LUT_processor
from opics.utils import LUT_reader
from opics.utils import netlistParser
from opics.globals import c, f

__author__ = "Jaspreet Jhoja"
__email__ = "jj@alumni.ubc.ca"
__version__ = "0.1.9"

# initialize OPICS package

name = "opics"

__all__ = [
    "Network",
    "libraries",
    "globals",
    "LUT_processor",
    "LUT_reader",
    "netlistParser",
    "universal_sparam_filereader",
    "c",
    "f",
]


print("OPICS version", __version__)
