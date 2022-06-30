variables = {}

from helper import convert_address_to_binary, convert_value_to_binary, convert_reg_to_binary

class Instruction:
    def __init__(self, type, code, secondary_code=None):
        self.type = type
        self.code = code
        self.secondary_code = secondary_code
    
    def final_assemble(self,line):
        command = line.split()
        if self.type == 'A':
            return self.code+'00'+convert_reg_to_binary(command[1])+convert_reg_to_binary(command[2])+convert_reg_to_binary(command[3])
        elif self.type == 'B':
            return self.code+convert_reg_to_binary(command[1])+convert_value_to_binary(int(command[2][1:]))
        elif self.type == 'C':
            return self.code+'00000'+convert_reg_to_binary(command[1])+convert_reg_to_binary(command[2])
        elif self.type == 'D':
            return self.code+convert_reg_to_binary(command[1])+convert_address_to_binary(command[2])
        elif self.type == 'E':
            return self.code+'000'+convert_address_to_binary(command[1])
        else:
            return self.code+('0'*11)

class Variable:
    #TODO
    pass


instructions = {'add':Instruction('A','10000'),
                'sub':Instruction('A','10001'),
                'mov':Instruction('B','10010','10011'),
                'ld':Instruction('D','10100'),
                'st':Instruction('D','10101'),
                'mul':Instruction('A','10110'),
                'div':Instruction('C','10111'),
                'rs':Instruction('B','11000'),
                'ls':Instruction('B','11001'),
                'xor':Instruction('A','11010'),
                'or':Instruction('A','11011'),
                'and':Instruction('A','11100'),
                'not':Instruction('C','11101'),
                'cmp':Instruction('C','11110'),
                'jmp':Instruction('E','11111'),
                'jlt':Instruction('E','01100'),
                'jgt':Instruction('E','01101'),
                'jeq':Instruction('E','01111'),
                'hlt':Instruction('F','01010'),}