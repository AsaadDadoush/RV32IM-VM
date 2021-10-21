from myhdl import *
import struct

def to_number(buff: bytearray, size, signed, little_endian=True):
    endianness = '<' if little_endian else '>'
    if size == 1:
        fmt = f'b' if signed else f'B'
    elif size == 2:
        fmt = f'{endianness}h' if signed else f'{endianness}H'
    elif size == 4:
        fmt = f'{endianness}i' if signed else f'{endianness}I'
    elif size == 8:
        fmt = f'{endianness}q' if signed else f'{endianness}Q'
    else:
        raise Exception('unsupported Size')

    retV = struct.unpack(fmt, buff[0:size])
    return retV[0]


def number_to_Buff(number: int, size, little_endian=True):
    endianness = '<' if little_endian else '>'
    if size == 1:
        fmt = f'b'
    elif size == 2:
        fmt = f'{endianness}h'
    elif size == 4:
        fmt = f'{endianness}i'
    elif size == 8:
        fmt = f'{endianness}q'
    else:
        raise Exception('unsupported Size')

    retV = struct.pack(fmt, number)
    return retV


def readfile(path):
    f = open(path, 'rb')

    buff = f.read()

    f.close()

    return bytearray(buff)


class InstructionMemory:

    def __init__(self, maxsize=1024):

        self.buffer = bytearray(maxsize)
        self.Max_Address = len(self.buffer)

    def read(self, address, size):

        assert address + size <= self.Max_Address

        retV = self.buffer[address:address + size]

        return retV

    def load_binary_file(self, path, starting_address=0):

        new_buff = readfile(path)
        # N = len(new_buff)
        self.buffer = new_buff

#
# a = InstructionMemory("s")
# b = readfile("C:/Users/ksa_j/PycharmProjects/texts/binarydata.txt")
#
# # print(to_number(b, 4, True))
# # print(number_to_Buff(4, 4))
# a.load_binary_file("C:/Users/ksa_j/PycharmProjects/texts/binary.txt")
# print(a.buffer)
# c = intbv(to_number(a.read(0, 4), 4, signed=True))
# print(bin(c, 32))