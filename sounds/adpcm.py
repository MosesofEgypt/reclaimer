import array
import audioop
import sys

try:
    from .ext import adpcm_ext
    fast_adpcm = True
except:
    fast_adpcm = False

__all__ = (
    "decode_adpcm_samples",
    "encode_adpcm_samples",
    )

# Byte size of an encoded xbox adpcm block
XBOX_ADPCM_ENCODED_BLOCKSIZE = 36
# Byte size of a decoded xbox adpcm block
XBOX_ADPCM_DECODED_BLOCKSIZE = 128

# Byte size of an encoded ima adpcm block
IMA_ADPCM_ENCODED_BLOCKSIZE = 36
# Byte size of a decoded ima adpcm block
IMA_ADPCM_DECODED_BLOCKSIZE = 128


NOISE_SHAPING_OFF     = 0  # flat noise (no shaping)
NOISE_SHAPING_STATIC  = 1  # first-order highpass shaping
NOISE_SHAPING_DYNAMIC = 2  # dynamically tilted noise based on signal


def decode_adpcm_samples(in_data, channel_ct, use_xbadpcm,
                         output_big_endian=False):
    if channel_ct < 1:
        return b''
    elif not fast_adpcm:
        raise NotImplementedError(
            "Accelerator module not detected. Cannot decompress ADPCM.")

    encoded_blocksize = (XBOX_ADPCM_ENCODED_BLOCKSIZE if use_xbadpcm else
                         IMA_ADPCM_ENCODED_BLOCKSIZE)
    decoded_blocksize = (XBOX_ADPCM_DECODED_BLOCKSIZE if use_xbadpcm else
                         IMA_ADPCM_DECODED_BLOCKSIZE)

    # divide by 2 since we're treating out_data as a sint16 iterable
    out_data = array.array("h", (0,)) * (
        (len(in_data) // encoded_blocksize) * (decoded_blocksize // 2))

    adpcm_ext.decode_adpcm_samples(
        in_data, out_data, channel_ct, bool(use_xbadpcm))

    if (sys.byteorder == "big") != output_big_endian:
        out_data.byteswap()

    return bytes(out_data)


def encode_adpcm_samples(in_data, channel_ct, use_xbadpcm,
                         input_big_endian=False):
    if channel_ct < 1:
        return b''
    elif not fast_adpcm:
        raise NotImplementedError(
            "Accelerator module not detected. Cannot compress to ADPCM.")

    if (sys.byteorder == "big") != input_big_endian:
        out_data = audioop.byteswap(out_data, 2)

    encoded_blocksize = (XBOX_ADPCM_ENCODED_BLOCKSIZE if use_xbadpcm else
                         IMA_ADPCM_ENCODED_BLOCKSIZE) * channel_ct
    decoded_blocksize = (XBOX_ADPCM_DECODED_BLOCKSIZE if use_xbadpcm else
                         IMA_ADPCM_DECODED_BLOCKSIZE) * channel_ct

    pad_size = len(in_data) % decoded_blocksize
    if pad_size:
        pad_size = decoded_blocksize - pad_size
        # repeat the last sample to the end to pad to a multiple of blocksize
        pad_piece_size = (channel_ct * 2)
        in_data += in_data[-pad_piece_size: ] * (pad_size // pad_piece_size)

    out_data = bytearray(
        (len(in_data) // decoded_blocksize) * encoded_blocksize
        )

    adpcm_ext.encode_adpcm_samples(
        in_data, out_data, channel_ct, bool(use_xbadpcm))

    return bytes(out_data)
