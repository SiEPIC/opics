"""Top-level package for OPICS."""

from opics import libraries
from opics.network import Network
from opics.utils import netlistParser
from opics.globals import C, F

__author__ = "Jaspreet Jhoja"
__email__ = "jj@alumni.ubc.ca"
__version__ = "0.3.1"

# initialize OPICS package

name = "opics"

__all__ = [
    "Network",
    "libraries",
    "globals",
    "netlistParser",
    "C",
    "F",
]

print(
    r"""
   ____  ____  _______________
  / __ \/ __ \/  _/ ____/ ___/
 / / / / /_/ // // /    \__ \
/ /_/ / ____// // /___ ___/ /
\____/_/   /___/\____//____/
"""
)
print("OPICS version", __version__)
