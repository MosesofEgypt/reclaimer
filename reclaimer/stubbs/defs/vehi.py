#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
THIS DEFINITION IS INCORRECT BECAUSE THE UNIT STRUCTURE IS DIFFERENT THAN HALO'S
'''
from ...hek.defs.vehi import *
from .obje import *
from .unit import *
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(1))
    )

vehi_attrs = desc_variant(vehi_attrs,
    ("type", SEnum16('type', *vehicle_types))
    )

vehi_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    vehi_attrs,
    SIZE=1008,
    )

#def get():
#    return vehi_def
del get

vehi_def = TagDef("vehi",
    blam_header_stubbs('vehi'),
    vehi_body,

    ext=".vehicle", endian=">", tag_cls=ObjeTag
    )
