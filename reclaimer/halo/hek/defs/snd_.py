from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

sound_classes = (
    ("projectile impact", 0),
    ("projectile detonation", 1),

    ("weapon fire", 4),
    ("weapon ready", 5),
    ("weapon reload", 6),
    ("weapon empty", 7),
    ("weapon charge", 8),
    ("weapon overheat", 9),
    ("weapon idle", 10),

    ("object impacts", 13),
    ("particle impacts", 14),
    ("slow particle impacts", 15),

    ("unit footsteps", 18),
    ("unit dialog", 19),

    ("vehicle collision", 22),
    ("vehicle engine", 23),

    ("device door", 26),
    ("device force field", 27),
    ("device machinery", 28),
    ("device nature", 29),
    ("device computers", 30),

    ("music", 32),
    ("ambient nature", 33),
    ("ambient machinery", 34),
    ("ambient computers", 35),

    ("first person damage", 39),

    ("scripted dialog player", 44),
    ("scripted effect", 45),
    ("scripted dialog other", 46),
    ("scripted dialog force unspatialized", 47),

    ("game event", 50),
    )

compression = BSEnum16("compression",
    'none',
    'xbox adpcm',
    'ima adpcm',
    'ogg'
    )


permutation = Struct('permutation',
    StrLatin1("name", SIZE=32),
    BFloat("skip fraction"),
    BFloat("gain"),
    compression,
    BSInt16("next permutation index"),
    Pad(20),

    rawdata_ref("samples"),
    rawdata_ref("mouth data"),
    rawdata_ref("subtitle data"),

    SIZE=124
    )

pitch_range = Struct('pitch range',
    StrLatin1("name", SIZE=32),

    BFloat("natural pitch"),
    Struct("bend bounds", INCLUDE=from_to),
    BSInt16("actual permutation count"),
    Pad(14),

    reflexive("permutations", permutation, 256),
    SIZE=72,
    )


snd__body = Struct("tagdata",
    BBool32("flags",
        "fit to adpcm blocksize",
        "split long sound into permutations"
        ),
    BSEnum16("class", *sound_classes),
    BSEnum16("sample rate",
        {NAME: "khz_22", GUI_NAME: "22kHz"},
        {NAME: "khz_44", GUI_NAME: "44kHz"},
        ),
    BFloat("minimum distance"),
    BFloat("maximum distance"),
    BFloat("skip fraction"),  # [0.0 to 1.0]

    #Randomization
    Struct("random pitch bounds", INCLUDE=from_to),
    BFloat("inner cone angle"),  # measured in radians
    BFloat("outer cone angle"),  # measured in radians
    BFloat("outer cone gain"),  # [0.0 to 1.0]
    BFloat("gain modifier"),
    BFloat("maximum bend per second"),
    Pad(12),

    Struct("modifiers when scale is zero",
        BFloat("skip fraction"),
        BFloat("gain"),
        BFloat("pitch"),
        ),
    Pad(12),

    Struct("modifiers when scale is one",
        BFloat("skip fraction"),
        BFloat("gain"),
        BFloat("pitch"),
        ),
    Pad(12),

    BSEnum16("encoding",
        'mono',
        'stereo'
        ),
    compression,
    dependency("promotion sound", valid_sounds),
    BSInt16("promotion count"),
    Pad(22),
    reflexive("pitch ranges", pitch_range, 8),

    SIZE=164,
    )

    
def get():
    return snd__def

snd__def = TagDef("snd!",
    blam_header('snd!', 4),
    snd__body,

    ext=".sound", endian=">",
    )