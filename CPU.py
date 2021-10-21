from myhdl import *
import struct
from memory import Memory
from InstructionMemory import InstructionMemory
from Instruction import Instruction
# import syscalls

memText = InstructionMemory()
memdata = Memory()
RegisterFile = [intbv(0)[32:] for i in range(32)]
RegisterFile [2]=16380
RegisterFile [3]=6144


memText.load_binary_file('C:/Users/axa00/Desktop/Test1.txt')
memdata.load_binary_file('C:/Users/axa00/Desktop/bidata.txt')

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

def cpu():
    PC = 0
    ins = Instruction()
    for i in range(memText.Max_Address):
        ins.decode(bin(intbv(to_number(memText.read(PC,4),4,True)),32))
        print(bin(intbv(to_number(memText.read(PC,4),4,True)),32))
        # ================ R-Type Section ============ #
        if ins.type_inst == 'R':

            if ins.func3 == 0x00 and ins.func7 == 0x00:
                # add
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] + RegisterFile[ins.rs2]

                print(ins.rd)
                print(ins.rs1)
                print(ins.rs2)


                # sub
            elif ins.func3 == 0x00 and ins.func7 == 0x20:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] - RegisterFile[ins.rs2]

                # XOR
            elif ins.func3 == 0x4 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] ^ RegisterFile[ins.rs2]

                # OR
            elif ins.func3 == 0x6 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] | RegisterFile[ins.rs2]

                # AND
            elif ins.func3 == 0x7 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] & RegisterFile[ins.rs2]

                # shift left logical
            elif ins.func3 == 0x1 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] << RegisterFile[ins.rs2]

                # shift right logical
            elif ins.func3 == 0x5 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] >> RegisterFile[ins.rs2]
                # TODO zero-extends
                # shift right Arith*
            elif ins.func3 == 0x5 and ins.func7 == 0x20:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1.signed()] << RegisterFile[ins.rs2]

                # Set less than
            elif ins.func3 == 0x2 and ins.func7 == 0x00:
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    RegisterFile[ins.rd] = 1
                else:
                    RegisterFile[ins.rd] = 0

                # TODO zero-extends
                # Set less than (U)
            elif ins.func3 == 0x2 and ins.func7 == 0x00:
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    RegisterFile[ins.rd] = 1
                else:
                    RegisterFile[ins.rd] = 0

                # mul
                # TODO try
            elif ins.func3 == 0x0 and ins.func7 == 0x01:
                RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[31:0]

                  # TODO 32 bit implemtaion ?
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
             # TODO what the difference with DIV
                # DIV
            elif ins.func3 == 0x4 and ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] / RegisterFile[ins.rs2]

                # DIV (U)
            elif ins.func3 == 0x5 and ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] / RegisterFile[ins.rs2]
                # TODO what the difference with Remainder
                # Remainder
            elif ins.func3 == 0x6 and ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] % RegisterFile[ins.rs2]
                # Remainder (U)
            elif ins.func3 == 0x7 and ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] % RegisterFile[ins.rs2]
            else:
                print("Instruction on memory for address %s is not correct" )
        # ================ I-Type Section ============ #
        elif ins.type_inst == 'I':
            # ADD Immediate
            if ins.func3 == 0x0:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] + ins.imm
                print(ins.rd)
                print(RegisterFile[ins.rd])
            # XOR Immediate
            elif ins.func3 == 0x4:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] ^ ins.imm

            # OR Immediate
            elif ins.func3 == 0x6:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] | ins.imm

            # AND Immediate
            elif ins.func3 == 0x7:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] & ins.imm

            # Shift left logical Immediate
            elif ins.func3 == 0x1 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] << ins.imm[4:]

                # Shift right logical Immediate
            elif ins.func3 == 0x5 and ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] >> ins.imm[4:]
                # TODO msb-extends
                # Shift right Arith* Immediate
            elif ins.func3 == 0x5 and ins.func7 == 0x20:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] << ins.imm[4:]

                # Set less than
            elif ins.func3 == 0x2:
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    RegisterFile[ins.rd] = 1
                else:
                    RegisterFile[ins.rd] = 0

                # TODO zero-extends
                # Set less than (U)
            elif ins.func3 == 0x3:
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    RegisterFile[ins.rd] = 1
                else:
                    RegisterFile[ins.rd] = 0
                    # TODO loads type
                # load
        elif ins.type_inst == 'I(LOAD)':
            if ins.func3 == 0x0 :
                RegisterFile[ins.rd] = intbv(to_number(memdata.read(RegisterFile[ins.rs1] + ins.imm),1))
            elif ins.func3 == 0x1:
                RegisterFile[ins.rd] = intbv(to_number(memdata.read(RegisterFile[ins.rs1] + ins.imm),2))
            elif ins.func3 == 0x2:
                RegisterFile[ins.rd] = intbv(to_number(memdata.read(RegisterFile[ins.rs1] + ins.imm), 4))
            # TODO zero-extends
            elif ins.func3 == 0x4:
                RegisterFile[ins.rd] = intbv(to_number(memdata.read(RegisterFile[ins.rs1] + ins.imm), 1))
                # TODO zero-extends
            elif ins.func3 == 0x5:
                RegisterFile[ins.rd] = intbv(to_number(memdata.read(RegisterFile[ins.rs1] + ins.imm), 2))

        elif ins.type_inst == 'I(JALR)':
            RegisterFile[ins.rd] = PC + 4
            PC = RegisterFile[ins.rs1] + ins.imm()
        # ================ S-Type Section ============ #
        elif ins.type_inst == 'S':
            if ins.func3 == 0x0:
                memdata.write(RegisterFile[ins.rs1] + ins.imm,1,RegisterFile[ins.rs2])
            elif ins.func3 == 0x1:
                memdata.write(RegisterFile[ins.rs1] + ins.imm,2,RegisterFile[ins.rs2])
            elif ins.func3 == 0x2:
                memdata.write(RegisterFile[ins.rs1] + ins.imm,4,RegisterFile[ins.rs2])


        # ================ B-Type Section ============ #
        elif ins.type_inst == 'B':

            if ins.func3 == 0x0:  # beq
                if RegisterFile[ins.rs1] == RegisterFile[ins.rs2]:
                    PC = PC + ins.imm
                    continue
            if ins.func3 == 0x1:  # bne
                if not (RegisterFile[ins.rs1] == RegisterFile[ins.rs2]):
                    PC = PC + ins.imm
                    continue
            if ins.func3 == 0x4:  # blt
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    PC = PC + ins.imm
                    continue
            if ins.func3 == 0x5:  # bge
                if RegisterFile[ins.rs1] >= RegisterFile[ins.rs2]:
                    PC = PC + ins.imm
                    continue
            if ins.func3 == 0x6:  # bltu
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    PC = PC + ins.imm
                    continue
            if ins.func3 == 0x7:  # bgeu
                if RegisterFile[ins.rs1] >= RegisterFile[ins.rs2]:
                    PC = PC + ins.imm
                    continue
            # ================ J-Type Section ============ #
        elif ins.type_inst == 'J':
            RegisterFile[ins.rd] = PC + 4
            PC = PC + ins.imm
            # ================ U-Type Section ============ #
        elif ins.type_inst == 'U(LUI)':
            RegisterFile[ins.rd]=  ins.imm <<12
        elif ins.type_inst == 'U(AUIPC)':
            RegisterFile[ins.rd] = PC + (ins.imm << 12)


        PC+=4
print(RegisterFile)
    # TODO syscalls
# def ecall(self):
# def ebreak(self):

cpu()