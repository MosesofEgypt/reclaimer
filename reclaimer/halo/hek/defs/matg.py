from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return matg_def

camera = Struct("camera",
    dependency('camera', "trak"),
    SIZE=16
    )

sound = Struct("sound",
    dependency('sound', "snd!"),
    SIZE=16
    )

look_function = Struct("look function",
    BFloat('scale'),
    SIZE=4
    )

player_control = Struct("player control",
    BFloat('magnetism friction'),
    BFloat('magnetism adhesion'),
    BFloat('inconsequential target scale'),

    Pad(52),
    float_sec('look acceleration time'),
    BFloat('look acceleration scale'),
    float_zero_to_one('look peg threshold'),
    float_deg('look default pitch rate'),  # degrees
    float_deg('look default yaw rate'),  # degrees
    BFloat('look autolevelling scale'),

    Pad(20),
    BSInt16('minimum weapon swap ticks'),
    BSInt16('minimum autolevelling ticks'),
    float_rad('minimum angle for vehicle flip'),  # radians
    reflexive("look functions", look_function, 16),

    SIZE=128
    )

difficulty_base = QStruct("",
    BFloat("easy"),
    BFloat("normal"),
    BFloat("hard"),
    BFloat("imposs"),
    ORIENT='h'
    )

difficulty = Struct("difficulty",
    # Health
    Struct("enemy scales",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    Struct("friend scales",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    QStruct("infection form vitality scales", INCLUDE=difficulty_base),

    Pad(16),
    # Enemy ranged fire
    Struct("ranged combat scales",
        QStruct("rate of fire", INCLUDE=difficulty_base),
        QStruct("projectile error", INCLUDE=difficulty_base),
        QStruct("burst error", INCLUDE=difficulty_base),
        QStruct("new target delay", INCLUDE=difficulty_base),
        QStruct("burst separation", INCLUDE=difficulty_base),
        QStruct("target tracking", INCLUDE=difficulty_base),
        QStruct("target leading", INCLUDE=difficulty_base),
        QStruct("overcharge chance", INCLUDE=difficulty_base),
        QStruct("special fire delay", INCLUDE=difficulty_base),
        QStruct("guidance vs player", INCLUDE=difficulty_base),
        ),

    Struct("close combat scales",
        QStruct("melee delay base",
            GUI_NAME="melee delay base(not a scale)", INCLUDE=difficulty_base
            ),
        QStruct("melee delay", INCLUDE=difficulty_base),
           
        Pad(16),
        # Grenades
        QStruct("grenade chance", INCLUDE=difficulty_base),
        QStruct("grenade timer", INCLUDE=difficulty_base),
        ),

    Pad(48),
    # Placement
    Struct("major upgrade fractions",
        QStruct("normal", INCLUDE=difficulty_base),
        QStruct("few", INCLUDE=difficulty_base),
        QStruct("many", INCLUDE=difficulty_base),
        ),

    SIZE=644
    )

grenade = Struct("grenade",
    BSInt16('maximum count'),
    BSInt16('mp spawn default'),
    dependency('throwing effect', "effe"),
    dependency('hud interface', "grhi"),
    dependency('equipment', "eqip"),
    dependency('projectile', "proj"),
    SIZE=68
    )

rasterizer_data = Struct("rasterizer data",
    # Function textures
    dependency('distance attenuation', "bitm"),
    dependency('vector normalization', "bitm"),
    dependency('atmospheric fog density', "bitm"),
    dependency('planar fog density', "bitm"),
    dependency('linear corner fade', "bitm"),
    dependency('active camouflage distortion', "bitm"),
    dependency('glow', "bitm"),

    Pad(60),
    # Default textures
    dependency('default 2d', "bitm"),
    dependency('default 3d', "bitm"),
    dependency('default cubemap', "bitm"),

    # Experimental textures
    dependency('test0', "bitm"),
    dependency('test1', "bitm"),
    dependency('test2', "bitm"),
    dependency('test3', "bitm"),

    # video effect textures
    dependency('video scanline map', "bitm"),
    dependency('video noise map', "bitm"),

    Pad(52),
    # Active camouflage
    BBool16("flags",
        "tint edge density"
        ),
    Pad(2),
    BFloat('refration amount', SIDETIP="pixels"),  # pixels
    BFloat('distance falloff'),
    QStruct('tint color', INCLUDE=rgb_float),
    BFloat('hyper-stealth refration amount', SIDETIP="pixels"),  # pixels
    BFloat('hyper-stealth distance falloff'),
    QStruct('hyper-stealth tint color', INCLUDE=rgb_float),

    # PC textures
    dependency('distance attenuation 2d', "bitm"),

    SIZE=428
    )

interface_bitmaps = Struct("interface bitmaps",
    dependency('font system', "font"),
    dependency('font terminal', "font"),
    dependency('screen color table', "colo"),
    dependency('hud color table', "colo"),
    dependency('editor color table', "colo"),
    dependency('dialog color table', "colo"),
    dependency('hud globals', "hudg"),
    dependency('motion sensor sweep bitmap', "bitm"),
    dependency('motion sensor sweep bitmap mask', "bitm"),
    dependency('multiplayer hud bitmap', "bitm"),
    dependency('localization', "str#"),
    dependency('hud digits definition', "hud#"),
    dependency('motion sensor blip', "bitm"),
    dependency('interface goo map1', "bitm"),
    dependency('interface goo map2', "bitm"),
    dependency('interface goo map3', "bitm"),
    SIZE=304
    )

cheat_weapon = Struct("weapon",
    dependency('weapon', valid_items),
    SIZE=16
    )

cheat_powerup = Struct("powerup",
    dependency('powerup', "eqip"),
    SIZE=16
    )

vehicle = Struct("vehicle",
    dependency('vehicle', "vehi"),
    SIZE=16
    )

multiplayer_information = Struct("multiplayer information",
    dependency('flag', valid_items),
    dependency('unit', valid_units),
    reflexive('vehicles', vehicle, 20),
    dependency('hill shader', valid_shaders),
    dependency('flag shader', valid_shaders),
    dependency('ball', valid_items),
    reflexive('sounds', sound, 60),
    SIZE=160
    )

player_information = Struct("player information",
    dependency('unit', valid_units),

    Pad(28),
    float_wu_sec("walking speed"),  # world units/second
    BFloat("double speed multiplier", SIDETIP="[1.0,+inf]", MIN=1.0),
    float_wu_sec("run forward"),  # world units/second
    float_wu_sec("run backward"),  # world units/second
    float_wu_sec("run sideways"),  # world units/second
    float_wu_sec_sq("run acceleration"),  # world units/second^2
    float_wu_sec("sneak forward"),  # world units/second
    float_wu_sec("sneak backward"),  # world units/second
    float_wu_sec("sneak sideways"),  # world units/second
    float_wu_sec_sq("sneak acceleration"),  # world units/second^2
    float_wu_sec_sq("airborne acceleration"),  # world units/second^2
    BFloat("speed multiplier", SIDETIP="multiplayer only"),  # multiplayer only

    Pad(12),
    QStruct("grenade origin", INCLUDE=xyz_float),

    Pad(12),
    float_zero_to_one("stun movement penalty"),
    float_zero_to_one("stun turning penalty"),
    float_zero_to_one("stun jumping penalty"),
    BFloat("minimum stun time"),
    BFloat("maximum stun time"),

    Pad(8),
    from_to_sec("first person idle time"),
    float_zero_to_one("first person skip fraction"),

    Pad(16),
    dependency('coop respawn effect', "effe"),
    SIZE=244
    )

first_person_interface = Struct("first person interface",
    dependency('first person hands', valid_models),
    dependency('base bitmap', "bitm"),
    dependency('shield meter', "metr"),
    QStruct('shield meter origin',
        BSInt16('x'), BSInt16('y'), ORIENT='h'
        ),
    dependency('body meter', "metr"),
    QStruct('body meter origin',
        BSInt16('x'), BSInt16('y'), ORIENT='h'
        ),
    dependency('night-vision toggle on effect', "effe"),
    dependency('night-vision toggle off effect', "effe"),

    SIZE=192
    )

falling_damage = Struct("falling_damage",
    Pad(8),
    QStruct("harmful falling distance", INCLUDE=from_to),
    dependency('falling damage', "jpt!"),

    Pad(8),
    BFloat("maximum falling distance"),
    dependency('distance damage', "jpt!"),
    dependency('vehicle environment collision damage', "jpt!"),
    dependency('vehicle killed unit damage', "jpt!"),
    dependency('vehicle collision damage', "jpt!"),
    dependency('flaming death damage', "jpt!"),
    SIZE=152
    )

particle_effect = Struct("particle effect",
    dependency('particle type', "part"),
    BBool32("flags", *blend_flags),
    float_wu("density"),
    QStruct("velocity scale", INCLUDE=from_to),

    Pad(4),
    from_to_rad_sec("angular velocity"),  # radians/second

    Pad(8),
    from_to_wu("radius"),  # world units

    Pad(8),
    QStruct("tint lower bound", INCLUDE=argb_float),
    QStruct("tint upper bound", INCLUDE=argb_float),
    SIZE=128
    )

material = Struct("material",
    Pad(148),
    # Vehicle terrain parameters
    BFloat("ground friction scale"),
    BFloat("ground friction normal k1 scale"),
    BFloat("ground friction normal k0 scale"),
    BFloat("ground depth scale"),
    BFloat("ground damp fraction scale"),

    # Breakable surfaceparameters
    Pad(556),
    BFloat("maximum vitality"),

    Pad(12),
    dependency('effect', "effe"),
    dependency('sound', "snd!"),

    Pad(24),
    reflexive("particle effects", particle_effect, 8),

    Pad(60),
    dependency('melee hit sound', "snd!"),
    SIZE=884
    )

playlist_member = Struct("playlist_member",
    ascii_str32("map name"),
    ascii_str32("game variant"),
    BSInt32('minimum experience'),
    BSInt32('maximum experience'),
    BSInt32('minimum player count'),
    BSInt32('maximum player count'),
    BSInt32('rating'),
    SIZE=148
    )

matg_body = Struct('tagdata',
    Pad(248),
    reflexive("sounds", sound, 2,
        "enter water", "exit water"),
    reflexive("cameras", camera, 1),
    reflexive("player controls", player_control, 1),
    reflexive("difficulties", difficulty, 1),
    reflexive("grenades", grenade, 2, *grenade_types),
    reflexive("rasterizer datas", rasterizer_data, 1),
    reflexive("interface bitmaps", interface_bitmaps, 1),
    reflexive("cheat weapons", cheat_weapon, 20),
    reflexive("cheat powerups", cheat_powerup, 20),
    reflexive("multiplayer informations", multiplayer_information, 1),
    reflexive("player informations", player_information, 1),
    reflexive("first person interfaces", first_person_interface, 1),
    reflexive("falling damages", falling_damage, 1),
    reflexive("materials", material, len(materials_list), *materials_list),
    reflexive("playlist members", playlist_member, 20),

    SIZE=428
    )

matg_def = TagDef("matg",
    blam_header('matg', 3),
    matg_body,

    ext=".globals", endian=">"
    )
