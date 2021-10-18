from myhdl import *
from memory import mem
from Instruction import Instruction

memText = mem("C:/Users/ksa_j/PycharmProjects/texts/text.txt")
memdata = mem("C:/Users/ksa_j/PycharmProjects/texts/data.txt")
RegisterFile = [intbv(0)[32:] for i in range(32)]
PC = 0


def cpu():
    for i in range(memText.instruction_num):
        ins = Instruction(memText.get_data(PC))

        # ================ R-Type Section ============ #
        if ins.type_inst == 'R':
            if ins.func3 == 0x00 & ins.func7 == 0x00:
                # add
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] + RegisterFile[ins.rs2]

                # sub
            elif ins.func3 == 0x00 & ins.func7 == 0x20:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] - RegisterFile[ins.rs2]

                # XOR
            elif ins.func3 == 0x4 & ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] ^ RegisterFile[ins.rs2]

                # OR
            elif ins.func3 == 0x6 & ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] | RegisterFile[ins.rs2]

                # AND
            elif ins.func3 == 0x7 & ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] & RegisterFile[ins.rs2]

                # shift left logical
            elif ins.func3 == 0x1 & ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] << RegisterFile[ins.rs2]

                # shift right logical
            elif ins.func3 == 0x5 & ins.func7 == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] >> RegisterFile[ins.rs2]

                # TODO zero-extends
                # shift right Arith*
            elif ins.func3 == 0x5 & ins.func7 == 0x20:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] << RegisterFile[ins.rs2]

                # Set less than
            elif ins.func3 == 0x2 & ins.func7 == 0x00:
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    RegisterFile[ins.rd] = 1
                else:
                    RegisterFile[ins.rd] = 0

                # TODO zero-extends
                # Set less than (U)
            elif ins.func3 == 0x2 & ins.func7 == 0x00:
                if RegisterFile[ins.rs1] < RegisterFile[ins.rs2]:
                    RegisterFile[ins.rd] = 1
                else:
                    RegisterFile[ins.rd] = 0

                # mul
            elif ins.func3 == 0x0 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[31:0]

                # MUL High
            elif ins.func3 == 0x1 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[63:32]

                # MUL High (S)(U)
            elif ins.func3 == 0x2 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[63:32]

                # MUL High (U)
            elif ins.func3 == 0x3 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = (RegisterFile[ins.rs1] * RegisterFile[ins.rs2])[63:32]

                # DIV
            elif ins.func3 == 0x4 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] / RegisterFile[ins.rs2]

                # DIV (U)
            elif ins.func3 == 0x5 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] / RegisterFile[ins.rs2]

            # Remainder
            elif ins.func3 == 0x6 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] % RegisterFile[ins.rs2]

            elif ins.func3 == 0x7 & ins.func7 == 0x01:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] % RegisterFile[ins.rs2]
            else:
                print("Instruction on memory for address %s is not correct" % memText.addres)
        # ================ I-Type Section ============ #
        elif ins.type_inst == 'I':
            # ADD Immediate
            if ins.func3 == 0x0:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] + ins.imm

            # XOR Immediate
            elif ins.func3 == 0x4:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] ^ ins.imm

            # OR Immediate
            elif ins.func3 == 0x6:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] ^ ins.imm

            # AND Immediate
            elif ins.func3 == 0x7:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] & ins.imm

            # Shift left logical Immediate
            elif ins.func3 == 0x1 & ins.imm[11:5]==0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] << ins.imm[4:]

                # Shift right logical Immediate
            elif ins.func3 == 0x5 & ins.imm[11:5] == 0x00:
                RegisterFile[ins.rd] = RegisterFile[ins.rs1] >> ins.imm[4:]

                # Shift right Arith* Immediate
            elif ins.func3 == 0x5 & ins.imm[11:5] == 0x20:
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
        elif ins.type_inst == 'I(LOAD)':
            if ins.func3 == 0x0:
                RegisterFile[ins.rd] = memdata.get_data(RegisterFile[ins.rs1] + ins.imm)
            elif ins.func3 == 0x1:
                RegisterFile[ins.rd] = memdata.get_data(RegisterFile[ins.rs1] + ins.imm)

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
