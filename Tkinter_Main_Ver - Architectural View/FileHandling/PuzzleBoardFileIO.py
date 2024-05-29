from PuzzleBoard import *
from GeneralExceptions import *

# Clase con funcionalidad para guardar un tablero "PuzzleBoard" en un archivo.
# Y para crear un tablero "PuzzleBoard" a partir de un archivo.
class PuzzleBoardFile():

    __BLACK_CIRCLE = 'B'
    __WHITE_CIRCLE = 'W'
    __DOT = 'D'

    # Extension de los archivos que serán guardados y abiertos. Puede cambiar.
    FILE_EXTENSION = 'txt'

    @classmethod
    def saveToFile(cls, filePath, puzzleBoard):
        puzzleBoardFileData = []

        numRows, numCols = puzzleBoard.getDimensions()
        for rowNum in range(0, numRows):
            line = "["
            for colNum in range(0, numCols):
                if (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    line += cls.__BLACK_CIRCLE
                elif (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    line += cls.__WHITE_CIRCLE
                else:
                    line += cls.__DOT
            line += "]\n"
            puzzleBoardFileData.append(line)

        try:
            with open(filePath, 'w') as filehandle:
                filehandle.writelines(puzzleBoardFileData)

        except Exception as e:
            raise MasyuFileSaveException("Error opening puzzle file") from e

    @classmethod
    def loadFile(cls, filePath):
        try:
            with open(filePath, 'r') as reader:
                allLines = reader.readlines()

        except Exception as e:
            raise MasyuFileOpenException("Error during opening Puzzle File") from e

        numCols = -1
        rowData = []
        for line in allLines:
            line = line.strip()
            length = len(line)

            if not (line.startswith("[")) or not (line.endswith("]")):
                raise MasyuInvalidPuzzleFileException("Invalid Puzzle File")
            else:
                line = line[1:(length - 1)]
                length = len(line)

            if (numCols == -1):
                numCols = length
            elif (numCols != length):
                raise MasyuInvalidPuzzleFileException("Mismatched row and/or column lengths in Puzzle File")

            for char in line:
                if not (char == cls.__DOT) and not (char == cls.__BLACK_CIRCLE) and not (char == cls.__WHITE_CIRCLE):
                    raise MasyuInvalidPuzzleFileException("Invalid character in Puzzle File")

            rowData.append(line)

        if not (PuzzleBoard.MIN_NUM_COLS <= numCols <= PuzzleBoard.MAX_NUM_COLS):
            raise MasyuInvalidPuzzleFileException("Invalid Puzzle Column Size")

        if not (PuzzleBoard.MIN_NUM_ROWS <= len(rowData) <= PuzzleBoard.MAX_NUM_ROWS):
            raise MasyuInvalidPuzzleFileException("Invalid Puzzle Row Size")

        newPuzzleBoard = PuzzleBoard(size=(len(rowData), numCols))

        for rowNum in range (0, len(rowData)):
            nextRow = rowData[rowNum]

            for colNum in range (0, numCols):
                nextChar = nextRow[colNum]
                if (nextChar == cls.__WHITE_CIRCLE):
                    newPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                elif (nextChar == cls.__BLACK_CIRCLE):
                    newPuzzleBoard.setBlackCircleAt(rowNum, colNum)

        return (newPuzzleBoard)

