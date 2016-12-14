from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return unit_def

camera_track = Struct('camera track',
    dependency('track', "trak"),
    SIZE=28
    )

new_hud_interface = Struct('new hud interface',
    dependency('unit hud interface', "unhi"),
    SIZE=48
    )

dialogue_variant = Struct('dialogue variant',
    BSInt16('variant number'),
    Pad(6),
    dependency('dialogue', "udlg"),
    SIZE=24
    )

powered_seat = Struct('powered seat',
    Pad(4),
    float_sec('driver powerup time'),
    float_sec('driver powerdown time'),
    SIZE=68
    )

weapon = Struct('weapon',
    dependency('weapon', "weap"),
    SIZE=36
    )

seat = Struct('seat',
    BBool32("flags",
        "invisible",
        "locked",
        "driver",
        "gunner",
        "third person camera",
        "allows weapons",
        "third person on enter",
        "first person slaved to gun",
        "allow vehicle communcation animation",
        "not valid without driver",
        "allow ai noncombatants"
        ),
    ascii_str32('label'),
    ascii_str32('marker name'),

    Pad(32),
    QStruct("acceleration scale", INCLUDE=ijk_float),

    Pad(12),
    float_deg_sec('yaw rate'),  # degrees per second
    float_deg_sec('pitch rate'),  # degrees per second
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    float_rad('pitch auto-level'),  # radians
    from_to_rad('pitch range'),  # radians

    reflexive("camera tracks", camera_track, 2,
              'loose', 'tight'),
    reflexive("new hud interfaces", new_hud_interface, 2,
              'default/solo', 'multiplayer'),

    Pad(4),
    BSInt16("hud text message index"),

    Pad(2),
    BFloat('yaw minimum'),
    BFloat('yaw maximum'),
    dependency('built-in gunner', "actv"),
    SIZE=284
    )

unit_attrs = Struct("unit attrs",
    BBool32("flags",
        "circular aiming",
        "destroyed after dying",
        "half-speed interpolation",
        "fires from camera",
        "entrance inside bounding sphere",
        "unused",
        "causes passenger dialogue",
        "resists pings",
        "melee attack is fatal",
        "dont reface during pings",
        "has no aiming",
        "simple creature",
        "impact melee attaches to unit",
        "cannot open doors automatically",
        "melee attackers cannot attach",
        "not instantly killed by melee",
        "shield sapping",
        "runs around flaming",
        "inconsequential",
        "special cinematic unit",
        "ignored by autoaiming",
        "shields fry infection forms",
        "integrated light controls weapon",
        "integrated light lasts forever",
        ),
    BSEnum16('default team', *unit_teams),
    BSEnum16('constant sound volume', *sound_volumes),
    float_zero_to_inf('rider damage fraction'),
    dependency('integrated light toggle', "effe"),
    BSEnum16('A in', *unit_inputs),
    BSEnum16('B in', *unit_inputs),
    BSEnum16('C in', *unit_inputs),
    BSEnum16('D in', *unit_inputs),
    float_rad('camera field of view'),  # radians
    BFloat('camera stiffness'),
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    float_rad('pitch auto-level'),  # radians
    from_to_rad('pitch range'),  # radians
    reflexive("camera tracks", camera_track, 2,
              'loose', 'tight'),

    #Miscellaneous
    QStruct("seat acceleration scale", INCLUDE=ijk_float),
    Pad(12),
    float_zero_to_one('soft ping threshold'),  # [0,1]
    float_sec('soft ping interrupt time'),  # seconds
    float_zero_to_one('hard ping threshold'),  # [0,1]
    float_sec('hard ping interrupt time'),  # seconds
    float_zero_to_one('hard death threshold'),  # [0,1]
    float_zero_to_one('feign death threshold'),  # [0,1]
    float_sec('feign death time'),  # seconds
    float_wu('distance of evade aim'),  # world units
    float_wu('distance of dive aim'),  # world units

    Pad(4),
    float_zero_to_one('stunned movement threshold'),  # [0,1]
    float_zero_to_one('feign death chance'),  # [0,1]
    float_zero_to_one('feign repeat chance'),  # [0,1]
    dependency('spawned actor', "actv"),
    QStruct("spawned actor count",
        BSInt16("from", GUI_NAME=""), BSInt16("to"), ORIENT='h',
        ),
    BFloat('spawned velocity'),
    float_rad_sec('aiming velocity maximum'),  # radians/second
    float_rad_sec_sq('aiming acceleration maximum'),  # radians/second^2
    float_zero_to_one('casual aiming modifier'),
    float_rad_sec('looking velocity maximum'),  # radians/second
    float_rad_sec_sq('looking acceleration maximum'),  # radians/second^2

    Pad(8),
    BFloat('ai vehicle radius'),
    BFloat('ai danger radius'),
    dependency('melee damage', "jpt!"),
    BSEnum16('motion sensor blip size',
        "medium",
        "small",
        "large",
        ),

    Pad(14),
    reflexive("new hud interfaces", new_hud_interface, 2,
              'default/solo', 'multiplayer'),
    reflexive("dialogue variants", dialogue_variant, 16),

    #Grenades
    float_wu_sec('grenade velocity'),
    BSEnum16('grenade type', *grenade_types),
    BSInt16('grenade count', MIN=0),

    Pad(4),
    reflexive("powered seats", powered_seat, 2,
              "driver", "gunner"),
    reflexive("weapons", weapon, 4),
    reflexive("seats", seat, 16),

    SIZE=372
    )

unit_body = Struct('tagdata',
    unit_attrs,
    SIZE=372
    )

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">"
    )
