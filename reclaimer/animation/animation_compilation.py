import traceback

from struct import Struct as PyStruct

__all__ = ("compile_animation", "compile_animation_tag", )


def compile_animation(anim, jma_anim):
    '''
    Compiles the provided JmaAnimation into the provided antr animation block.
    '''
    anim.name = jma_anim.name
    anim.type.set_to(jma_anim.anim_type)
    anim.frame_count = jma_anim.frame_count
    anim.frame_size = jma_anim.frame_data_frame_size
    anim.frame_info_type.set_to(jma_anim.frame_info_type)
    anim.node_list_checksum = jma_anim.node_list_checksum
    anim.node_count = jma_anim.node_count

    # cant compress animations yet
    anim.flags.data = 0
    anim.flags.world_relative = jma_anim.world_relative
    anim.offset_to_compressed_data = 0

    anim.trans_flags0 =  jma_anim.trans_flags_int & 0xFFffFFff
    anim.trans_flags1 = (jma_anim.trans_flags_int >> 32) & 0xFFffFFff
    anim.rot_flags0   =  jma_anim.rot_flags_int & 0xFFffFFff
    anim.rot_flags1   = (jma_anim.rot_flags_int >> 32) & 0xFFffFFff
    anim.scale_flags0 =  jma_anim.scale_flags_int & 0xFFffFFff
    anim.scale_flags1 = (jma_anim.scale_flags_int >> 32) & 0xFFffFFff

    # determine the sizes of the frame_info, default_data, and frame_data
    frame_info_node_size = jma_anim.root_node_info_frame_size

    frame_info_size   = frame_info_node_size * jma_anim.frame_count
    default_data_size = jma_anim.default_data_size
    frame_data_size   = jma_anim.frame_data_frame_size * anim.frame_count

    max_frame_info_size   = anim.frame_info.get_desc('MAX', 'size')
    max_default_data_size = anim.default_data.get_desc('MAX', 'size')
    max_frame_data_size   = anim.frame_data.get_desc('MAX', 'size')

    if frame_info_size > max_frame_info_size:
        raise ValueError("Too much frame_info data. Max is %s bytes, got %s" %
                         (max_frame_info_size, frame_info_size))
    elif default_data_size > max_default_data_size:
        raise ValueError("Too much default data. Max is %s bytes, got %s" %
                         (max_default_data_size, default_data_size))
    elif frame_data_size > max_frame_data_size:
        raise ValueError("Too much frame data. Max is %s bytes, got %s" %
                         (max_frame_data_size, frame_data_size))


    anim.frame_info.STEPTREE   = bytearray(b'\x00' * frame_info_size)
    anim.default_data.STEPTREE = bytearray(b'\x00' * default_data_size)
    anim.frame_data.STEPTREE   = bytearray(b'\x00' * frame_data_size)

    frame_info   = anim.frame_info.STEPTREE
    default_data = anim.default_data.STEPTREE
    frame_data   = anim.frame_data.STEPTREE

    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags
    has_dxdy = "dx"   in jma_anim.frame_info_type
    has_dz   = "dz"   in jma_anim.frame_info_type
    has_dyaw = "dyaw" in jma_anim.frame_info_type

    pack_1_float_into = PyStruct(">f").pack_into
    pack_2_float_into = PyStruct(">2f").pack_into
    pack_3_float_into = PyStruct(">3f").pack_into
    pack_4_float_into = PyStruct(">4f").pack_into
    pack_4_int16_into = PyStruct(">4h").pack_into

    i = 0
    for f in range(anim.frame_count):
        info = jma_anim.root_node_info[f]
        if has_dz:
            pack_4_float_into(frame_info, i, info.dx, info.dy, info.dz, info.dyaw)
        elif has_dyaw:
            pack_3_float_into(frame_info, i, info.dx, info.dy, info.dyaw)
        elif has_dxdy:
            pack_2_float_into(frame_info, i, info.dx, info.dy)
        else:
            break

        i += frame_info_node_size

    # write the rotations, translations, and scales
    # to the frame_data and def_data
    i = j = 0
    def_state = None
    for f in range(anim.frame_count):
        for n in range(anim.node_count):
            node_state = jma_anim.frames[f][n]

            if rot_flags[n]:
                pack_4_int16_into(frame_data, i,
                    int(node_state.rot_i*32767), int(node_state.rot_j*32767),
                    int(node_state.rot_k*32767), int(node_state.rot_w*32767))
                i += 8
            elif f == 0:
                pack_4_int16_into(default_data, j,
                    int(node_state.rot_i*32767), int(node_state.rot_j*32767),
                    int(node_state.rot_k*32767), int(node_state.rot_w*32767))
                j += 8

            if trans_flags[n]:
                pack_3_float_into(frame_data, i,
                    node_state.pos_x, node_state.pos_y, node_state.pos_z)
                i += 12
            elif f == 0:
                pack_3_float_into(default_data, j,
                    node_state.pos_x, node_state.pos_y, node_state.pos_z)
                j += 12

            if scale_flags[n]:
                pack_1_float_into(frame_data, i, node_state.scale)
                i += 4
            elif f == 0:
                pack_1_float_into(default_data, j, node_state.scale)
                j += 4


def compile_animation_tag(antr_tag, jma_anim_set):
    antr_units = antr_tag.data.tagdata.units.STEPTREE
    antr_weapons = antr_tag.data.tagdata.weapons.STEPTREE
    antr_vehicles = antr_tag.data.tagdata.vehicles.STEPTREE
    antr_devices = antr_tag.data.tagdata.devices.STEPTREE
    antr_unit_damages = antr_tag.data.tagdata.unit_damages.STEPTREE
    antr_fp_animations = antr_tag.data.tagdata.fp_animations.STEPTREE
    antr_anims = antr_tag.data.tagdata.animations.STEPTREE
    antr_nodes = antr_tag.data.tagdata.nodes.STEPTREE

    del antr_weapons[:]
    del antr_vehicles[:]
    del antr_devices[:]
    del antr_unit_damages[:]
    del antr_fp_animations[:]
    del antr_nodes[:]
    del antr_anims[:]

    for jma_node in jma_anim_set.nodes:
        antr_nodes.append()
        antr_node = antr_nodes[-1]
        antr_node.name = jma_node.name
        antr_node.next_sibling_node_index = jma_node.sibling_index
        antr_node.first_child_node_index = jma_node.first_child
        antr_node.parent_node_index = jma_node.parent_index

    unit_labels = set()

    for jma_anim_name in sorted(jma_anim_set.animations):
        try:
            antr_anims.append()
            compile_animation(antr_anims[-1], jma_anim_set[jma_anim_name])
        except Exception:
            print(traceback.format_exc())
            antr_anims.pop(-1)

        # determine where this animation is to be used
        name_pieces = jma_anim_name.split(" ")
        if len(name_pieces) < 2:
            continue

    # remove any unused unit blocks
    for i in range(len(antr_units) - 1, -1, -1)
        if antr_units[i].label not in unit_names:
            antr_units.pop(i)
