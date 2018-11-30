############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Copypasta H2
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


snde_meta_def = BlockDef("snde", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt16("priority"),
    SInt16("unknown_1", VISIBLE=False),
    Float("room_intensity"),
    Float("room_intensity_high_frequency"),
    Float("room_rolloff"),
    Float("decay_time"),
    Float("decay_high_frequency_ratio"),
    Float("reflections_intensity", VISIBLE=False),
    Float("reflections_delay"),
    Float("reverb_intensity"),
    Float("reverb_delay"),
    Float("diffusion"),
    Float("density"),
    Float("high_frequency_refrence"),
    BytesRaw("unknown_2", SIZE=16, VISIBLE=False),
    TYPE=Struct, ENDIAN=">", SIZE=72
    )