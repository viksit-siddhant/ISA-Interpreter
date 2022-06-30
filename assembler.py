from helper import convert_address_to_binary, convert_value_to_binary, convert_reg_to_binary, handle_vars,handle_labels
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
    
    def assemble(self,line):
        if self.secondary_code is None:
            return self.final_assemble(line)
        else:
            if '$' in line:
                self.type = 'B'
                temp = self.code
                self.code = self.secondary_code
                machine_code = self.final_assemble(line)
                self.code = 'C'
                self.code = temp
                return machine_code                
            else:
                return self.final_assemble(line)

instructions = {'add':Instruction('A','10000'),
                'sub':Instruction('A','10001'),
                'mov':Instruction('C','10011','10010'),
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

file = "input.txt"
file_counter = handle_vars(file)
handle_labels(file)
out_file = open("output.txt","w")
with open(file,"r") as f:
    for i,line in enumerate(f):
        #ignore vars
        if i < file_counter:
            continue
        #get rid of whitespace and labels
        line = line.strip()
        line = line.split(':')[-1]
        command = line.split()[0]
        if command in instructions:
            out_file.write(instructions[command].assemble(line)+"\n")
        else:
            out_file.close()
            raise ValueError("Invalid command")
out_file.close()