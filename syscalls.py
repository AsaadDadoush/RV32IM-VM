class syscalls:

    def __init__(self, Memory, RegisterFile):
        self.Memory = Memory
        self.flag = False
        if RegisterFile[17] == 93:
            self.flag = True
        elif RegisterFile[17] == 64:
            if RegisterFile[10] == 1:
                for i in range(RegisterFile[12]):
                    print(bytearray.decode(Memory.read(RegisterFile[11], 1)), end="")
                    RegisterFile[11] += 1
                self.flag = False