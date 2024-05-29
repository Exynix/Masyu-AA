from ProcessingThread import *
from BoardCell import *
from GeneralExceptions import *

class DetermineCellsToDisableWorkThread(WorkThread):

    def __init__(self, solver, puzzleBoard, itemType):
        super().__init__(solver, puzzleBoard)

        self.__itemType = itemType

    def codeToRunInThread(self):
        clonedPuzzleBoard = self.pb.cloneBoardOnly()
        numRows, numCols = clonedPuzzleBoard.getDimensions()

        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):

                if (clonedPuzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    currentCell = Cell.TYPE_BLACK_CIRCLE
                elif (clonedPuzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    currentCell = Cell.TYPE_WHITE_CIRCLE
                else:
                    currentCell = Cell.TYPE_DOT

                if (self.__itemType == Cell.TYPE_BLACK_CIRCLE):
                    clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                elif (self.__itemType == Cell.TYPE_WHITE_CIRCLE):
                    clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                else:
                    clonedPuzzleBoard.setDotAt(rowNum, colNum)

                try:
                    self.solver.solve(clonedPuzzleBoard)
                except (MasyuSolverException, MasyuOrphanedRegionException) as e:

                    self.pb.setCellDisabled(rowNum, colNum)
                else:

                    self.pb.setCellEnabled(rowNum, colNum)
                finally:

                    if (currentCell == Cell.TYPE_BLACK_CIRCLE):
                        clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                    elif (currentCell == Cell.TYPE_WHITE_CIRCLE):
                        clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                    else:
                        clonedPuzzleBoard.setDotAt(rowNum, colNum)

                    clonedPuzzleBoard.clearSolution()