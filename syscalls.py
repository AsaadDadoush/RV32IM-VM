import math


class syscalls:

    def __init__(self, Memory, RegisterFile):
        self.Memory = Memory
        self.a0 = RegisterFile[10]
        self.a1 = RegisterFile[11]
        self.a2 = RegisterFile[12]
        self.a7 = RegisterFile[17]
        self.flag = False
        if self.a7 == 93:
            self.flag = True
        elif self.a7 == 64:
            if self.a0 == 1:
                a = ''
                for i in range(math.ceil(self.a2 / 4)):
                    a = a + bytearray.decode(Memory.read(self.a1, 4))
                    self.a1 += 4
                print(a)
                self.flag = False