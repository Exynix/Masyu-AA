# Un pathway, o conexión, representa una conexión entre 2 celdas.
# Un pathway puede ser una línea, un bloqueo o una conexión abierta.

# Linea: Representa una conexión entre 2 celdas.
# Bloqueado: Camino o conexión bloqueda. Determinada por las reglas de juego.
# Abierto: Aun no se determina si la linea debería estar bloqueada, o si debería ser una linea.

class Pathway():
    TYPE_OPEN = 0
    TYPE_LINE = 1
    TYPE_BLOCKED = 2
# ------------ Constructor ------------
    def __init__(self, type = TYPE_OPEN):
        self.type = type

    def clone(self):
        return(Pathway(self.type))

    def reset(self):
        self.type = Pathway.TYPE_OPEN
# ------------ Gettters y Setters------------
    def setAsLine(self):
        self.type = Pathway.TYPE_LINE

    def setAsBlocked(self):
        self.type = Pathway.TYPE_BLOCKED

    def setAsOpen(self):
        self.type = Pathway.TYPE_OPEN

# ------------ Funcinoes para saber el tipo de pathway. ------------
    def isLine(self):
        return(self.type == Pathway.TYPE_LINE)

    def isBlocked(self):
        return(self.type == Pathway.TYPE_BLOCKED)

    def isOpen(self):
        return(self.type == Pathway.TYPE_OPEN)

    def getType(self):
        return(self.type)

    # Imprime el tipo de coneción. O = Abierto, L = Linea, X = Bloqueado. ? = Desconocido
    def print(self):
        if self.type == Pathway.TYPE_OPEN:
            print("O", end = "")
        elif self.type == Pathway.TYPE_LINE:
            print("L", end = "")
        elif self.type == Pathway.TYPE_BLOCKED:
            print("X", end = "")
        else:
            print("?", end = "")
