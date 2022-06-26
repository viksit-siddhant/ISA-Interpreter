variables = {}

def convert_reg_to_binary(reg):
    #Strip R from register name
    reg = reg[1:]
    #Convert to binary
    reg = bin(int(reg))[2:]
    #Pad with zeros
    reg = reg.zfill(3)
    return reg

def convert_value_to_binary(val):
    #Convert to binary
    val = bin(int(val))[2:]
    #Pad with zeros
    if len(val) > 8:
        raise ValueError("Immediate value too large")
    val = val.zfill(8)
    return val

def convert_address_to_binary(address):
    #Convert to binary
    try:
        address = bin(int(address))[2:]
        #Pad with zeros
        address = address.zfill(8)
        return address
    except Exception:
        if address in variables:
            return variables[address]
        else:
            raise ValueError("Address not found")


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



