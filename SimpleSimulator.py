def program_counter(pc: int) -> str:
    # Returns the binary representation of the PC
    return bin(pc)[2:].zfill(8)


def register(name: str) -> int:
    # Returns the address of that register
    return int(name.lstrip("R"))


def register_file(name: str) -> str:
    if name == "FLAGS":
        return REGISTER_FILE[7]
    else:
        return REGISTER_FILE[register(name)]


def get_instruction(pc: int) -> str:
    return MACHINE_CODE[pc]


def current_state() -> None:
    print(program_counter(PC), *REGISTER_FILE)


def handle_overflow() -> None:
    REGISTER_FILE[7] = "0"*12 + "1000"


def handle_comparison(value1: int, value2: int) -> None:
    if value1 == value2:
        REGISTER_FILE[7] = "0"*12 + "0001"
    elif value1 > value2:
        REGISTER_FILE[7] = "0"*12 + "0010"
    else:
        REGISTER_FILE[7] = "0"*12 + "0100"


def type_A(instruction: str) -> list[str, str, str]:
    opcode = instruction[:5]
    reg1 = instruction[7:10]
    reg2 = instruction[10:13]
    reg3 = instruction[13:16]
    return REGISTERS[reg1], REGISTERS[reg2], REGISTERS[reg3]


def type_B(instruction: str) -> list[str, str]:
    opcode = instruction[:5]
    reg1 = instruction[5:8]
    imm = instruction[8:16]
    return REGISTERS[reg1], imm


def type_C(instruction: str) -> list[str, str]:
    opcode = instruction[:5]
    reg1 = instruction[10:13]
    reg2 = instruction[13:16]
    return REGISTERS[reg1], REGISTERS[reg2]


def type_D(instruction: str) -> list[str, str]:
    opcode = instruction[:5]
    reg1 = instruction[5:8]
    mem = instruction[8:16]
    return REGISTERS[reg1], mem


def type_E(instruction: str) -> str:
    opcode = instruction[:5]
    mem = instruction[8:16]
    return mem


def execution_engine(instruction: str, pc: int) -> tuple[int, bool]:
    opcode = instruction[:5]

    if opcode == "10000": #addition
        reg1, reg2, reg3 = type_A(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)

        value = bin(value1 + value2)[2:].zfill(16)

        if len(value) > 16:
            handle_overflow()
        else:
            REGISTER_FILE[register(reg3)] = value
            REGISTER_FILE[7] = "0" * 16

        pc = pc + 1


    elif opcode == "10001": #subtraction
        reg1, reg2, reg3 = type_A(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)

        value = bin(value1 - value2)[2:].zfill(16)

        if value1 < value2:
            handle_overflow()
            value = "0" * 16
        else:
            REGISTER_FILE[7] = "0" * 16

        REGISTER_FILE[register(reg3)] = value
        pc = pc + 1


    elif opcode == "10010": #move immediate
        reg1, imm = type_B(instruction)
        REGISTER_FILE[register(reg1)] = "0"*8 + imm
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "10011": #move register
        reg1, reg2 = type_C(instruction)
        value1 = int(register_file(reg1), base=2)
        REGISTER_FILE[register(reg2)] = bin(value1)[2:].zfill(16)
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "10100": #load
        reg1, mem = type_D(instruction)
        REGISTER_FILE[register(reg1)] = MEMORY[int(mem, base=2)]
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "10101": #store
        reg1, mem = type_D(instruction)
        MEMORY[int(mem, base=2)] = register_file(reg1)
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "10110": #multiply
        reg1, reg2, reg3 = type_A(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)

        value = bin(value1 * value2)[2:].zfill(16)

        if len(value) > 16:
            handle_overflow()
        else:
            REGISTER_FILE[register(reg3)] = value
            REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "10111": #divide
        reg3, reg4 = type_C(instruction)
        value3 = int(register_file(reg3), base=2)
        value4 = int(register_file(reg4), base=2)

        REGISTER_FILE[0] = bin(value3 // value4)[2:].zfill(16)
        REGISTER_FILE[1] = bin(value3 % value4)[2:].zfill(16)
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11000": #right shift
        reg1, imm = type_B(instruction)
        value1 = int(register_file(reg1), base=2)
        value1 >>= int(imm, base=2)
        REGISTER_FILE[register(reg1)] = bin(value1)[2:].zfill(16)
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11001": #left shift
        reg1, imm = type_B(instruction)
        value1 = int(register_file(reg1), base=2)
        value1 <<= int(imm, base=2)
        REGISTER_FILE[register(reg1)] = bin(value1)[2:].zfill(16)
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11010": #XOR
        reg1, reg2, reg3 = type_A(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)

        value = bin(value1 ^ value2)[2:].zfill(16)

        REGISTER_FILE[register(reg3)] = value
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11011": #OR
        reg1, reg2, reg3 = type_A(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)

        value = bin(value1 | value2)[2:].zfill(16)

        REGISTER_FILE[register(reg3)] = value
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11100": #AND
        reg1, reg2, reg3 = type_A(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)

        value = bin(value1 & value2)[2:].zfill(16)

        REGISTER_FILE[register(reg3)] = value
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11101": #invert
        reg1, reg2 = type_C(instruction)
        value1 = register_file(reg1).replace("0", "_").replace("1", "0").replace("_", "1")
        REGISTER_FILE[register(reg2)] = value1.zfill(16)
        REGISTER_FILE[7] = "0" * 16
        pc = pc + 1


    elif opcode == "11110": #compare
        reg1, reg2 = type_C(instruction)
        value1 = int(register_file(reg1), base=2)
        value2 = int(register_file(reg2), base=2)
        handle_comparison(value1, value2)
        pc = pc + 1


    elif opcode == "11111": #unconditional jump
        mem = type_E(instruction)
        pc = int(mem, base=2)
        REGISTER_FILE[7] = "0" * 16


    elif opcode == "01100": #jump if less than
        mem = type_E(instruction)
        pc = int(mem, base=2) if REGISTER_FILE[7][-3] == "1" else pc + 1
        REGISTER_FILE[7] = "0" * 16


    elif opcode == "01101": #jump if greater than
        mem = type_E(instruction)
        pc = int(mem, base=2) if REGISTER_FILE[7][-2] == "1" else pc + 1
        REGISTER_FILE[7] = "0" * 16


    elif opcode == "01111": #jump if equal
        mem = type_E(instruction)
        pc = int(mem, base=2) if REGISTER_FILE[7][-1] == "1" else pc + 1
        REGISTER_FILE[7] = "0" * 16


    else: # HALT => stop program
        return True, pc

    return False, pc


MACHINE_CODE: list[str] = []
line = None
while line != "0101000000000000":
    MACHINE_CODE.append(line := input())


MEMORY: list[str] = MACHINE_CODE.copy()
while len(MEMORY) != 256:
    MEMORY.append("0" * 16)


REGISTER_FILE: list[str] = ["0" * 16] * 8
HALTED: bool = False
PC: int = 0
PC_REGISTER: str = program_counter(PC)

REGISTERS: dict[str, str] = {
    "000": "R0", "001": "R1", "010": "R2", "011": "R3",
    "100": "R4", "101": "R5", "110": "R6", "111": "FLAGS"
}

while not HALTED:
    INSTRUCTION: str = get_instruction(PC)
    HALTED, new_PC = execution_engine(INSTRUCTION, PC)
    current_state()
    PC = new_PC


for mem in MEMORY:
    print(mem)