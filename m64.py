#!/usr/bin/python3

#  Reads out .m64 header and button presses

import sys
import numpy as np

def interpret_packet(packet):
    ret = ""

    packet = np.uint32(packet)
    buttons = np.uint16(packet >> 16)
    stick_x = np.int8((packet & 0x0000FF00) >> 8)
    stick_y = np.int8(packet & 0x000000FF)

    if buttons & 0x8000:
        ret += "a,"
    if buttons & 0x4000:
        ret += "b,"
    if buttons & 0x2000:
        ret += "z,"
    if buttons & 0x1000:
        ret += "Start,"
    if buttons & 0x0800:
        ret += "dpad UP,"
    if buttons & 0x0400:
        ret += "dpad DOWN,"
    if buttons & 0x0200:
        ret += "dpad LEFT,"
    if buttons & 0x0100:
        ret += "dpad RIGHT,"
    if buttons & 0x0020:
        ret += "L,"
    if buttons & 0x0010:
        ret += "R,"
    if buttons & 0x0008:
        ret += "C UP,"
    if buttons & 0x0004:
        ret += "C DOWN,"
    if buttons & 0x0002:
        ret += "C LEFT,"
    if buttons & 0x0001:
        ret += "C RIGHT,"

    ret += np.str(stick_x) + ","
    ret += np.str(stick_y) + ","

    ret = "0x" + hex(packet)[2:].rjust(8,'0') + '\t\t' + ret

    print(ret[:-1])


def interpret_file(fileName):
    numInputs = 0

    with open(fileName, "rb") as f:
        signature = int.from_bytes(f.read(4), byteorder='big')
        print('byte signature     ' + hex(signature))

        version = int.from_bytes(f.read(4), byteorder='little', signed=False)
        print('version            ' + str(version))

        uid = int.from_bytes(f.read(4), byteorder='little', signed=True)
        print('uid                ' + str(uid))

        number_of_frames = int.from_bytes(f.read(4), byteorder='little', signed=False)
        print('number of frames   ' + str(number_of_frames))

        rerecord_count = int.from_bytes(f.read(4), byteorder='little', signed=False)
        print('rerecord count     ' + str(rerecord_count))

        fps = int.from_bytes(f.read(1), byteorder='little', signed=False)
        print('fps vertical inter ' + str(fps) )

        number_of_controllers = int.from_bytes(f.read(1), byteorder='little', signed=False)
        print('num of controllers ' + str(number_of_controllers))

        f.read(2)

        number_input_samples = int.from_bytes(f.read(4), byteorder='little', signed=False)
        print('num input samples  ' + str(number_input_samples))

        movie_start_type = int.from_bytes(f.read(2), byteorder='little', signed=False)
        print('movie start type   ' + str(movie_start_type))

        f.read(2)

        controller_flags = int.from_bytes(f.read(4), byteorder='little', signed=False)
        print('controller flags   ' + str(controller_flags))

        f.read(160)

        internal_name_ROM = f.read(32)
        print(internal_name_ROM)

        CRC32 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        print('crc32              ' + str(CRC32))

        country_code = int.from_bytes(f.read(2), byteorder='little', signed=False)
        print('country code       ' + str(country_code))

        f.read(56)

        print()
        video_plugin = f.read(64)
        print(video_plugin)

        print()
        sound_plugin = f.read(64)
        print(sound_plugin)

        print()
        input_plugin = f.read(64)
        print(input_plugin)

        print()
        rsp_plugin = f.read(64)
        print(rsp_plugin)

        print()
        author = f.read(222)
        print(author)

        print()
        description = f.read(256)
        print(description)

        print('\n-------------------------\nnow at 0x400h  input starts\n-------------------------')

        while f.read(1):
            f.seek(-1,1)
            packet = int.from_bytes(f.read(4), byteorder='big', signed=False)
            interpret_packet(packet)
            numInputs = numInputs + 1

        print("Number of Inputs:\t" + str(numInputs))

def main():
    interpret_file(sys.argv[1])

if __name__ == "__main__":
    main()

