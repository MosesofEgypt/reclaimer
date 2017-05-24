from .mod2 import *
from .objs.mode import ModeTag

def get():
    return mode_def

permutation = Struct('permutation',
    ascii_str32("name"),
    BBool32('flags',
        'cannot be chosen randomly'
        ),
    Pad(28),

    dyn_senum16('superlow geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('low geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('medium geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('high geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('superhigh geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    Pad(2),
    SIZE=88
    )

part = Struct('part',
    BBool32('flags',
        'stripped',
        'ZONER',
        ),
    Pad(1),
    dyn_senum8('shader index',
        DYN_NAME_PATH="tagdata.shaders.shaders_array[DYN_I].shader.filepath"),
    SInt8('previous part index'),
    SInt8('next part index'),

    BSInt16('centroid primary node'),
    BSInt16('centroid secondary node'),
    BFloat('centroid primary weight'),
    BFloat('centroid secondary weight'),

    QStruct('centroid translation', INCLUDE=xyz_float),
    Pad(12),

    #reflexive("compressed vertices", compressed_vertex_union, 65535),
    #reflexive("triangles", triangle_union, 65535),
    reflexive("compressed vertices", fast_compressed_vertex, 65535),
    reflexive("triangles", triangle, 65535),

    #Pad(36),
    Struct("model meta info",
        FlUEnum32("index type",  # name is a guess.  always 1?
            ("uncompressed", 1),
            ),
        FlUInt32("index count"),
        FlUInt32("indices offset"),
        FlUInt32("indices reflexive offset"),

        FlUEnum32("vertex type",  # name is a guess
            ("uncompressed", 4),
            ("compressed",   5),
            ),
        FlUInt32("vertex count"),
        FlUInt32("unknown"),  # always 0?
        FlUInt32("vertices offset"),
        FlUInt32("vertices reflexive offset"),
        VISIBLE=False
        ),

    SIZE=104
    )


node = Struct('node',
    ascii_str32("name"),
    dyn_senum16('next sibling node', DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16('first child node', DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16('parent node', DYN_NAME_PATH="..[DYN_I].name"),
    Pad(2),

    QStruct('translation', INCLUDE=xyz_float),
    QStruct('rotation', INCLUDE=ijkw_float),
    BFloat('distance from parent'),
    Pad(32),

    # xbox specific values
    LFloat('unknown', ENDIAN='<', DEFAULT=1.0),
    QStruct("rot_jj_kk", GUI_NAME="[1-2j^2-2k^2]   2[ij+kw]   2[ik-jw]",
        INCLUDE=ijk_float, ENDIAN='<'),
    QStruct("rot_kk_ii", GUI_NAME="2[ij-kw]   [1-2k^2-2i^2]   2[jk+iw]",
        INCLUDE=ijk_float, ENDIAN='<'),
    QStruct("rot_ii_jj", GUI_NAME="2[ik+jw]   2[jk-iw]   [1-2i^2-2j^2]",
        INCLUDE=ijk_float, ENDIAN='<'),
    QStruct('translation to root', INCLUDE=xyz_float, ENDIAN='<'),
    SIZE=156,
    )

region = Struct('region',
    ascii_str32("name"),
    Pad(32),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH=".name"),
    SIZE=76
    )

geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", part, 32),
    SIZE=48
    )


mode_body = Struct('tagdata',
    BBool32('flags',
        'blend shared normals',
        'parts have local nodes',
        'ignore skinning'
        ),
    BSInt32('node list checksum'),

    BFloat('superhigh lod cutoff', SIDETIP="pixels"),
    BFloat('high lod cutoff', SIDETIP="pixels"),
    BFloat('medium lod cutoff', SIDETIP="pixels"),
    BFloat('low lod cutoff', SIDETIP="pixels"),
    BFloat('superlow lod cutoff', SIDETIP="pixels"),

    BSInt16('superhigh lod nodes', SIDETIP="nodes"),
    BSInt16('high lod nodes', SIDETIP="nodes"),
    BSInt16('medium lod nodes', SIDETIP="nodes"),
    BSInt16('low lod nodes', SIDETIP="nodes"),
    BSInt16('superlow lod nodes', SIDETIP="nodes"),

    Pad(10),

    BFloat('base map u scale'),
    BFloat('base map v scale'),

    Pad(116),

    reflexive("markers", marker, 256, DYN_NAME_PATH=".name"),
    reflexive("nodes", node, 64, DYN_NAME_PATH=".name"),
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    reflexive("geometries", geometry, 256),
    reflexive("shaders", shader, 256, DYN_NAME_PATH=".shader.filepath"),

    SIZE=232
    )


mode_def = TagDef("mode",
    blam_header('mode', 4),
    mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )