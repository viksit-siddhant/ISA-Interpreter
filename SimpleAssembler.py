from typing import Optional


class Instruction:
    def __init__(self, _type: str, opcode: str, secondary_opcode: Optional[str]=None):
        self._type = _type
        self.opcode = opcode
        self.secondary_opcode = secondary_opcode

    def final_assemble(self, line: str):
        try:
            match self._type:
                case "A":
                    _, r0, r1, r2 = line.split()
                    return f"{self.opcode}00{handle_register(r0)}{handle_register(r1)}{handle_register(r2)}"
                case "B":
                    _, r0, imm = line.split()
                    return f"{self.opcode}{handle_register(r0)}{handle_immediate(imm[1:])}"
                case "C":
                    _, r0, r1 = line.split()
                    return f"{self.opcode}00000{handle_register(r0, flags_allowed=(self.opcode=='10011'))}{handle_register(r1)}"
                case "D":
                    _, r0, addr = line.split()
                    return f"{self.opcode}{handle_register(r0)}{handle_address(addr)}"
                case "E":
                    _, addr = line.split()
                    return f"{self.opcode}000{handle_address(addr)}"
                case "F":
                    return f"{self.opcode}{'0' * 11}"
        except ValueError:
            throw_error("Syntax", "Invalid syntax encountered on Line {}")

    def assemble(self, line: str):
        if self.secondary_opcode is not None and "$" in line:
            self._type = "B"
            temp = self.opcode
            self.opcode = self.secondary_opcode
            machine_code = self.final_assemble(line)
            self._type = "C"
            self.opcode = temp
            return machine_code
        else:
            return self.final_assemble(line)


def throw_error(error: str, message: str):
    print(f"Error//{error}: {message.format(LINE_NUM)}")
    try:
        print(f"Traceback: {ASSEMBLY_CODE[LINE_NUM-1]}")
        print("^".rjust(12))
    except IndexError:
        pass
    finally:
        quit()


def handle_register(register: str, flags_allowed: Optional[bool]=False):
    if register == "FLAGS":
        if not flags_allowed:
            throw_error("FLAGS", "Illegal use of FLAGS Register on Line {}")
        else:
            return "111"
    else:
        register = int(register.lstrip("R"))
        if register >= 7:
            throw_error("Register", "Invalid Register name used on Line {}")
        else:
            return bin(int(register))[2:].zfill(3)


def handle_immediate(immediate: str):
    if not immediate.isdigit():
        throw_error("Syntax", "Invalid Immediate value used on Line {} - must be an integer")
    immediate = bin(int(immediate))[2:]
    if len(immediate) > 8:
        throw_error("Overflow", "Immediate value used on Line {} is too large")
    else:
        return immediate.zfill(8)


def handle_address(address: str):
    if address.isdigit():
        if set(address) not in [{"0", "1"}, {"0"}, {"1"}]:
            throw_error("Memory-Address", "Invalid Address used on Line {}")
        if len(address) > 8:
            throw_error("Memory-Address", "Address longer than 8 bits used on Line {}")
        if not 0 <= int(address, base=2) < len(ASSEMBLY_CODE):
            throw_error("Memory-Address", "Address out of range of program used on Line {}")
        return address
    else:
        address = VARIABLES.get(address) if address in VARIABLES else LABELS.get(address)
        if address is None:
            throw_error("Address-Not-Found", "Undeclared Variable / Label used on Line {}")
        else:
            return bin(address)[2:].zfill(8)


INSTRUCTIONS: dict[str, Instruction] = {
    "ld": Instruction("D", "10100"),
    "st": Instruction("D", "10101"),
    "rs": Instruction("B", "11000"),
    "ls": Instruction("B", "11001"),
    "or": Instruction("A", "11011"),
    "je": Instruction("E", "01111"),
    "add": Instruction("A", "10000"),
    "sub": Instruction("A", "10001"),
    "mul": Instruction("A", "10110"),
    "div": Instruction("C", "10111"),
    "xor": Instruction("A", "11010"),
    "and": Instruction("A", "11100"),
    "not": Instruction("C", "11101"),
    "cmp": Instruction("C", "11110"),
    "jmp": Instruction("E", "11111"),
    "jlt": Instruction("E", "01100"),
    "jgt": Instruction("E", "01101"),
    "hlt": Instruction("F", "01010"),
    "mov": Instruction("C", "10011", "10010"),
}

MACHINE_CODE: list[str] = []
variables = codes = 0

temp_code: list[str] = []
counter = 0
while True:
    try:
        line = input().strip()
    except EOFError:
        break
    if line != "":
        temp_code.append(line)
        counter += 1 if "var" not in line else 0
        if "var" not in line:
            codes += 1
        else:
            variables += 1
    if variables + codes > 256:
        LINE_NUM = 256
        throw_error("Memory-Overflow", "256 Bytes Memory Limit Exceeded after Line {}")


ASSEMBLY_CODE: list[str] = []
VARIABLES: dict[str, int] = {}
program_begun = False

for LINE_NUM, line in enumerate(temp_code, start=1):
    if line[:3] == "var":
        if program_begun:
            throw_error("Syntax", "Variable declared on Line {}, not in the beginning")

        variable = line.split()[1]

        if not variable.isalnum() and not (not variable[0].isalpha() and variable[0] == "_"):
            throw_error("Syntax", "Invalid Variable name used on Line {}")
        elif counter > 256:
            throw_error("Memory-Overflow", "256 Bytes Memory Limit Exceeded after Line {}")
        else:
            VARIABLES[variable] = counter
            counter += 1
    else:
        program_begun = True
        ASSEMBLY_CODE.append(line)


LABELS: dict[str, int] = {}
for i, line in enumerate(ASSEMBLY_CODE):
    if ":" in line:
        label, code = line.split(":")
        if code == "":
            LINE_NUM = i+1
            throw_error("Syntax", "Empty Label Declaration encountered on Line {}")
        else:
            LABELS[label] = i


for LINE_NUM, line in enumerate(ASSEMBLY_CODE, start=1):
    line = line.split(":")[-1]
    operation = line.split()[0]

    if operation in INSTRUCTIONS:
        if operation == "hlt" and LINE_NUM != len(ASSEMBLY_CODE):
            throw_error("End-of-File", "Misuse of 'hlt' instruction on Line {}")

        if LINE_NUM == len(ASSEMBLY_CODE) and operation != "hlt":
            LINE_NUM += 1
            throw_error("End-of-File", "Missing 'hlt' instruction on Line {}")

        if operation[0] == "j" and line.split()[1] in VARIABLES:
            throw_error("Memory-Address", "Misuse of Variable as a Label on Line {}")

        if operation in ["ld", "st"] and line.split()[-1] in LABELS:
            throw_error("Memory-Address", "Misuse of Label as a Variable on Line {}")

        machine_code = INSTRUCTIONS[operation].assemble(line)
        MACHINE_CODE.append(machine_code)

    else:
        throw_error("Syntax", "Invalid operation encountered on Line {}")


for line in MACHINE_CODE:
    print(line)
