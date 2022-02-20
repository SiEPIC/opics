import yaml as _yaml
import pathlib as _pathlib
from importlib import util as _util
from .catalogue_mgmt import download_library, remove_library

_curr_dir = _pathlib.Path(__file__).parent.resolve()

# read yaml file for available libraries in the catalogue
with open(_curr_dir / "catalogue.yaml", "r") as _stream:
    library_catalogue = _yaml.safe_load(_stream)


def _module_from_file(module_name, file_path):
    spec = _util.spec_from_file_location(module_name, file_path)
    module = _util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _import_external_libraries(library_catalogue):
    installed_libraries = []

    for each_lib in library_catalogue.keys():
        if library_catalogue[each_lib]["installed"]:
            installed_libraries.append(each_lib)
            globals()[each_lib] = _module_from_file(
                each_lib,
                f"{library_catalogue[each_lib]['library_path']}/{library_catalogue[each_lib]['name']}/__init__.py",
            )

    return installed_libraries


installed_libraries = _import_external_libraries(library_catalogue)

__all__ = [
    "download_library",
    "remove_library",
]
