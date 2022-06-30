import variableHandler

variablesHandler = variableHandler.VariableHandler()
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