from HeuristicAislatedRegions import *

class Solver():
    def __init__(self):
        self.__orphanedRegionDetector = OrphanedRegions()

    def solve(self,puzzleBoard):
        changed = True

        while (changed):
            changed = False
            changed = changed or self.__processSpecialCases(puzzleBoard)

            changed = changed or self.__findPathwaysToBlock(puzzleBoard)

            changed = changed or self.__processDeadendPaths(puzzleBoard)

            changed = changed or self.__processBlackCircles(puzzleBoard)

            changed = changed or self.__processWhiteCircles(puzzleBoard)

            changed = changed or self.__addLines(puzzleBoard)

            changed = changed or self.__processSubPaths(puzzleBoard)

            if not (changed):

                changed = self.__orphanedRegionDetector.checkForOrphanedRegions(puzzleBoard)

    def __updateBlockedPathways(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

        if (lineCount == 2):
            if not(l):
                puzzleBoard.markBlockedLeft(rowNum, colNum)

            if not(r):
                puzzleBoard.markBlockedRight(rowNum, colNum)

            if not(u):
                puzzleBoard.markBlockedUp(rowNum, colNum)

            if not(d):
                puzzleBoard.markBlockedDown(rowNum, colNum)
        elif (lineCount > 2):
            raise MasyuSolverException("Cell has more than 2 lines", (rowNum, colNum))

    def drawLineLeftWrapper(self, puzzleBoard, rowNum, colNum):
        self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)

    def drawLineRightWrapper(self, puzzleBoard, rowNum, colNum):
        self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)

    def drawLineUpWrapper(self, puzzleBoard, rowNum, colNum):
        self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)

    def drawLineDownWrapper(self, puzzleBoard, rowNum, colNum):
        self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)

    def __drawLineLeftWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineLeftWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):

            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)

            if ((endingCol == (colNum - 1)) and (endingRow == rowNum)):
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException ("lineLeftWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        puzzleBoard.drawLineLeft(rowNum, colNum)

        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, rowNum, (colNum - 1))

    def __drawLineRightWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineRightWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):

            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)

            if ((endingCol == (colNum + 1)) and (endingRow == rowNum)):
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException("lineRightWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        puzzleBoard.drawLineRight(rowNum, colNum)

        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, rowNum, (colNum + 1))

    def __drawLineUpWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineUpWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):

            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)

            if ((endingCol == colNum) and (endingRow == (rowNum - 1))):
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException("lineUpWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        puzzleBoard.drawLineUp(rowNum, colNum)

        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, (rowNum - 1), colNum)

    def __drawLineDownWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineDownWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):

            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)

            if ((endingCol == colNum) and (endingRow == (rowNum + 1))):
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException("lineDownWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        puzzleBoard.drawLineDown(rowNum, colNum)

        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, (rowNum + 1), colNum)

    def __moveToNextCell(self, puzzleBoard, row, col, prevRow, prevCol, numCirclesVisited):

        if not (puzzleBoard.isDotAt(row, col)):
            numCirclesVisited += 1

        lineCount, l, r, u, d = puzzleBoard.getLines(row, col)

        if (lineCount == 1):

            return ((row, col, numCirclesVisited))
        else:

            if ((l) and ((prevRow != row) or (prevCol != (col - 1)))):
                return (self.__moveToNextCell(puzzleBoard, row, (col - 1), row, col, numCirclesVisited))

            if (r) and ((prevRow != row) or (prevCol != (col + 1))):
                return (self.__moveToNextCell(puzzleBoard, row, (col + 1), row, col, numCirclesVisited))

            if (u) and ((prevCol != col) or (prevRow != (row - 1))):
                return (self.__moveToNextCell(puzzleBoard, (row - 1), col, row, col, numCirclesVisited))

            if (d) and ((prevCol != col) or (prevRow != (row + 1))):
                return (self.__moveToNextCell(puzzleBoard, (row + 1), col, row, col, numCirclesVisited))

    def __cellsAbut(self, r1, c1, r2, c2):

        if ((r2 == r1) and (c2 == (c1 - 1))):
            return (True)

        if ((r2 == r1) and (c2 == (c1 + 1))):
            return (True)

        if ((r2 == (r1 - 1)) and (c2 == c1)):
            return (True)

        if ((r2 == (r1 + 1)) and (c2 == c1)):
            return (True)

        return (False)

    def __drawLineBetweenCells(self, puzzleBoard, r1, c1, r2, c2):

        if ((r2 == r1) and (c2 == (c1 - 1))):
            if not (puzzleBoard.hasLineLeft(r1, c1)):

                self.__drawLineLeftWrapper(puzzleBoard, r1, c1)
                return (True)
            else:

                return (False)

        if ((r2 == r1) and (c2 == (c1 + 1))):
            if not (puzzleBoard.hasLineRight(r1, c1)):

                self.__drawLineRightWrapper(puzzleBoard, r1, c1)
                return (True)
            else:

                return (False)

        if ((r2 == (r1 - 1)) and (c2 == c1)):
            if not (puzzleBoard.hasLineUp(r1, c1)):

                self.__drawLineUpWrapper(puzzleBoard, r1, c1)
                return (True)
            else:

                return (False)

        if ((r2 == (r1 + 1)) and (c2 == c1)):
            if not (puzzleBoard.hasLineDown(r1, c1)):

                self.__drawLineDownWrapper(puzzleBoard, r1, c1)
                return (True)
            else:

                return (False)

        return (False)

    def __blockPathBetweenCells(self, puzzleBoard, r1, c1, r2, c2):

        if ((r2 == r1) and (c2 == (c1 - 1))):
            if not (puzzleBoard.isBlockedLeft(r1, c1)):

                puzzleBoard.markBlockedLeft(r1, c1)
                return (True)
            else:

                return (False)

        if ((r2 == r1) and (c2 == (c1 + 1))):
            if not (puzzleBoard.isBlockedRight(r1, c1)):

                puzzleBoard.markBlockedRight(r1, c1)
                return (True)
            else:

                return (False)

        if ((r2 == (r1 - 1)) and (c2 == c1)):
            if not (puzzleBoard.isBlockedUp(r1, c1)):

                puzzleBoard.markBlockedUp(r1, c1)
                return (True)
            else:

                return (False)

        if ((r2 == (r1 + 1)) and (c2 == c1)):
            if not (puzzleBoard.isBlockedDown(r1, c1)):

                puzzleBoard.markBlockedDown(r1, c1)
                return (True)
            else:

                return (False)

        return (False)

    def __numConsecutiveWhiteCirclesInCol(self, puzzleBoard, rowNum, colNum):

        if ((rowNum == 0) or (rowNum > 0) and not (puzzleBoard.isWhiteCircleAt((rowNum - 1), colNum))):

            count = 0
            numRows, numCols = puzzleBoard.getDimensions()
            for i in range(rowNum, numRows):
                if (puzzleBoard.isWhiteCircleAt(i, colNum)):
                    count += 1
                else:
                    return (True, count)

            return (True, count)
        else:
            return (False, -1)

    def __numConsecutiveWhiteCirclesInRow(self, puzzleBoard, rowNum, colNum):

        if ((colNum == 0) or (colNum > 0) and not (puzzleBoard.isWhiteCircleAt(rowNum, (colNum - 1)))):

            count = 0
            numRows, numCols = puzzleBoard.getDimensions()
            for i in range(colNum, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum, i)):
                    count += 1
                else:
                    return (True, count)

            return (True, count)
        else:
            return (False, -1)

    def __processSpecialCases(self, puzzleBoard):

        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if(puzzleBoard.isWhiteCircleAt(rowNum, colNum)):

                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInCol(puzzleBoard, rowNum, colNum)

                    if (iAmFirst and (count > 2)):
                        if ((colNum > 0) and (colNum < (numCols - 1))):

                            if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line up in special case 9", (rowNum, colNum))
                            elif not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                    changesMade = True

                            for i in range(rowNum, (rowNum + count)):
                                if (puzzleBoard.hasLineDown(i, colNum)):
                                    raise MasyuSolverException("Unexpected line down in special case 9", (i, colNum))
                                elif not (puzzleBoard.isBlockedDown(i, colNum)):
                                    puzzleBoard.markBlockedDown(i, colNum)
                                    changesMade = True

                        else:
                            raise MasyuSolverException("Invalid white circle location in special case 9-1", (rowNum, colNum))

                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInRow(puzzleBoard, rowNum, colNum)

                    if (iAmFirst and (count > 2)):
                        if ((rowNum > 0) and (rowNum < (numRows - 1))):

                            if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line left in special case 9", (rowNum, colNum))
                            elif not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True

                            for i in range(colNum, (colNum + count)):
                                if (puzzleBoard.hasLineRight(rowNum, i)):
                                    raise MasyuSolverException("Unexpected line right in special case 9", (rowNum, i))
                                elif not (puzzleBoard.isBlockedRight(rowNum, i)):
                                    puzzleBoard.markBlockedRight(rowNum, i)
                                    changesMade = True

                        else:
                            raise MasyuSolverException("Invalid white circle location in special case 9-2", (rowNum, colNum))

                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInCol(puzzleBoard, rowNum, colNum)

                    if (iAmFirst and (count == 2)):

                        if (rowNum > 1):
                            if (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                                if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in Case 14-1", (rowNum, colNum))
                                elif (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                    raise MasyuSolverException("Unexpected line down in Case 14-1", ((rowNum + 1), colNum))
                                else:
                                    if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                        puzzleBoard.markBlockedUp(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedDown((rowNum + 1), colNum)):
                                        puzzleBoard.markBlockedDown((rowNum + 1), colNum)
                                        changesMade = True

                        if (rowNum < (numRows - 3)):
                            if (puzzleBoard.hasLineDown((rowNum + 2), colNum)):
                                if (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                    raise MasyuSolverException("Unexpected line down in Case 14-3", ((rowNum + 1), colNum))
                                elif (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in Case 14-3",(rowNum, colNum))
                                else:
                                    if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                        puzzleBoard.markBlockedUp(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedDown((rowNum + 1), colNum)):
                                        puzzleBoard.markBlockedDown((rowNum + 1), colNum)
                                        changesMade = True

                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInRow(puzzleBoard, rowNum, colNum)

                    if (iAmFirst and (count == 2)):

                        if (colNum > 1):
                            if (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                                if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in Case 14-2",(rowNum, colNum))
                                elif (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                    raise MasyuSolverException("Unexpected line right in Case 14-2",(rowNum, (colNum + 1)))
                                else:
                                    if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                        puzzleBoard.markBlockedLeft(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedRight(rowNum, (colNum + 1))):
                                        puzzleBoard.markBlockedRight(rowNum, (colNum + 1))
                                        changesMade = True

                        if (colNum < (numCols - 3)):
                            if (puzzleBoard.hasLineRight(rowNum, (colNum + 2))):
                                if (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                    raise MasyuSolverException("Unexpected line right in Case 14-4",(rowNum, (colNum + 1)))
                                elif (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in Case 14-4",(rowNum, colNum))
                                else:
                                    if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                        puzzleBoard.markBlockedLeft(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedRight(rowNum, (colNum + 1))):
                                        puzzleBoard.markBlockedRight(rowNum, (colNum + 1))
                                        changesMade = True

                    if (1 < rowNum < (numRows - 2)):
                        if ((puzzleBoard.hasLineUp((rowNum - 1), colNum)) and (puzzleBoard.hasLineDown((rowNum + 1), colNum))):
                            if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line up in Case 15-1", (rowNum, colNum))
                            if (puzzleBoard.hasLineDown(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line down in Case 15-1", (rowNum, colNum))
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True

                    if (1 < colNum < (numCols - 2)):
                        if ((puzzleBoard.hasLineLeft(rowNum, (colNum - 1)) and (puzzleBoard.hasLineRight(rowNum, (colNum + 1))))):
                            if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line left in Case 15-2",(rowNum, colNum))
                            if (puzzleBoard.hasLineRight(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line right in Case 15-2",(rowNum, colNum))
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True

                elif (puzzleBoard.isBlackCircleAt(rowNum, colNum)):

                    if ((colNum > 0) and (colNum < (numCols - 1)) and (rowNum < (numRows - 1))):
                       if (puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum - 1)) and
                               puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum + 1))):
                            if (rowNum > 1):
                                if (puzzleBoard.hasLineDown(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line down in case 10-1", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                    puzzleBoard.markBlockedDown(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-1", (rowNum, colNum))

                    if ((rowNum > 0) and (rowNum < (numRows - 1)) and (colNum > 0)):
                       if (puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum - 1)) and
                               puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum - 1))):
                            if (colNum < (numCols - 2)):
                                if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in case 10-2", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                    puzzleBoard.markBlockedLeft(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-2", (rowNum, colNum))

                    if ((colNum > 0) and (colNum < (numCols - 1)) and (rowNum > 0)):
                       if (puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum - 1)) and
                               puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum + 1))):
                            if (rowNum < (numRows - 2)):
                                if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in case 10-3", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-3", (rowNum, colNum))

                    if ((rowNum > 0) and (rowNum < (numRows - 1)) and (colNum < (numCols - 1))):
                        if (puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum + 1)) and
                                puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum + 1))):
                            if (colNum > 1):
                                if (puzzleBoard.hasLineRight(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line right in case 10-4", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-4", (rowNum, colNum))

                    if (rowNum < (numRows - 3)):
                        if ((puzzleBoard.isDotAt((rowNum + 1), colNum)) and
                                puzzleBoard.isWhiteCircleAt((rowNum + 2), colNum) and
                                puzzleBoard.isWhiteCircleAt((rowNum + 3), colNum)):
                            if (rowNum > 1):
                                if (puzzleBoard.hasLineDown(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line down in case 12-1", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                    puzzleBoard.markBlockedDown(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-1", (rowNum, colNum))

                    if (colNum > 2):
                        if ((puzzleBoard.isDotAt(rowNum, (colNum - 1)) and
                                puzzleBoard.isWhiteCircleAt(rowNum, (colNum - 2)) and
                                puzzleBoard.isWhiteCircleAt(rowNum, (colNum - 3)))):
                            if (colNum < (numCols - 2)):
                                if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in case 12-2", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                    puzzleBoard.markBlockedLeft(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-2", (rowNum, colNum))

                    if (rowNum > 2):
                        if ((puzzleBoard.isDotAt((rowNum - 1), colNum)) and
                                puzzleBoard.isWhiteCircleAt((rowNum - 2), colNum) and
                                puzzleBoard.isWhiteCircleAt((rowNum - 3), colNum)):
                            if (rowNum < (numRows - 2)):
                                if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in case 12-3", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-3", (rowNum, colNum))

                    if (colNum < (numCols - 3)):
                        if ((puzzleBoard.isDotAt(rowNum, (colNum + 1)) and
                             puzzleBoard.isWhiteCircleAt(rowNum, (colNum + 2)) and
                             puzzleBoard.isWhiteCircleAt(rowNum, (colNum + 3)))):
                            if (colNum > 1):
                                if (puzzleBoard.hasLineRight(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line right in case 12-4", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-4", (rowNum, colNum))

    def __findPathwaysToBlock(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False

        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)

                    if (lineLeft and lineRight and (colNum > 1)):
                        if (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                            if not (puzzleBoard.isBlockedRight(rowNum, (colNum + 1))):
                                puzzleBoard.markBlockedRight(rowNum, (colNum + 1))
                                changesMade = True

                    if (lineLeft and lineRight and (colNum < (numCols - 2))):
                        if (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                             if not (puzzleBoard.isBlockedLeft(rowNum, (colNum - 1))):
                                 puzzleBoard.markBlockedLeft(rowNum, (colNum - 1))
                                 changesMade = True

                    if (lineUp and lineDown and (rowNum > 1)):
                        if (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                            if not (puzzleBoard.isBlockedDown((rowNum + 1), colNum)):
                                puzzleBoard.markBlockedDown((rowNum + 1), colNum)
                                changesMade = True

                    if (lineUp and lineDown and (rowNum < (numRows - 2))):
                        if (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                            if not (puzzleBoard.isBlockedUp((rowNum - 1), colNum)):
                                puzzleBoard.markBlockedUp((rowNum - 1), colNum)
                                changesMade = True

        for rowNum in range(0, numRows):
             for colNum in range(0, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)

                    if (lineUp or lineDown):
                        if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                            puzzleBoard.markBlockedLeft(rowNum, colNum)
                            changesMade = True

                        if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                            puzzleBoard.markBlockedRight(rowNum, colNum)
                            changesMade = True

                    if (lineLeft or lineRight):
                        if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                            puzzleBoard.markBlockedUp(rowNum, colNum)
                            changesMade = True

                        if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                            puzzleBoard.markBlockedDown(rowNum, colNum)
                            changesMade = True

        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):

                numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)
                if (puzzleBoard.isDotAt(rowNum, colNum)):
                    if (numLines == 2):
                        if not (lineLeft):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                        if not (lineUp):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                        if not (lineRight):
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                        if not (lineDown):
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True

                elif (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    if (numLines == 2):
                        if (lineLeft and lineRight):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True
                        elif (lineUp and lineDown):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                        else:
                            raise MasyuSolverException("Invalid turn in white circle", (rowNum, colNum))

                elif (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    if (numLines == 2):
                        if (lineLeft and lineUp):
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True
                        elif (lineUp and lineRight):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True
                        elif (lineRight and lineDown):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                        elif (lineLeft and lineDown):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                        else:
                            raise MasyuSolverException("Missing turn in black circle", (rowNum, colNum))

        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isBlackCircleAt(rowNum, colNum)):

                    if (colNum > 0):
                        if (puzzleBoard.hasLineUp(rowNum, (colNum - 1)) or puzzleBoard.hasLineDown(rowNum, (colNum - 1))):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True

                    if (colNum < (numCols - 1)):
                        if (puzzleBoard.hasLineUp(rowNum, (colNum + 1)) or puzzleBoard.hasLineDown(rowNum, (colNum + 1))):
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True

                    if (rowNum > 0):
                        if (puzzleBoard.hasLineLeft((rowNum - 1), colNum) or puzzleBoard.hasLineRight((rowNum - 1), colNum)):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True

                    if (rowNum < (numRows - 1)):
                        if (puzzleBoard.hasLineLeft((rowNum + 1), colNum) or puzzleBoard.hasLineRight((rowNum + 1), colNum)):
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True

        return (changesMade)

    def __processDeadendPaths(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        deadEndFound = True
        while deadEndFound:
            deadEndFound = False
            for rowNum in range(0, numRows):
                for colNum in range(0, numCols):
                    if (puzzleBoard.isDotAt(rowNum, colNum)):
                        count, l, r, u, d = puzzleBoard.getBlockedPaths(rowNum, colNum)

                        if (count == 3):
                            numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)
                            if (numLines != 0):
                                raise MasyuSolverException("Unexpected line at dead-end", (rowNum, colNum))
                            else:
                                if not (l):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedLeft(rowNum, colNum)
                                    changesMade = True
                                elif not (r):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                                    changesMade = True
                                elif not (u):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                    changesMade = True
                                elif not (d):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedDown(rowNum, colNum)
                                    changesMade = True

            changesMade = changesMade | deadEndFound

        return (changesMade)

    def __processBlackCircles(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    if (puzzleBoard.isBlockedLeft(rowNum, colNum) or
                        ((colNum > 0) and puzzleBoard.isBlockedLeft(rowNum, (colNum - 1)))):
                        if (colNum > (numCols - 3)) or \
                                puzzleBoard.isBlockedRight(rowNum, colNum) or \
                                puzzleBoard.isBlockedRight(rowNum, (colNum + 1)):
                            raise MasyuSolverException("Black Circle Blocked L/R", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineRight(rowNum, colNum)):
                                changesMade = True

                                self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                changesMade = True

                                self.__drawLineRightWrapper(puzzleBoard, rowNum, (colNum + 1))

                    if (puzzleBoard.isBlockedRight(rowNum, colNum) or
                        ((colNum < (numCols - 1) and puzzleBoard.isBlockedRight(rowNum, (colNum + 1))))):
                        if ((colNum < 2) or \
                                puzzleBoard.isBlockedLeft(rowNum, colNum) or \
                                puzzleBoard.isBlockedLeft(rowNum, (colNum - 1))):
                            raise MasyuSolverException("Black Circle Blocked L/R - 2", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                changesMade = True

                                self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                                changesMade = True

                                self.__drawLineLeftWrapper(puzzleBoard, rowNum, (colNum - 1))

                    if (puzzleBoard.isBlockedUp(rowNum, colNum) or
                        ((rowNum > 0) and puzzleBoard.isBlockedUp((rowNum - 1), colNum))):
                        if (rowNum > (numRows - 3)) or \
                                puzzleBoard.isBlockedDown(rowNum, colNum) or \
                                puzzleBoard.isBlockedDown((rowNum + 1), colNum):
                            raise MasyuSolverException("Black Circle Blocked U/D", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineDown(rowNum, colNum)):
                                changesMade = True

                                self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                changesMade = True

                                self.__drawLineDownWrapper(puzzleBoard, (rowNum + 1), colNum)

                    if (puzzleBoard.isBlockedDown(rowNum, colNum) or
                        ((rowNum < (numRows - 1)) and puzzleBoard.isBlockedDown((rowNum + 1), colNum))):
                        if (rowNum < 2) or \
                                puzzleBoard.isBlockedUp(rowNum, colNum) or \
                                puzzleBoard.isBlockedUp((rowNum - 1), colNum):
                            raise MasyuSolverException("Black Circle Blocked U/D - 2", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineUp(rowNum, colNum)):
                                changesMade = True

                                self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                                changesMade = True

                                self.__drawLineUpWrapper(puzzleBoard, (rowNum - 1), colNum)

                    count, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

                    if (l):
                        if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedRight(rowNum, colNum)

                        if not (puzzleBoard.isBlockedUp(rowNum, (colNum - 1))):
                            changesMade = True
                            puzzleBoard.markBlockedUp(rowNum, (colNum - 1))

                        if not (puzzleBoard.isBlockedDown(rowNum, (colNum - 1))):
                            changesMade = True
                            puzzleBoard.markBlockedDown(rowNum, (colNum - 1))

                    if (r):
                        if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedLeft(rowNum, colNum)

                        if not (puzzleBoard.isBlockedUp(rowNum, (colNum + 1))):
                            changesMade = True
                            puzzleBoard.markBlockedUp(rowNum, (colNum + 1))

                        if not (puzzleBoard.isBlockedDown(rowNum, (colNum + 1))):
                            changesMade = True
                            puzzleBoard.markBlockedDown(rowNum, (colNum + 1))
                    if (u):
                        if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedDown(rowNum, colNum)
                        if not (puzzleBoard.isBlockedLeft((rowNum - 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedLeft((rowNum - 1), colNum)
                        if not (puzzleBoard.isBlockedRight((rowNum - 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedRight((rowNum - 1), colNum)
                    if (d):
                        if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedUp(rowNum, colNum)
                        if not (puzzleBoard.isBlockedLeft((rowNum + 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedLeft((rowNum + 1), colNum)
                        if not (puzzleBoard.isBlockedRight((rowNum + 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedRight((rowNum + 1), colNum)

        return (changesMade)

    def __processWhiteCircles(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum,colNum)):

                    if (puzzleBoard.isBlockedUp(rowNum,colNum) or puzzleBoard.isBlockedDown(rowNum,colNum)):
                        if ((colNum == 0) or (colNum == (numCols-1))):
                            raise MasyuSolverException("White circle cannot be in first or last column",
                                                       (rowNum, colNum))
                        elif (puzzleBoard.isBlockedLeft(rowNum, colNum) or
                              puzzleBoard.isBlockedRight(rowNum, colNum)):
                            raise MasyuSolverException("White circle blocked L/R", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                changesMade = True
                                self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineRight(rowNum, colNum)):
                                changesMade = True
                                self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                    elif (puzzleBoard.isBlockedLeft(rowNum,colNum) or puzzleBoard.isBlockedRight(rowNum,colNum)):
                        if ((rowNum == 0) or (rowNum == (numRows-1))):
                            raise MasyuSolverException("White circle cannot be in first or last row",
                                                       (rowNum, colNum))
                        elif (puzzleBoard.isBlockedUp(rowNum, colNum) or
                              puzzleBoard.isBlockedDown(rowNum, colNum)):
                            raise MasyuSolverException("White circle blocked U/D", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineUp(rowNum, colNum)):
                                changesMade = True
                                self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineDown(rowNum, colNum)):
                                changesMade = True
                                self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedRight(rowNum, colNum)

                    count, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                    if (count == 1):
                        if (l):
                            self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True
                        elif (r):
                            self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True
                        elif (u):
                            self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True
                        elif (d):
                            self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True

        return (changesMade)

    def __addLines(self, puzzleBoard):

        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isDotAt(rowNum, colNum)):
                    numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                    numOpenPaths, openL, openR, openU, openD = puzzleBoard.getOpenPaths(rowNum, colNum)

                    if ((numLines == 1) and (numOpenPaths == 1)):
                        changesMade = True
                        if (openL):
                            self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                        elif (openR):
                            self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                        elif (openU):
                            self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                        else:
                            self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)

        return (changesMade)

    def __processSubPath(self, puzzleBoard, rowNum, colNum):
        numCirclesVisited = 0

        numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

        puzzleBoard.setCellProcessedFlag(rowNum, colNum)

        if not (puzzleBoard.isDotAt(rowNum, colNum)):

            numCirclesVisited += 1
        if (l):
            result = self.__moveToNextCell(puzzleBoard, rowNum, colNum - 1, rowNum, colNum, numCirclesVisited)
        elif (r):
            result = self.__moveToNextCell(puzzleBoard, rowNum, colNum + 1, rowNum, colNum, numCirclesVisited)
        elif (u):
            result = self.__moveToNextCell(puzzleBoard, rowNum - 1, colNum, rowNum, colNum, numCirclesVisited)
        else:
            result = self.__moveToNextCell(puzzleBoard, rowNum + 1, colNum, rowNum, colNum, numCirclesVisited)

        endRowNum, endColNum, na = result
        puzzleBoard.setCellProcessedFlag(endRowNum, endColNum)

        return(result)

    def __processSubPaths(self, puzzleBoard):
        changesMade = False
        numRows, numCols = puzzleBoard.getDimensions()
        puzzleBoard.clearAllCellProcessedFlags()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):

                numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                if (numLines == 1):
                    if (puzzleBoard.wasCellProcessed(rowNum, colNum)):
                        continue
                    numCirclesVisited = 0
                    startingRow = rowNum
                    startingCol = colNum

                    if not (puzzleBoard.isDotAt(rowNum, colNum)):

                        numCirclesVisited += 1

                    result = self.__processSubPath(puzzleBoard, startingRow, startingCol)

                    endingRow, endingCol, numCirclesVisited = result
                    if (self.__cellsAbut(startingRow, startingCol, endingRow, endingCol)):
                        numCirclesInPuzzle = Utilities.getNumberOfCircles(puzzleBoard)
                        if (numCirclesInPuzzle == numCirclesVisited):
                            puzzleBoard.setSolved()
                            changesMade = changesMade | self.__drawLineBetweenCells(puzzleBoard, startingRow, startingCol, endingRow, endingCol)
                        else:
                            changesMade = changesMade | self.__blockPathBetweenCells(puzzleBoard, startingRow, startingCol, endingRow, endingCol)

        return (changesMade)