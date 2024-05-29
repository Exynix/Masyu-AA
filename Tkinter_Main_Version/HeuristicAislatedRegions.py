from GeneralExceptions import *
from BoardUtilities import *

class OrphanedRegions():

    START = 0
    END = 1

    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    TOP_RIGHT = 4
    TOP_LEFT = 5
    BOTTOM_RIGHT = 6
    BOTTOM_LEFT = 7
    TOP_BOTTOM = 8
    LEFT_RIGHT = 9

    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

    TOP_ROW = 0
    BOTTOM_ROW = 1
    LEFT_COLUMN = 2
    RIGHT_COLUMN = 3

    def hasLineOut(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_RIGHT)):
                return(pb.hasLineLeft(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or (edges == self.BOTTOM_RIGHT)):
                return(pb.hasLineUp(rowNum, colNum))
            elif ((edges == self.TOP_LEFT) or (edges == self.TOP_BOTTOM)):
                return(pb.hasLineRight(rowNum, colNum))
            elif (edges == self.LEFT_RIGHT):
                return(pb.hasLineDown(rowNum, colNum))
        else:
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or (edges == self.TOP_BOTTOM)):
                return(pb.hasLineRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or
                  (edges == self.TOP_RIGHT) or (edges == self.LEFT_RIGHT)):
                return(pb.hasLineDown(rowNum, colNum))
            elif (edges == self.BOTTOM_RIGHT):
                return(pb.hasLineLeft(rowNum, colNum))


        raise MasyuSolverException("hasLineOut(): unexpected condition encountered!!\n" + \
                                   "pointId=" + str(pointId) + "\n" + \
                                   "edges=" + str(edges), (rowNum, colNum))

    def hasLineIn(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_RIGHT)):
                return (pb.hasLineRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or (edges == self.BOTTOM_RIGHT)):
                return (pb.hasLineDown(rowNum, colNum))
            elif ((edges == self.TOP_LEFT) or (edges == self.TOP_BOTTOM)):
                return (pb.hasLineLeft(rowNum, colNum))
            elif (edges == self.LEFT_RIGHT):
                return (pb.hasLineUp(rowNum, colNum))
        else:
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or (edges == self.TOP_BOTTOM)):
                return (pb.hasLineLeft(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or (edges == self.TOP_RIGHT) or
                  (edges == self.LEFT_RIGHT)):
                return (pb.hasLineUp(rowNum, colNum))
            elif (edges == self.BOTTOM_RIGHT):
                return (pb.hasLineRight(rowNum, colNum))

        raise MasyuSolverException("hasLineIn(): unexpected condition encountered!!\n" + \
                                   "pointId=" + str(pointId) + "\n" + \
                                   "edges=" + str(edges), (rowNum, colNum))

    def isOpen(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_LEFT) or
                    (edges == self.TOP_RIGHT) or (edges == self.TOP_BOTTOM)):
                return (pb.isOpenLeft(rowNum, colNum) and pb.isOpenRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or
                  (edges == self.BOTTOM_RIGHT) or (edges == self.LEFT_RIGHT)):
                return (pb.isOpenUp(rowNum, colNum) and pb.isOpenDown(rowNum, colNum))
        else:
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or
                    (edges == self.BOTTOM_RIGHT) or (edges == self.TOP_BOTTOM)):
                return (pb.isOpenLeft(rowNum, colNum) and pb.isOpenRight(rowNum, colNum))
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or
                  (edges == self.TOP_RIGHT) or (edges == self.LEFT_RIGHT)):
                return (pb.isOpenUp(rowNum, colNum) and pb.isOpenDown(rowNum, colNum))

        raise MasyuSolverException("isOpen(): unexpected condition encountered!!\n" + \
                                   "pointId=" + str(pointId) + "\n" + \
                                   "edges=" + str(edges), (rowNum, colNum))

    def determineEdges(self, pb, startRow, startCol, endRow, endCol):
        numRows, numCols = pb.getDimensions()

        if (((startCol == 0) and (endCol == (numCols - 1))) or
             ((startCol == (numCols - 1)) and (endCol == 0))):
            return(self.LEFT_RIGHT)
        elif (((startRow == 0) and (endRow == (numRows - 1))) or
              ((startRow == (numRows - 1)) and (endRow == 0))):
            return(self.TOP_BOTTOM)
        elif (startRow == endRow):
            if (startRow == 0):
                return(self.TOP)
            else:
                return(self.BOTTOM)
        elif (startCol == endCol):
            if (startCol == 0):
                return(self.LEFT)
            else:
                return(self.RIGHT)
        elif (startRow == 0):
            if (endCol == 0):
                return(self.TOP_LEFT)
            else:
                return(self.TOP_RIGHT)
        elif (endRow == (numRows - 1)):
            if (startCol == 0):
                return(self.BOTTOM_LEFT)
            else:
                return(self.BOTTOM_RIGHT)

        raise MasyuOrphanedRegionException("determineEdges(): unexpected condition encountered!!", (startRow, startCol),
                                           (endRow, endCol))
    def determineQuadrant(self, numRows, numCols, rowNum, colNum):
        centerR = int(numRows / 2)
        centerC = int(numCols / 2)

        if ((rowNum <= centerR) and (colNum <= centerC)):
            return((self.Q1, -1, -1))
        elif ((rowNum <= centerR) and (colNum >= centerC)):
            return((self.Q2, -1, 1))
        elif ((rowNum >= centerR) and (colNum <= centerC)):
            return((self.Q3, 1, -1))
        else:
            return((self.Q4, 1, 1))

    def drawBoundaryLine(self, pb, region):
        lineStartRow, lineStartCol = region[0]

        for i in range(1, len(region)):
            lineEndRow, lineEndCol = region[i]

            if (lineStartRow == lineEndRow):
                if (lineStartCol < lineEndCol):
                    pb.drawLineRight(lineStartRow, lineStartCol)
                else:
                    pb.drawLineLeft(lineStartRow, lineStartCol)
            else:
                if (lineStartRow < lineEndRow):
                    pb.drawLineDown(lineStartRow, lineStartCol)
                else:
                    pb.drawLineUp(lineStartRow, lineStartCol)

            lineStartRow = lineEndRow
            lineStartCol = lineEndCol

    def markRowImpliedBoundary(self, pb, rowNum, colStart, colEnd):
        for colNum in range(colStart, colEnd):
            pb.setCellDisabled(rowNum, colNum)

    def markColImpliedBoundary(self, pb, colNum, rowStart, rowEnd):
        for rowNum in range(rowStart, rowEnd):
            pb.setCellDisabled(rowNum, colNum)

    def markImpliedBoundary(self, pb, edges, region):
        numRows, numCols = pb.getDimensions()
        regionStartRow, regionStartCol = region[0]
        regionEndRow, regionEndCol = region[-1]

        if (edges == self.TOP):
            self.markRowImpliedBoundary(pb, 0, (regionStartCol + 1), regionEndCol)
        elif (edges == self.BOTTOM):
            self.markRowImpliedBoundary(pb, (numRows - 1), (regionStartCol + 1), regionEndCol)
        elif (edges == self.RIGHT):
            self.markColImpliedBoundary(pb, (numCols - 1), (regionStartRow + 1), regionEndRow)
        elif (edges == self.LEFT):
            self.markColImpliedBoundary(pb, 0, (regionStartRow + 1), regionEndRow)
        elif (edges == self.TOP_RIGHT):
            self.markRowImpliedBoundary(pb, 0, (regionStartCol + 1), numCols)
            self.markColImpliedBoundary(pb, (numCols - 1), 0, regionEndRow)
        elif (edges == self.TOP_LEFT):
            self.markRowImpliedBoundary(pb, 0, 0, regionStartCol)
            self.markColImpliedBoundary(pb, 0, 0, regionEndRow)
        elif (edges == self.BOTTOM_RIGHT):
            self.markRowImpliedBoundary(pb, (numRows - 1), (regionEndCol + 1), numCols)
            self.markColImpliedBoundary(pb, (numCols - 1), (regionStartRow + 1), numRows)
        elif (edges == self.BOTTOM_LEFT):
            self.markRowImpliedBoundary(pb, (numRows - 1), 0, regionEndCol)
            self.markColImpliedBoundary(pb, 0, (regionStartRow + 1), numRows)
        elif (edges == self.TOP_BOTTOM):
            self.markRowImpliedBoundary(pb, 0, 0, regionStartCol)
            self.markColImpliedBoundary(pb, 0, 1, (numRows - 1))
            self.markRowImpliedBoundary(pb, (numRows - 1), 0, regionEndCol)
        else:
            self.markColImpliedBoundary(pb, 0, 0, regionStartRow)
            self.markRowImpliedBoundary(pb, 0, 1, (numCols - 1))
            self.markColImpliedBoundary(pb, (numCols - 1), 0, regionEndRow)

    def countCirclesInOrphanedRegion(self, pb, region, edges):
        clone = pb.cloneBoardOnly()
        Utilities.enableAllCells(clone)
        numRows, numCols = clone.getDimensions()

        self.drawBoundaryLine(clone, region)

        self.markImpliedBoundary(clone, edges, region)
        circlesOnBoundary = 0
        circlesInside = 0
        circlesOutside = 0

        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if not (clone.isDotAt(rowNum, colNum)):
                    numLines, l, r, u, d = clone.getLines(rowNum, colNum)
                    if (numLines > 0):
                        circlesOnBoundary += 1
                    elif not (clone.isCellEnabled(rowNum, colNum)):
                        circlesInside += 1
                    else:
                        quadrant, rowDelta, colDelta = self.determineQuadrant(numRows, numCols, rowNum, colNum)

                        crossings = 0
                        nextCellRowNum = rowNum
                        nextCellColNum = colNum

                        while ((0 <= nextCellRowNum <= (numRows -1)) and (0 <= nextCellColNum <= (numCols - 1))):
                            numLines, l, r, u, d = clone.getLines(nextCellRowNum, nextCellColNum)
                            if (numLines > 0):
                                if ((l and r) or (u and d)):
                                    crossings += 1
                                elif (quadrant == self.Q1):
                                    if ((l and u) or (r and d)):
                                        crossings += 1
                                    elif (((nextCellRowNum == 0) and ((crossings % 2) == 1) and d) or
                                          ((nextCellColNum == 0) and ((crossings % 2) == 1) and r)):
                                        crossings += 1
                                elif  (quadrant == self.Q4):
                                    if ((l and u) or (r and d)):
                                        crossings += 1
                                    elif (((nextCellRowNum == (numRows - 1)) and ((crossings % 2) == 1) and u) or
                                          ((nextCellColNum == (numCols - 1)) and ((crossings % 2) == 1) and l)):
                                        crossings += 1
                                elif (quadrant == self.Q2):
                                    if ((l and d) or (r and u)):
                                        crossings += 1
                                    elif (((nextCellRowNum == 0) and ((crossings % 2) == 1) and d) or
                                          ((nextCellColNum == (numCols - 1)) and ((crossings % 2) == 1) and l)):
                                        crossings += 1
                                elif (quadrant == self.Q3):
                                    if ((l and d) or (r and u)):
                                        crossings += 1
                                    elif (((nextCellRowNum == (numRows - 1)) and ((crossings % 2) == 1) and u) or
                                          ((nextCellColNum == 0) and ((crossings % 2) == 1) and r)):
                                        crossings += 1
                            elif not (clone.isCellEnabled(nextCellRowNum, nextCellColNum)):
                                crossings += 1
                            nextCellRowNum += rowDelta
                            nextCellColNum += colDelta

                        if ((crossings % 2) == 0):
                            circlesOutside += 1
                        else:
                            circlesInside += 1

        return((circlesOnBoundary, circlesInside, circlesOutside))

    def processPathway(self, pb, rowNum, colNum, nextCellRowOffset, nextCellColOffset, orphanedRegions):
        activePath = []
        activePath.append((rowNum, colNum))

        rowNum += nextCellRowOffset
        colNum += nextCellColOffset

        numRows, numCols = pb.getDimensions()

        while (True):
            pb.setCellProcessedFlag(rowNum, colNum)
            activePath.append((rowNum, colNum))
            if ((rowNum == 0) or (rowNum == (numRows - 1)) or (colNum == 0) or (colNum == (numCols - 1))):
                orphanedRegions.append(activePath)
                return(orphanedRegions)
            else:
                numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                nextCellRowOffset, nextCellColOffset = Utilities.chooseNextLineToFollow(nextCellRowOffset, nextCellColOffset,
                                                                                        l, r, u, d)
                if ((nextCellRowOffset == -1) and (nextCellColOffset == -1)):
                    return(orphanedRegions)
                else:
                    rowNum += nextCellRowOffset
                    colNum += nextCellColOffset

    def findOrphanedRegions(self, pb, startingPoint, orphanedRegions):
        numRows, numCols = pb.getDimensions()

        if (startingPoint == self.TOP_ROW):
            startRow = 0
            endRow = 1
            startCol = 1
            endCol = (numCols - 1)
        elif (startingPoint == self.BOTTOM_ROW):
            startRow = (numRows - 1)
            endRow = numRows
            startCol = 1
            endCol = (numCols - 1)
        elif (startingPoint == self.LEFT_COLUMN):
            startRow = 1
            endRow = (numRows - 1)
            startCol = 0
            endCol = 1
        else:
            startRow = 1
            endRow = (numRows - 1)
            startCol = (numCols - 1)
            endCol = numCols

        for rowNum in range(startRow, endRow):
            for colNum in range(startCol, endCol):
                if (pb.wasCellProcessed(rowNum, colNum)):
                    continue

                pb.setCellProcessedFlag(rowNum, colNum)

                numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                if (numLines == 0):
                    continue

                if (startingPoint == self.TOP_ROW):
                    if (d):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, 1, 0, orphanedRegions)
                elif (startingPoint == self.BOTTOM_ROW):
                    if (u):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, -1, 0, orphanedRegions)
                elif (startingPoint == self.LEFT_COLUMN):
                    if (r):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, 0, 1, orphanedRegions)
                else:
                    if (l):
                        orphanedRegions = self.processPathway(pb, rowNum, colNum, 0, -1, orphanedRegions)

        return(orphanedRegions)

    def blockPathIn(self, pb, pointId, edges, rowNum, colNum):
        if (pointId == self.START):
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.TOP_RIGHT)):
                pb.markBlockedRight(rowNum, colNum)
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.BOTTOM_LEFT) or (edges == self.BOTTOM_RIGHT)):
                pb.markBlockedDown(rowNum, colNum)
            elif ((edges == self.TOP_LEFT) or (edges == self.TOP_BOTTOM)):
                pb.markBlockedLeft(rowNum, colNum)
            elif (edges == self.LEFT_RIGHT):
                pb.markBlockedUp(rowNum, colNum)
        else:
            if ((edges == self.TOP) or (edges == self.BOTTOM) or (edges == self.BOTTOM_LEFT) or (edges == self.TOP_BOTTOM)):
                pb.markBlockedLeft(rowNum, colNum)
            elif ((edges == self.LEFT) or (edges == self.RIGHT) or (edges == self.TOP_LEFT) or (edges == self.TOP_RIGHT) or
                  (edges == self.LEFT_RIGHT)):
                pb.markBlockedUp(rowNum, colNum)
            elif (edges == self.BOTTOM_RIGHT):
                pb.markBlockedRight(rowNum, colNum)

    def normalizeRegions(self, pb, orphanedRegions):
        normalizedRegions = []
        numRows, numCols = pb.getDimensions()

        for region in orphanedRegions:
            startCellRowNum, startCellColNum = region[0]
            endCellRowNum, endCellColNum = region[-1]

            if ((startCellColNum == 0) and (endCellColNum == (numCols - 1)) and
                    (startCellRowNum > endCellRowNum)):
                normalizedRegion = region.reverse()
                normalizedRegions.append(normalizedRegion)
            else:
                normalizedRegions.append(region)

        return(normalizedRegions)

    def checkForOrphanedRegions(self, pb):
        orphanedRegions = []
        changesMade = False

        clone = pb.cloneAll()
        clone.clearAllCellProcessedFlags()

        orphanedRegions = self.findOrphanedRegions(clone, self.TOP_ROW, orphanedRegions)
        orphanedRegions = self.findOrphanedRegions(clone, self.LEFT_COLUMN, orphanedRegions)
        orphanedRegions = self.findOrphanedRegions(clone, self.RIGHT_COLUMN, orphanedRegions)
        orphanedRegions = self.findOrphanedRegions(clone, self.BOTTOM_ROW, orphanedRegions)

        orphanedRegions = self.normalizeRegions(clone, orphanedRegions)

        totalNumCircles = Utilities.getNumberOfCircles(clone)

        for region in orphanedRegions:
            startCell = region[0]
            endCell = region[-1]
            startCellRowNum, startCellColNum = startCell
            endCellRowNum, endCellColNum = endCell

            edges = self.determineEdges(clone, startCellRowNum, startCellColNum, endCellRowNum, endCellColNum)

            numBoundaryCircles, numCirclesInside, numCirclesOutside = self.countCirclesInOrphanedRegion(clone, region, edges)
            if ((numCirclesInside > 0) and (numCirclesOutside > 0)):
                raise MasyuOrphanedRegionException("Error 0 - found circles inside and outside an orphaned region",
                                                   startCell, endCell)
            if (self.hasLineIn(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineOut(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 7 - Invalid puzzle", startCell, endCell)
            elif (self.hasLineOut(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineIn(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 5 - Invalid puzzle", startCell, endCell)

            if ((numCirclesInside == 0) and (numCirclesOutside > 0)):
                if (self.isOpen(clone, self.START, edges, startCellRowNum, startCellColNum)):
                    self.blockPathIn(pb, self.START, edges, startCellRowNum, startCellColNum)
                    changesMade = True

                if (self.isOpen(clone, self.END, edges, endCellRowNum, endCellColNum)):
                    self.blockPathIn(pb, self.END, edges, endCellRowNum, endCellColNum)
                    changesMade = True

            if ((numCirclesInside > 0) and self.hasLineOut(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineOut(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 1 - Invalid puzzle", startCell, endCell)

            if ((numCirclesInside > 0) and self.hasLineOut(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.isOpen(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 2 - Invalid puzzle", startCell, endCell)

            if ((numCirclesInside > 0) and self.isOpen(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineOut(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 6 - Invalid puzzle", startCell, endCell)

            if ((numCirclesOutside > 0) and self.isOpen(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineIn(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 3 - Invalid puzzle", startCell, endCell)

            if ((numCirclesOutside > 0) and self.hasLineIn(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.isOpen(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 8 - Invalid puzzle", startCell, endCell)
            if ((numCirclesOutside > 0) and self.hasLineIn(clone, self.START, edges, startCellRowNum, startCellColNum) and
                self.hasLineIn(clone, self.END, edges, endCellRowNum, endCellColNum)):
                raise MasyuOrphanedRegionException("Error 9 - Invalid puzzle", startCell, endCell)

        return(changesMade)