from CPU import CPU
from memory import Memory, to_number
from Instruction import Instruction


inst = Instruction()
mem = Memory()
mem.load_binary_file(path='C:/Users/asaad/Desktop/test2/text.txt', starting_address=0)
mem.load_binary_file(path='C:/Users/asaad/Desktop/test2/data.txt', starting_address=8192)
test = CPU(mem, inst)

while not test.flag:
    test.step()

print("Before Executing")
print("Data Memory at Result[0]:", to_number(mem.read(8268, 4), 4, True))
print("Data Memory at Result[1]:", to_number(mem.read(8272, 4), 4, True))
# print("Data Memory at Result[0]:", to_number(mem.read(8268, 4), 4, True))
# print("Data Memory at Result[1]:", to_number(mem.read(8272, 4), 4, True))
