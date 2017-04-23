from ...hek.defs.meta_descs import *
from . import *

modules = locals()
meta_cases = dict(meta_cases)
fcc_map = dict(**fcc_map)
fccs.remove("gelc")

for fcc in fccs:
    meta_cases[fcc_map.get(fcc, fcc)] = modules[fcc].get().descriptor[1]

# not for export
del modules
