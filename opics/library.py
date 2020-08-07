from pathlib import Path, PurePath


parent_datadir = Path(str(Path(__file__).parent) + "/data/")

#adding ebeam library
ebeam_datadir = Path(str(parent_datadir) + '/ebeam/')
ebeam_components = {}

#library list
libraries = {"ebeam": {"components":ebeam_components, "datafolder":ebeam_datadir}}
