from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

tag_reference = dependency_os("tag")

tagc_body = Struct("tagdata",
    reflexive("tag references", tag_reference, 200),
    SIZE=12,
    )


def get():
    return tagc_def

tagc_def = TagDef("tagc",
    blam_header('tagc'),
    tagc_body,

    ext=".tag_collection", endian=">"
    )