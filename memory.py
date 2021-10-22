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


class Memory:

    def __init__(self, maxsize=8191):

        self.buffer = bytearray(maxsize)
        self.Max_Address = len(self.buffer)

    def read(self, address, size):

        assert address + size <= self.Max_Address

        retV = self.buffer[address:address + size]

        return retV

    def write(self, address, size, data):

        assert address + size <= self.Max_Address

        self.buffer[address:address + size] = data

    def load_binary_file(self, path, starting_address):

        new_buff = readfile(path)

        N = len(new_buff)

        max_address = starting_address + N

        if max_address > len(self.buffer):

            temp = self.buffer

            old_N = len(temp)

            self.buffer = bytearray(max_address)

            self.Max_Address = max_address

            self.buffer[0:old_N] = temp

            self.buffer[old_N + 1:] = new_buff

        else:

            self.buffer[0: N] = new_buff

#
# a = Memory()
# a.load_binary_file('C:/Users/axa00/Desktop/test/soso1', starting_address=0)
# a.load_binary_file('C:/Users/axa00/Desktop/test/soso2', starting_address=8192)
# print(to_number(a.read(8268,4),4,True))
# a.write(8268,4,number_to_Buff(92,4))
# print(to_number(a.read(8268,4),4,True))
# # # print(a.buffer)
#