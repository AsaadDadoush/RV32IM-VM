def readfile(path):
    f = open(path, 'rb')

    buff = f.read()

    f.close()

    return bytearray(buff)


class Memory:

    def __init__(self, maxsize=8191):

        self.buffer = bytearray(maxsize)
        self.Max_Address = len(self.buffer)

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

    def read(self, address, size):

        assert address + size <= self.Max_Address

        retV = self.buffer[address:address + size]

        return retV

    def write(self, address, size, data):

        assert address + size <= self.Max_Address

        self.buffer[address:address + size] = data