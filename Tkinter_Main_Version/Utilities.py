class Utilities():

    @classmethod

    def chooseNextLineToFollow(cls, lastRowOffset, lastColOffset, l, r, u, d):

        if ((lastRowOffset == 1) and (lastColOffset == 0)):

            u = False
        elif ((lastRowOffset == -1) and (lastColOffset == 0)):

            d = False
        elif ((lastRowOffset == 0) and (lastColOffset == 1)):

            l = False
        elif ((lastRowOffset == 0) and (lastColOffset == -1)):

            r = False

        if (l):
            return((0, -1))
        elif (r):
            return((0, 1))
        elif (u):
            return((-1, 0))
        elif (d):
            return((1, 0))
        else:

            return((-1, -1))

    @classmethod
    def getNumberOfCircles(cls, puzzleBoard):
        numCircles = 0
        numRows, numCols = puzzleBoard.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if not (puzzleBoard.isDotAt(rowNum, colNum)):
                    numCircles += 1

        return (numCircles)

    @ classmethod
    def enableAllCells(cls, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                puzzleBoard.setCellEnabled(rowNum, colNum)

    @classmethod
    def checkIfPuzzleIsSolved(cls, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        numCirclesInPuzzle = Utilities.getNumberOfCircles(puzzleBoard)
        numCirclesFound = 0

        for rowNum in range (0, numRows):
            for colNum in range (0, numCols):

                numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

                if (0 < numLines < 2):
                    return(False)

                if (numLines == 0):
                    if (puzzleBoard.isDotAt(rowNum, colNum)):

                        continue
                    else:

                        return(False)

                if (u):
                    nextRowOffset = -1
                    nextColOffset = 0
                elif (d):
                    nextRowOffset = 1
                    nextColOffset = 0
                elif (l):
                    nextRowOffset = 0
                    nextColOffset = -1
                elif (r):
                    nextRowOffset = 0
                    nextColOffset = 1

                startingRowNum = rowNum
                startingColNum = colNum

                nextRowNum = rowNum + nextRowOffset
                nextColNum = colNum + nextColOffset

                if not (puzzleBoard.isDotAt(rowNum, colNum)):
                    numCirclesFound += 1

                while ((nextRowNum != startingRowNum) or (nextColNum != startingColNum)):
                    numLines, l, r, u, d = puzzleBoard.getLines(nextRowNum, nextColNum)

                    if (numLines < 2):
                        return (False)

                    nextRowOffset, nextColOffset = Utilities.chooseNextLineToFollow(nextRowOffset, nextColOffset, l, r, u, d)

                    if ((nextRowOffset == -1) and (nextColOffset == -1)):
                        return (False)

                    if not(puzzleBoard.isDotAt(nextRowNum, nextColNum)):
                        numCirclesFound += 1

                    nextRowNum = nextRowNum + nextRowOffset
                    nextColNum = nextColNum + nextColOffset

                if (numCirclesInPuzzle == numCirclesFound):
                    return(True)

                return(False)