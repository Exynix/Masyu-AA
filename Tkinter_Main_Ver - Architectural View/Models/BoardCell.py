# Representa una celda del tablero.
class Cell():
    TYPE_DOT = 0
    TYPE_BLACK_CIRCLE = 1
    TYPE_WHITE_CIRCLE = 2

    # ------------ Constructor ------------
    def __init__(self, type = TYPE_DOT):
        self.type = type
        self.isCellEnabled = True
        self.isCellValid = True
        self.wasProcessed = False


    def clone(self):
        c = Cell(self.type)
        c.isCellEnabled = self.isCellEnabled
        c.isCellValid = self.isCellValid
        return(c)

    # ------------ Gettters y Setters------------

    def setProcessedFlag(self):
        self.wasProcessed = True

    def clearProcessedFlag(self):
        self.wasProcessed = False

    def wasCellProcessed(self):
        return (self.wasProcessed)

    def reset(self):
        self.type = Cell.TYPE_DOT
        self.isCellEnabled = True
        self.isCellValid = True

    def setAsBlackCircle(self):
        self.type = Cell.TYPE_BLACK_CIRCLE

    def setAsWhiteCircle(self):
        self.type = Cell.TYPE_WHITE_CIRCLE

    def setAsDot(self):
        self.type = Cell.TYPE_DOT

    # ------------ Funcinoes para saber el tipo de celda ------------
    def isBlackCircle(self):
        return(self.type == Cell.TYPE_BLACK_CIRCLE)

    def isWhiteCircle(self):
        return(self.type == Cell.TYPE_WHITE_CIRCLE)

    def isDot(self):
        return(self.type == Cell.TYPE_DOT)

    def isEnabled(self):
        return(self.isCellEnabled)

    def setEnabled(self):
        self.isCellEnabled = True

    def setDisabled(self):
        self.isCellEnabled = False

    def isValid(self):
        return(self.isCellValid)

    def setValid(self):
        self.isCellValid = True

    def setInvalid(self):
        self.isCellValid = False

    def getType(self):
        return(self.type)

    def print(self):
        if self.type == Cell.TYPE_DOT:
            print("D", end="")
        elif self.type == Cell.TYPE_BLACK_CIRCLE:
            print("B", end="")
        elif self.type == Cell.TYPE_WHITE_CIRCLE:
            print("W", end="")
        else:
            print("?", end="")
