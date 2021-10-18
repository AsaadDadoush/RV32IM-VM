from myhdl import *


class mem:
    # Init
    def __init__(self, file, size=0, address=intbv, data_memory=[]):
        self.file = file
        self.bytes = size
        self.addres = address
        self.data_memory = data_memory
        numbers_of_lines = 0
        with open(self.file, 'r', encoding='UTF-8') as file:
            while line := file.readline().rstrip():
                numbers_of_lines += 1
        self.data_memory = [intbv(0)[32:]] * (numbers_of_lines * 4)
        n = 0
        with open(self.file, 'r', encoding='UTF-8') as file:
            while line := file.readline().rstrip():
                a = int(line, 2)
                b = intbv(int(line, 2))[32:]
                self.data_memory[n] = b
                n += 4

        file.close()

    def show_memory(self):
        for i in range(len(self.data_memory)):
            print(bin(self.data_memory[i], 32))

    def get_instruction(self, address):
        return self.data_memory[address]

    def write_instruction(self, address, data):
        self.data_memory[address] = data


p1 = mem("C:/Users/ksa_j/PycharmProjects/texts/aa.txt")
print(bin(p1.get_instruction(), 32))
