import argparse
from CPU import CPU
from memory import Memory
from Instruction import Instruction

parser = argparse.ArgumentParser()
parser.add_argument('Path1', help="Path of Text binary file: Name_file.bin", type=str)
parser.add_argument('Path2', help="Path of Data binary file: Name_file.bin", type=str)
args = parser.parse_args()
inst = Instruction()
mem = Memory()
mem.load_binary_file(path=args.Path1, starting_address=0)  # Text section will start on address 0
mem.load_binary_file(path=args.Path2, starting_address=8192)  # Data section will start on address 8192
test = CPU(mem, inst)
while not test.flag:
    test.step()