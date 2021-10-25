import struct
from myhdl import *
from syscalls import syscalls


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


class CPU:

    def __init__(self, mem, ins):
        self.mem = mem
        self.RegisterFile = [intbv(0)[32:] for i in range(32)]
        self.RegisterFile[2] = 10016
        self.RegisterFile[3] = 6144
        self.PC = 0
        self.ins = ins
        self.flag = False

    def step(self):
        if self.PC > self.mem.Max_Address:
            raise Exception
        self.RegisterFile[0] = 0
        self.ins.decode(bin(intbv(to_number(self.mem.read(self.PC, 4), 4, True)), 32))

        # ================ R-Type Section ============ #
        if self.ins.type_inst == 'R':

            if self.ins.func3 == 0x00 and self.ins.func7 == 0x00:
                # add
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] + self.RegisterFile[self.ins.rs2]

                # sub
            elif self.ins.func3 == 0x00 and self.ins.func7 == 0x20:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] - self.RegisterFile[self.ins.rs2]

                # XOR
            elif self.ins.func3 == 0x4 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] ^ self.RegisterFile[self.ins.rs2]

                # OR
            elif self.ins.func3 == 0x6 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] | self.RegisterFile[self.ins.rs2]

                # AND
            elif self.ins.func3 == 0x7 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] & self.RegisterFile[self.ins.rs2]

                # shift left logical
            elif self.ins.func3 == 0x1 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] << self.RegisterFile[self.ins.rs2]

                # shift right logical
            elif self.ins.func3 == 0x5 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] >> self.RegisterFile[self.ins.rs2]

                # shift right Arith*
            elif self.ins.func3 == 0x5 and self.ins.func7 == 0x20:
                temp = intbv(self.RegisterFile[self.ins.rs1] << self.RegisterFile[self.ins.rs2]).signed()
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] >> self.RegisterFile[self.ins.rs2]

                # Set less than
            elif self.ins.func3 == 0x2 and self.ins.func7 == 0x00:
                if self.RegisterFile[self.ins.rs1] < self.RegisterFile[self.ins.rs2]:
                    self.RegisterFile[self.ins.rd] = 1
                else:
                    self.RegisterFile[self.ins.rd] = 0

                # Set less than (U)
            elif self.ins.func3 == 0x2 and self.ins.func7 == 0x00:
                if self.RegisterFile[self.ins.rs1] < self.RegisterFile[self.ins.rs2]:
                    self.RegisterFile[self.ins.rd] = 1
                else:
                    self.RegisterFile[self.ins.rd] = 0

                # mul
            elif self.ins.func3 == 0x0 and self.ins.func7 == 0x01:
                temp = intbv(self.RegisterFile[self.ins.rs1] * self.RegisterFile[self.ins.rs2])
                self.RegisterFile[self.ins.rd] = temp[32:]

                # MUL High
            # elif ins.func3 == 0x1 and ins.func7 == 0x01:
            #     RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[63:32]
            #
            #     # MUL High (S)(U)
            # elif ins.func3 == 0x2 and ins.func7 == 0x01:
            #     RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[63:32]
            #
            #     # MUL High (U)
            # elif ins.func3 == 0x3 and ins.func7 == 0x01:
            #     RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[63:32]

            # DIV
            elif self.ins.func3 == 0x4 and self.ins.func7 == 0x01:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] / self.RegisterFile[self.ins.rs2]

            # DIV (U)
            elif self.ins.func3 == 0x5 and self.ins.func7 == 0x01:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] / self.RegisterFile[self.ins.rs2]
            # Remainder
            elif self.ins.func3 == 0x6 and self.ins.func7 == 0x01:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] % self.RegisterFile[self.ins.rs2]
            # Remainder (U)
            elif self.ins.func3 == 0x7 and self.ins.func7 == 0x01:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] % self.RegisterFile[self.ins.rs2]

        # ================ I-Type Section ============ #
        elif self.ins.type_inst == 'I':
            # ADD Immediate
            if self.ins.func3 == 0x0:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] + self.ins.imm.signed()
            # XOR Immediate
            elif self.ins.func3 == 0x4:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] ^ self.ins.imm.signed()

            # OR Immediate
            elif self.ins.func3 == 0x6:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] | self.ins.imm.signed()

            # AND Immediate
            elif self.ins.func3 == 0x7:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] & self.ins.imm.signed()

            # Shift left logical Immediate
            elif self.ins.func3 == 0x1 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] << self.ins.imm[5:]

            # Shift right logical Immediate
            elif self.ins.func3 == 0x5 and self.ins.func7 == 0x00:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] >> self.ins.imm[5:]

            # Shift right Arith*
            elif self.ins.func3 == 0x5 and self.ins.func7 == 0x20:
                self.RegisterFile[self.ins.rd] = self.RegisterFile[self.ins.rs1] << self.ins.imm[5:]

            # Set less than
            elif self.ins.func3 == 0x2:
                if self.RegisterFile[self.ins.rs1] < self.RegisterFile[self.ins.rs2]:
                    self.RegisterFile[self.ins.rd] = 1
                else:
                    self.RegisterFile[self.ins.rd] = 0

            # Set less than (U)
            elif self.ins.func3 == 0x3:
                if self.RegisterFile[self.ins.rs1] < self.RegisterFile[self.ins.rs2]:
                    self.RegisterFile[self.ins.rd] = 1
                else:
                    self.RegisterFile[self.ins.rd] = 0

        # ================ I-Type Section (LOAD)  ============ #
        elif self.ins.type_inst == 'I(LOAD)':
            # load Byte
            if self.ins.func3 == 0x0:
                self.RegisterFile[self.ins.rd] = to_number(self.mem.read(self.RegisterFile[self.ins.rs1]
                                                                              + self.ins.imm.signed(), 1), 1, True)
            # load Half
            elif self.ins.func3 == 0x1:
                self.RegisterFile[self.ins.rd] = to_number(self.mem.read((self.RegisterFile[self.ins.rs1] +
                                                                          self.ins.imm.signed(), 2), 2, True))
            # load word
            elif self.ins.func3 == 0x2:
                self.RegisterFile[self.ins.rd] = to_number(self.mem.read((self.RegisterFile[self.ins.rs1]
                                                                          + self.ins.imm.signed()), 4), 4,
                                                           True)


            # load Byte (U)
            elif self.ins.func3 == 0x4:
                self.RegisterFile[self.ins.rd] = to_number(self.mem.read((self.RegisterFile[self.ins.rs1]
                                                                          + self.ins.imm.signed(), 1), 1,
                                                                         True))

            # load Half (U)
            elif self.ins.func3 == 0x5:
                self.RegisterFile[self.ins.rd] = to_number(self.mem.read((self.RegisterFile[self.ins.rs1] +
                                                                          self.ins.imm.signed()), 2), 2, True)

        # ================ I-Type Section (JALR)  ============ #
        # Jump And Link Reg
        elif self.ins.type_inst == 'I(JALR)':
            self.RegisterFile[self.ins.rd] = self.PC + 4
            self.PC = self.RegisterFile[self.ins.rs1] + self.ins.imm.signed()
            return self.RegisterFile

        # ================ I-Type Section (sys calls)  ============ #
        # Environment Call
        elif self.ins.type_inst == 'I(sys calls)':
            if self.ins.imm == 0x0:
                self.flag = syscalls(Memory=self.mem, RegisterFile=self.RegisterFile).flag

        # ================ S-Type Section ============ #
        elif self.ins.type_inst == 'S':
            # Store Byte
            if self.ins.func3 == 0x0:
                self.mem.write((self.RegisterFile[self.ins.rs1] + self.ins.imm), 1,
                               number_to_Buff(self.RegisterFile[self.ins.rs2], 1))

            # Store Half
            elif self.ins.func3 == 0x1:
                self.mem.write((self.RegisterFile[self.ins.rs1] + self.ins.imm), 2,
                               number_to_Buff(self.RegisterFile[self.ins.rs2], 2))

            # Store Word
            elif self.ins.func3 == 0x2:
                self.mem.write((self.RegisterFile[self.ins.rs1] + self.ins.imm), 4,
                               number_to_Buff(self.RegisterFile[self.ins.rs2], 4))

        # ================ B-Type Section ============ #
        elif self.ins.type_inst == 'B':
            # Branch ==
            if self.ins.func3 == 0x0:
                if self.RegisterFile[self.ins.rs1] == self.RegisterFile[self.ins.rs2]:
                    self.PC = self.PC + self.ins.imm.signed() * 2
                    return self.RegisterFile
            # Branch !=
            elif self.ins.func3 == 0x1:
                if self.RegisterFile[self.ins.rs2] != self.RegisterFile[self.ins.rs1]:
                    self.PC = self.PC + self.ins.imm.signed() * 2
                    return self.RegisterFile
            # Branch <
            elif self.ins.func3 == 0x4:
                if self.RegisterFile[self.ins.rs1] < self.RegisterFile[self.ins.rs2]:
                    self.PC = self.PC + self.ins.imm.signed() * 2
                    return self.RegisterFile
            # Branch =<
            elif self.ins.func3 == 0x5:
                if self.RegisterFile[self.ins.rs1] >= self.RegisterFile[self.ins.rs2]:
                    self.PC = self.PC + self.ins.imm.signed() * 2
                    return self.RegisterFile
            # Branch < (U)
            elif self.ins.func3 == 0x6:  # bltu
                if self.RegisterFile[self.ins.rs1] < self.RegisterFile[self.ins.rs2]:
                    self.PC = self.PC + self.ins.imm.signed() * 2
                    return self.RegisterFile
            # # Branch >= (U)
            elif self.ins.func3 == 0x7:  # bgeu
                if self.RegisterFile[self.ins.rs1] >= self.RegisterFile[self.ins.rs2]:
                    self.PC = self.PC + self.ins.imm.signed() * 2
                    return self.RegisterFile

        # ================ J-Type Section ============ #
        # JAL
        elif self.ins.type_inst == 'J':
            self.RegisterFile[self.ins.rd] = self.PC + 4
            self.PC = self.PC + self.ins.imm.signed() * 2
            return self.RegisterFile
        # ================ U-Type Section ============ #
        # load upper imm
        elif self.ins.type_inst == 'U(LUI)':
            self.RegisterFile[self.ins.rd] = self.ins.imm << 12
        # Add upper Imm to PC
        elif self.ins.type_inst == 'U(AUIPC)':
            self.RegisterFile[self.ins.rd] = self.PC + (self.ins.imm.signed() << 12)
        else:
            print("Instruction on text memory is not correct")

        self.PC += 4