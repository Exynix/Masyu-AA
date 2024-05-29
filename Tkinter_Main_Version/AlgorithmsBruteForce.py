from ProcessingThread import *
from WindowProgress import *
from BoardUtilities import *
import time

# Implementaciones de métodos de fuerzaw bruta para dedicir los siguientes movimientos.
class BruteForceSolveWorkThread(WorkThread):

    # Define la dirección de la linea que será dibujada.
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self, solver, puzzleBoard):
        super().__init__(solver, puzzleBoard)

        self.__bruteForceResults = None
        self.__wasCancelledByUser = False

    # Busca el primer circulo negro que tenga una SOLA LINEA. Luego se determina en que dirección
    # se debería intentar dibujar la linea.
    def __findBlackCircleWithOneLine(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range (0, numRows):
            for colNum in range (0, numCols):
                if (pb.isBlackCircleAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 1):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u):
                            return((rowNum, colNum, self.UP))
                        if (d):
                            return((rowNum, colNum, self.DOWN))
                        if (l):
                            return((rowNum, colNum, self.LEFT))
                        if (r):
                            return((rowNum, colNum, self.RIGHT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    def __findWhiteCircleWithNoLines(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (pb.isWhiteCircleAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 0):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u and d):
                            return ((rowNum, colNum, self.UP))
                        if (l and r):
                            return ((rowNum, colNum, self.LEFT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    def __findBlackCircleWithNoLines(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (pb.isBlackCircleAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 0):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u):
                            return ((rowNum, colNum, self.UP))
                        if (d):
                            return ((rowNum, colNum, self.DOWN))
                        if (l):
                            return ((rowNum, colNum, self.LEFT))
                        if (r):
                            return ((rowNum, colNum, self.RIGHT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    def __findDotWithOneLine(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (pb.isDotAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 1):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u):
                            return ((rowNum, colNum, self.UP))
                        if (d):
                            return ((rowNum, colNum, self.DOWN))
                        if (l):
                            return ((rowNum, colNum, self.LEFT))
                        if (r):
                            return ((rowNum, colNum, self.RIGHT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    def __findNextGuess(self, pb):
        rowNum, colNum, direction = self.__findBlackCircleWithOneLine(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        rowNum, colNum, direction = self.__findWhiteCircleWithNoLines(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        rowNum, colNum, direction = self.__findBlackCircleWithNoLines(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        rowNum, colNum, direction = self.__findDotWithOneLine(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        return ((-1,-1,-1))

    def __findNextDirection(self, pb, lastGuess):
        rowNum, colNum, direction = lastGuess
        if (pb.isBlackCircleAt(rowNum, colNum) or pb.isDotAt(rowNum, colNum)):
            numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
            if (direction == self.UP):
                if (d):
                    return ((rowNum, colNum, self.DOWN))
                elif (l):
                    return ((rowNum, colNum, self.LEFT))
                elif (r):
                    return ((rowNum, colNum, self.RIGHT))

            elif (direction == self.DOWN):
                if (l):
                    return ((rowNum, colNum, self.LEFT))
                elif (r):
                    return ((rowNum, colNum, self.RIGHT))

            elif (direction == self.LEFT):
                if (r):
                    return ((rowNum, colNum, self.RIGHT))

        elif (pb.isWhiteCircleAt(rowNum, colNum)):
            numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
            if (direction == self.UP):
                if (l):
                    return ((rowNum, colNum, self.LEFT))

        return ((-1, -1, -1))

    def __applyNextGuess(self, pb, nextGuess):

        pbClone = pb.cloneAll()
        rowNum, colNum, direction = nextGuess

        if (direction == self.UP):
            self.solver.drawLineUpWrapper(pbClone,rowNum, colNum)
        elif (direction == self.DOWN):
            self.solver.drawLineDownWrapper(pbClone, rowNum, colNum)
        elif (direction == self.LEFT):
            self.solver.drawLineLeftWrapper(pbClone, rowNum, colNum)
        elif (direction == self.RIGHT):
            self.solver.drawLineRightWrapper(pbClone, rowNum, colNum)

        return(pbClone)

    __enableShowInterimResults = False

    def __showInterimResults(self, pb):

        if not (self.__enableShowInterimResults):
            return (True)

        self.__bruteForceResults = pb
        self.showResultsEvent.set()

        while ((not self.cancelEvent.isSet()) and (not self.resumeEvent.isSet())):
            time.sleep(0.1)

        if (self.cancelEvent.isSet()):
            self.cancelEvent.clear()
            self.__bruteForceResults = None
            self.__wasCancelledByUser = True
            return (False)
        else:
            self.resumeEvent.clear()
            return (True)

    def wasRequestCancelledByUser(self):
        return(self.__wasCancelledByUser)


    def codeToRunInThread(self):

        pbClone = self.pb.cloneAll()
        cloneStack = []
        cloneStack.append(pbClone)
        guessStack = []

        self.__wasCancelledByUser = False

        nextGuess = self.__findNextGuess(pbClone)
        rowNum, colNum, direction = nextGuess

        if ((rowNum == -1) and (colNum == -1)):

            self.__bruteForceResults = None
            return

        while (True):

            guessStack.append(nextGuess)
            pbClone = self.__applyNextGuess(pbClone, nextGuess)
            cloneStack.append(pbClone)

            if (self.__showInterimResults(pbClone) == False):
                return

            try:

                if (self.cancelEvent.isSet()):
                    self.cancelEvent.clear()
                    self.__bruteForceResults = None
                    self.__wasCancelledByUser = True
                    return

                self.solver.solve(pbClone)

                if (self.__showInterimResults(pbClone) == False):
                    return

            except Exception as e:

                rowNum = -1
                colNum = -1

            else:

                if (Utilities.checkIfPuzzleIsSolved(pbClone)):
                    self.__bruteForceResults = pbClone
                    return
                nextGuess = self.__findNextGuess(pbClone)
                rowNum, colNum, direction = nextGuess
            finally:
                while ((rowNum == -1) and (colNum == -1)):
                    if (len(guessStack) <= 0):

                        self.__bruteForceResults = None
                        return

                    cloneStack.pop()
                    lastGuess = guessStack.pop()
                    if (len(cloneStack) <= 0):
                        self.__bruteForceResults = None
                        return

                    pbClone = cloneStack[-1]
                    nextGuess = self.__findNextDirection(pbClone, lastGuess)
                    rowNum, colNum, direction = nextGuess

    # Retorna nada o "None" si no se encontro una solución.
    # Alternativamente, retorna un tablero con la solución.
    def getBruteForceResults(self):
        return(self.__bruteForceResults)
