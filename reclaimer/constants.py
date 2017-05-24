from supyr_struct.defs.constants import *
from binilla.constants import *
from struct import unpack


def inject_halo_constants():
    # add the new descriptor keywords to the sets
    add_desc_keywords()

XBOX_BSP_MAGIC = 0x819A6000

PCDEMO_INDEX_MAGIC = 0x4BF10000
PC_INDEX_MAGIC     = 0x40440000
XBOX_INDEX_MAGIC   = 0x803A6000
STUBBS_INDEX_MAGIC = 0x8038B000


map_build_dates = {
    "stubbs":   "400",
    "pcstubbs": "",
    "xbox":     "01.10.12.2276",
    "xbox2":    "01.10.12.2274",
    "pcdemo":   "01.00.00.0576",
    "pc":       "01.00.00.0564",
    "ce":       "01.00.00.0609",
    "yelo":     "01.00.00.0609",
    }

map_versions = {
    "stubbs": 5,
    "pcstubbs": 5,
    "xbox": 5,
    "pcdemo": 6,
    "pc": 7,
    "ce": 609,
    "yelo": 609,
    }

map_magics = {
    "stubbs":   STUBBS_INDEX_MAGIC,
    "pcstubbs": PC_INDEX_MAGIC,
    "xbox":     XBOX_INDEX_MAGIC,
    "pcdemo":   PCDEMO_INDEX_MAGIC,
    "pc":       PC_INDEX_MAGIC,
    "ce":       PC_INDEX_MAGIC,
    "yelo":     PC_INDEX_MAGIC,
    }

#I cant imagine Halo allowing any one field even close to this many
#indices, though I have seen some open sauce stuff go over 180,000.
MAX_REFLEXIVE_COUNT = 2**31-1

# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
tag_class_fcc_to_be_int = {}
tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
tag_class_be_int_to_fcc = {}
tag_class_le_int_to_fcc = {}

# maps tag class four character codes to the tags file extension
tag_class_fcc_to_ext = {
    'actr': "actor",
    'actv': "actor_variant",
    'ant!': "antenna",
    'bipd': "biped",
    'bitm': "bitmap",
    'trak': "camera_track",
    'colo': "color_table",
    'cdmg': "continuous_damage_effect",
    'cont': "contrail",
    'jpt!': "damage_effect",
    'deca': "decal",
    'udlg': "dialogue",
    'dobc': "detail_object_collection",
    'devi': "device",
    'ctrl': "device_control",
    'lifi': "device_light_fixture",
    'mach': "device_machine",
    'effe': "effect",
    'eqip': "equipment",
    'flag': "flag",
    'fog ': "fog",
    'font': "font",
    'garb': "garbage",
    'mod2': "gbxmodel",
    'matg': "globals",
    'glw!': "glow",
    'grhi': "grenade_hud_interface",
    'hudg': "hud_globals",
    'hmt ': "hud_message_text",
    'hud#': "hud_number",
    'devc': "input_device_defaults",
    'item': "item",
    'itmc': "item_collection",
    'lens': "lens_flare",
    'ligh': "light",
    'mgs2': "light_volume",
    'elec': "lightning",
    'foot': "material_effects",
    'metr': "meter",
    'mode': "model",
    'antr': "model_animations",
    'coll': "model_collision_geometry",
    'mply': "multiplayer_scenario_description",
    'obje': "object",
    'part': "particle",
    'pctl': "particle_system",
    'phys': "physics",
    'plac': "placeholder",
    'pphy': "point_physics",
    'ngpr': "preferences_network_game",
    'proj': "projectile",
    'scnr': "scenario",
    'sbsp': "scenario_structure_bsp",
    'scen': "scenery",
    'snd!': "sound",
    'snde': "sound_environment",
    'lsnd': "sound_looping",
    'ssce': "sound_scenery",
    'boom': "spheroid",
    'shdr': "shader",
    'schi': "shader_transparent_chicago",
    'scex': "shader_transparent_chicago_extended",
    'sotr': "shader_transparent_generic",
    'senv': "shader_environment",
    'sgla': "shader_transparent_glass",
    'smet': "shader_transparent_meter",
    'soso': "shader_model",
    'spla': "shader_transparent_plasma",
    'swat': "shader_transparent_water",
    'sky ': "sky",
    'str#': "string_list",
    'tagc': "tag_collection",
    'Soul': "ui_widget_collection",
    'DeLa': "ui_widget_definition",
    'ustr': "unicode_string_list",
    'unit': "unit",
    'unhi': "unit_hud_interface",
    'vehi': "vehicle",
    'vcky': "virtual_keyboard",
    'weap': "weapon",
    'wphi': "weapon_hud_interface",
    'rain': "weather_particle_system",
    'wind': "wind",
    }

for tag_cls in tag_class_fcc_to_ext:
    tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls


################################
# Open Sauce related constants #
################################
tag_class_fcc_to_ext_os = {
    'avti': "actor_variant_transform_in",
    'avto': "actor_variant_transform_out",
    'avtc': "actor_variant_transform_collection",
    'efpp': "effect_postprocess",
    'efpc': "effect_postprocess_collection",
    'efpg': "effect_postprocess_generic",
    'eqhi': "equipment_hud_interface",
    'magy': "model_animations_yelo",
    'unic': "multilingual_unicode_string_list",
    'yelo': "project_yellow",
    'gelo': "project_yellow_globals",
    'gelc': "project_yellow_globals_cv",
    'shpp': "shader_postprocess",
    'shpg': "shader_postprocess_generic",
    'sppg': "shader_postprocess_globals",
    'sidy': "string_id_yelo",
    'tag+': "tag_database",
    'sily': "text_value_pair_definition",
    }

tag_class_fcc_to_ext_os.update(tag_class_fcc_to_ext)

# maps open sauce tag class four character codes(fccs)
# in their string encoding to their int encoding.
tag_class_fcc_to_be_int_os = {}
tag_class_fcc_to_le_int_os = {}
# maps open sauce tag class four character codes(fccs)
# in their int encoding to their string encoding.
tag_class_be_int_to_fcc_os = {}
tag_class_le_int_to_fcc_os = {}

for tag_cls in tag_class_fcc_to_ext_os:
    tag_class_fcc_to_be_int_os[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc_os[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int_os[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc_os[fcc(tag_cls)] = tag_cls



#######################################
# Stubbs the Zombie related constants #
#######################################
tag_class_fcc_to_ext_stubbs = {
    'imef': "image_effect",
    'vege': "vegetation",
    'terr': "terrain",  # as kornman said, i dont fucking know
    }

tag_class_fcc_to_ext_stubbs.update(tag_class_fcc_to_ext)

# maps open sauce tag class four character codes(fccs)
# in their string encoding to their int encoding.
tag_class_fcc_to_be_int_stubbs = {}
tag_class_fcc_to_le_int_stubbs = {}
# maps open sauce tag class four character codes(fccs)
# in their int encoding to their string encoding.
tag_class_be_int_to_fcc_stubbs = {}
tag_class_le_int_to_fcc_stubbs = {}

for tag_cls in tag_class_fcc_to_ext_stubbs:
    tag_class_fcc_to_be_int_stubbs[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc_stubbs[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int_stubbs[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc_stubbs[fcc(tag_cls)] = tag_cls

