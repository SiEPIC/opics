import os
import opics
import importlib

# install to the current working directory
curr_dir = os.getcwd()

# get library catalogue
library_catalogue = opics.libraries.library_catalogue

# get the ebeam library details
library = library_catalogue["ebeam"]

print("installing library")
# download the library using the download library
opics.libraries.download_library(
    library_name=library["name"],
    library_url=library["dl_link"],
    library_path=curr_dir,
)

# reload libraries
importlib.reload(opics.libraries)
print(dir(opics.libraries))

print("removing library")
# remove the library
opics.libraries.remove_library(library["name"])
importlib.reload(opics.libraries)
print(dir(opics.libraries))

print("done")
