from supyr_struct.defs.executables.xbe import *

def get(): return GdlXbeDef

# these are for when the program can handle displaying
# structs and the library can handle union fields
weapon_types = LBitStruct("weapon flags",
    BitUEnum("weapon type",
        "normal",
        "fire",
        "elec",
        "light",
        "acid",
        SIZE=4,
        ),
    BitBool("weapon flags",
        "knockback",
        "knockdown",
        Pad(10),
        "whirlwind",
        Pad(2),
        "three way",
        "super",
        "reflect", 
        "five way",
        "heals",
        Pad(1),
        "turbo",
        Pad(2),
        "hammer",
        "rapid",
        SIZE=28,
        ),
    SIZE=4,
    )

weapon_types_simp = LBool32("weapon flags",
    "fire",
    "elec",
    "acid",
    Pad(1),
    "knockback",
    "knockdown",
    Pad(10),
    "whirlwind",
    Pad(2),
    "three way",
    "super",
    "reflect", 
    "five way",
    "heals",
    Pad(1),
    "turbo",
    Pad(2),
    "hammer",
    "rapid",
    )

armor_types = LBool32("armor flags",
    "resist fire",
    "resist elec",
    "resist light",
    "resist acid",
    "resist magic",
    Pad(3),
    "immune fire",
    "immune elec",
    "immune light",
    "immune acid",
    "immune magic",
    "immune gas",
    Pad(5),
    "immune knockback",

    ("invulnerability silver", 65536),
    ("invulnerability gold", 1048576),

    ("armor reflect", 131072),
    ("armor reflect2", 16777216),
    ("armor protect", 8388608),
    ("armor fire", 2097152),
    ("armor elec", 4194304),

    ("antideath", 524288),
    )

special_types = LBool32("special flags",
    "levitate",
    "x ray",
    "invisible",
    "stop time",
    "fire breath",
    "acid breath",
    "elec breath",
    "phoenix",
    "growth",
    "shrink",
    "pojo",
    Pad(1),
    "skorn horns",
    "skorn mask",
    "skorn gauntlet r",
    "skorn gauntlet l",
    "speed",
    "health",
    Pad(1),
    "turbo",
    "mikey",
    "hand of death",
    "health vampire",
    )

character = Struct("character",                         
    UEnum32("color",
        "yellow",
        "blue",
        "red",
        "green"
        ),
    UEnum32("type",
        "warrior",
        "valkyrie",
        "wizard",
        "archer",
        "dwarf",
        "knight",
        "sorceress",
        "jester",

        "minotaur",
        "falconess",
        "jackal",
        "tigress",
        "ogre",
        "unicorn",
        "medusa",
        "hyena",
        ),
    StrLatin1("code", SIZE=7),
    Pad(1),
    StrLatin1("directory", SIZE=16),
    Bool32("flags",
        "disable",
        ),
    SIZE=36, ENDIAN='<',
    )


cheat = Struct("cheat",
    StrLatin1("code", SIZE=7),
    Pad(1),
    UEnum32("type",
        Pad(1),
        "gold",
        "key",
        Pad(1),
        "potion",

        # these 3 utilize the below flags
        "weapon",
        "armor",
        Pad(2),
        "special",
        ),
    Float("add"),
    Union("flags",
        CASE='.type.data_name',
        CASES={'weapon':weapon_types_simp,
               # 'weapon':weapon_types,
               'armor':armor_types,
               'special':special_types}
        ),
    SIZE=20, ENDIAN='<',
    )


GdlXbeDef = TagDef('xbe',
    xbe_image_header,
    xbe_certificate,
    xbe_sec_headers,
    xbe_lib_ver_headers,
    Array("secret characters",
        SIZE=27, POINTER=1135088,
        SUB_STRUCT=character),
    Array("cheats",
        SIZE=18, POINTER=1136064,
        SUB_STRUCT=cheat),

    ext='.xbe', incomplete=True, endian='<',
    subdefs = {'weapon_types': weapon_types_simp,
               'special_types': special_types,
               'armor_types': armor_types,
               'no_types': Bool32("flags")
               }
    )
