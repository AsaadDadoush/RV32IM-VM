from myhdl import *


class mem:
    # Init
    def __init__(self, file, size=0, address=intbv(0), data_memory=[], instruction_num=0):
        self.file = file
        self.addres = address
        self.data_memory = data_memory
        numbers_of_lines = 0
        self.data_memory = []
        with open(self.file, 'r') as file:
            for i in file:
                a = file.read()
                print(a)
                b = a[0:8]
                print(b)

    def show_memory(self):
        ad = 0
        for i in self.data_memory:
            print(self.data_memory)

    def get_data(self, address):
        return self.data_memory[address]

    def write_instruction(self, address, data):
        self.data_memory[address] = data


p1 = mem("C:/Users/ksa_j/PycharmProjects/texts/aa.txt")
print(p1.show_memory())