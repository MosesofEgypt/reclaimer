from traceback import format_exc
try:
    from ReclaimerLib.Tag_Handlers.Halo_Programs.Bitmap_Optimizer_and_Converter import *

    if __name__ == '__main__':
        Bitmap_Convertor = Bitmap_Converter_Class(Debug = 0)

except:
    print(format_exc())
    input()