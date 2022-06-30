class VariableHandler:
    def __init__(self):
        self.variables = {}
    def execute(self,file):
        programBegun = False
        val = 0
        with open(file) as f:
            for i,line in enumerate(f):
                if line[:3] == 'var':
                    if programBegun:
                        raise ValueError("Variable declaration after program begins")
                    var = line.split()[1]
                    self.variables[var] = True
                else:
                    if not programBegun:
                        val = i
                    programBegun = True
        return val
