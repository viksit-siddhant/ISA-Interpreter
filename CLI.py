import math

units = {
    'M': 2**20,
    'K': 2**10,
    'B': 1,
    'b': 1,
    'G': 2**30,
}

space = input("Enter total size of memory:")
num, unit = space.split()
num = int(num)
if (unit[0] in units):
    num *= units[unit[0]]
else:
    raise ValueError("Invalid unit")
if unit[-1] == 'B':
    num *= 8

print('''Enter how the memory is addressed:
1. Bit addressable
2. Nibble addressable
3. Byte addressable
4. Word addressable''')
mode = int(input())
if mode == 4:
    mode = int(input("Enter word size(in bytes):"))*8
modes = {
    1: 1,
    2: 4,
    3: 8,
}
num_addr = num/(modes[mode] if mode in modes else mode)
   
while True:
    qtype = int(input("Enter qtype of query(1/2):"))
    if qtype == 1:
        len_inst = int(input("Enter length of instruction:"))
        len_reg = int(input("Enter length of register:"))
        print(f"Min number of bits to represent memory: {math.ceil(math.log2(num_addr))}")
        len_opcode = len_inst + len_reg + math.ceil(math.log2(num_addr))
        print(f"Number of bits for opcode: {len_opcode}")
        print(f"Number of filler bits for Instruction 2: {len_opcode - len_inst - 2*len_reg}")
        print(f"Max number of instructions: {2**len_inst}")
        print(f"Max number of registers: {2**len_reg}")
    elif qtype == 2:
        sub_type = int(input("Enter subtype of query(1/2):"))
        if sub_type == 1:
            bits = int(input("bit-size of CPU?"))
            print('''Enter how the memory is addressed:
            1. Bit addressable
            2. Nibble addressable
            3. Byte addressable
            4. Word addressable''')
            modes = {
                1: 1,
                2: 4,
                3: 8,
            }
            mode = int(input())
            mode = modes[mode] if mode in modes else bits
            print(f"{'+' if math.ceil(math.log2(num_addr)) < math.ceil(math.log2(num/mode)) else '-'}{abs(math.ceil(math.log2(num_addr)) - math.ceil(math.log2(num/mode)))}")
        elif sub_type == 2:
            num_bits = int(input("Enter number of bits CPU has:"))
            num_pins = int(input("Enter number of address pins CPU has:"))
            print('''Enter how the memory is addressed:
            1. Bit addressable
            2. Nibble addressable
            3. Byte addressable
            4. Word addressable''')
            modes = {
                1: 1,
                2: 4,
                3: 8,
            }
            mode = int(input())
            mode = modes[mode] if mode in modes else num_bits
            total_mem = 2**num_pins * mode / 8
            unit = 'B'
            if (total_mem > 2**30):
                total_mem /= 2**30
                unit = 'GB'
            elif (total_mem > 2**20):
                total_mem /= 2**20
                unit = 'MB'
            elif (total_mem > 2**10):
                total_mem /= 2**10
                unit = 'KB'
            print("Total memory:", total_mem, unit)
        else:
            raise ValueError("Invalid subtype")
    else:
        raise ValueError("Invalid qtype")
    to_continue = input("Continue?(y/n):")
    if to_continue == 'n':
        break


