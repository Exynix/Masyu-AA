class Pathway():
    TYPE_OPEN = 0
    TYPE_LINE = 1
    TYPE_BLOCKED = 2

    def __init__(self, type = TYPE_OPEN):
        self.type = type

    def clone(self):
        return(Pathway(self.type))

    def reset(self):
        self.type = Pathway.TYPE_OPEN

    def setAsLine(self):
        self.type = Pathway.TYPE_LINE

    def setAsBlocked(self):
        self.type = Pathway.TYPE_BLOCKED

    def setAsOpen(self):
        self.type = Pathway.TYPE_OPEN


    def isLine(self):
        return(self.type == Pathway.TYPE_LINE)

    def isBlocked(self):
        return(self.type == Pathway.TYPE_BLOCKED)

    def isOpen(self):
        return(self.type == Pathway.TYPE_OPEN)

    def getType(self):
        return(self.type)

    def print(self):
        if self.type == Pathway.TYPE_OPEN:
            print("O", end = "")
        elif self.type == Pathway.TYPE_LINE:
            print("L", end = "")
        elif self.type == Pathway.TYPE_BLOCKED:
            print("X", end = "")
        else:
            print("?", end = "")
