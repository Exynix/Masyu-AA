from ProcessingThread import *
from BoardCell import *
from GeneralExceptions import *

# Esta clase determina qué celdas del tablero de rompecabezas deben ser deshabilitadas.
class DetermineCellsToDisableWorkThread(WorkThread):

    # Constructor de la clase. Inicializa la instancia con un solucionador, un tablero de rompecabezas y un tipo de elemento.
    def __init__(self, solver, puzzleBoard, itemType):
        super().__init__(solver, puzzleBoard)

        self.__itemType = itemType

    # Este es el código principal que se ejecuta en un hilo. Intenta reemplazar todas las celdas en el tablero, una por una.
    # Cada vez ejecuta el jugador sintético para ver si el tablero sigue siendo válido.
    # Si el solucionador arroja una excepción, entonces no se puede colocar un elemento en esa celda. Por lo tanto, se deshabilita esa celda.
    def codeToRunInThread(self):
        clonedPuzzleBoard = self.pb.cloneBoardOnly()
        numRows, numCols = clonedPuzzleBoard.getDimensions()

        # Itera sobre todas las celdas
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):

                # Guarda el tipo de celda actual
                if (clonedPuzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    currentCell = Cell.TYPE_BLACK_CIRCLE
                elif (clonedPuzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    currentCell = Cell.TYPE_WHITE_CIRCLE
                else:
                    currentCell = Cell.TYPE_DOT

                # Reemplaza la celda actual con el tipo de elemento
                if (self.__itemType == Cell.TYPE_BLACK_CIRCLE):
                    clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                elif (self.__itemType == Cell.TYPE_WHITE_CIRCLE):
                    clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                else:
                    clonedPuzzleBoard.setDotAt(rowNum, colNum)

                try:
                    # Intenta resolver el rompecabezas con el tablero modificado
                    self.solver.solve(clonedPuzzleBoard)
                except (MasyuSolverException, MasyuOrphanedRegionException) as e:
                    # Si el solucionador arroja una excepción, deshabilita la celda
                    self.pb.setCellDisabled(rowNum, colNum)
                else:
                    # Si el solucionador no arroja una excepción, habilita la celda
                    self.pb.setCellEnabled(rowNum, colNum)
                finally:
                    # Restaura el tipo de celda original y limpia la solución para la próxima iteración
                    if (currentCell == Cell.TYPE_BLACK_CIRCLE):
                        clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                    elif (currentCell == Cell.TYPE_WHITE_CIRCLE):
                        clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                    else:
                        clonedPuzzleBoard.setDotAt(rowNum, colNum)

                    clonedPuzzleBoard.clearSolution()