# rv32im-vm

This Virtual machine will work on the command Prompt(CMD)

to run your program make sure that the two binary files

1-Code Binary.bin

2-Data Binary.bin

in the same directory of python project

Also make sure that the Text binary file must be compact at address 0 

And the Data binary file must be compact at address 8192

Commands to use:

1-team-1-risc-vm.py -h

to see the requiered arguments  to run

2- team-1-risc-vm.py TextBinaryFile.bin  DataBinaryFile.bin
Example:

team-1-risc-vm.py Code-Binary.bin  Data-Binary.bin

TextBinaryFile = Code-Binary

DataBinaryFile = Data-Binary
