class fun:
    def __init__(self):
        self.Id = ""
        self.Type = ""
        self.KNumParam = 1
        self.CallModule = ""
        self.GlobalName = ""

    def return_globalName(self):
        return self.GlobalName
    
    def assign_globalName(self,gn):
        self.GlobalName = gn
f=fun()