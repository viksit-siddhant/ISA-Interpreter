class LabelHandler:
    def __init__(self):
        self.labels = dict()
    
    def execute(self,file):
        with open(file) as f:
            for i,line in enumerate(f):
                if ':' in line:
                    addr = i
                    addr = bin(addr)[2:]
                    addr = addr.zfill(8)
                    self.labels[line.split(':')[0]] = addr