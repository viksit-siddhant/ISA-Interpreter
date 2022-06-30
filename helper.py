import variableHandler
from labelHandler import LabelHandler

var_handler = variableHandler.VariableHandler()
label_handler = LabelHandler()

def handle_vars(filename):
    #Get variable list
    file_counter = var_handler.execute(filename)
    #Convert variables to binary
    return file_counter

def handle_labels(filename):
    #Get label list
    label_handler.execute(filename)

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
        addr = bin(int(address))[2:]
    except Exception:
        if addr in var_handler.variables:
            addr =  var_handler.variables[address]
        elif address in label_handler.labels:
            addr = label_handler.labels[address]
        else:
            raise ValueError("Address not found")
        #Pad with zeros
    return addr.zfill(8)