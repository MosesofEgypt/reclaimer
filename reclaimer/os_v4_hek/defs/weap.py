#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.weap import *
from .obje import *
from .item import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(2))
    )

weap_body = desc_variant(weap_body,
    ("obje_attrs", obje_attrs)
    )

def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">", tag_cls=WeapTag
    )
