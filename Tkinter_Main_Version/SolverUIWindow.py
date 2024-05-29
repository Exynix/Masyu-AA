from GetPuzzleBoardSizeDialog import *
from Solver import *
from FileIO import *
from ErrorDialog import *
from NoSolutionDialog import *
from BruteForceSolve import *
from DetermineCellsToDisableWorkThread import *

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class SolverUIWindow():

    # Estados de los archivos.
    STATE_1 = 1     # Sin  cambios, y nunca se guardo un archivo.
    STATE_2 = 2     # Cambiado y nunca se guardo un archivo.
    STATE_3 = 3     # Sin cambios desde la ultima apertura de archivo.
    STATE_4 = 4     # Cambiado desde la ultima apertura de archivo.
    STATE_5 = 5     # Sin cambios desde la ultima guardada.
    STATE_6 = 6     # Cambiado desde la ultima guardada.

    # Constantes para la creación y estética de elementos gráficos.
    NUM_ITEMS = 3                   
    ITEM_PADDING = 3                
    ITEM_HIGHLIGHT_THICKNESS = 2    
    ITEM_WIDTH = 30                 
    ITEM_HEIGHT = 30                
    MENU_ITEM_WHITE_CIRCLE_SIZE = 20      
    MENU_ITEM_BLACK_CIRCLE_SIZE = 20      
    MENU_ITEM_DOT_SIZE = 8               

    NO_ITEM = -1
    WHITE_ITEM = 0
    BLACK_ITEM = 1
    DOT_ITEM = 2

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN =3

    def __fileOpenHandler(self):

        try:
            status, newPuzzleBoard = FileIO.fileOpen(self.mainWindow, self.puzzleBoardObject)
            if (status):
                self.registerPuzzleBoard(newPuzzleBoard)

                self.__setWindowTitle(PuzzleStateMachine.getFileName())

                self.__setActiveItem(self.dotItem)

                self.__determineCellsToDisableInThread()

                try:
                    self.solver.solve(newPuzzleBoard)
                    print("File -> Open successful")

                    self.enableSmartPlacement['state'] = tk.NORMAL

                    if (Utilities.checkIfPuzzleIsSolved(newPuzzleBoard)):
                        print("puzzle solved")
                        newPuzzleBoard.setSolved()
                        self.bruteForceBtn['state'] = tk.DISABLED
                    else:
                        print("puzzle not solved")
                        newPuzzleBoard.setUnsolved()
                        self.bruteForceBtn['state'] = tk.NORMAL
                except Exception as e:

                    errorDialog = ErrorDialog(self.mainWindow)
                    errorDialog.showDialog("Invalid Puzzle File", str(e))

                    numRows, numCols = newPuzzleBoard.getDimensions()
                    newPuzzleBoard = PuzzleBoard(size=(numRows, numCols))
                    PuzzleStateMachine.reset()
                    self.registerPuzzleBoard(newPuzzleBoard)
                    self.__setWindowTitle(None)

                    self.__determineCellsToDisableInThread()

                    self.enableSmartPlacement['state'] = tk.NORMAL

                self.puzzleBoardCanvasManager.refreshCanvas()

        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save As")
        except MasyuFileOpenException as mfoe:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Opening Puzzle File", str(mfoe))
            print("Exception during File -> Open")
        except MasyuInvalidPuzzleFileException as mipfe:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Invalid Puzzle File", str(mipfe))
            print("Attempted to load invalid puzzle file")

    def __fileExitMenuHandler(self):

        try:
            status, unusedReturnValue = FileIO.fileExit(self.mainWindow, self.puzzleBoardObject)
            if(status):
                print("File -> Exit was successful")
                self.mainWindow.destroy()

        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Exit")

    def __fileSaveAsMenuHandler(self):

        try:
            status, unusedReturnValue = FileIO.fileSaveAs(self.mainWindow, self.puzzleBoardObject)
            if(status):
                print("File -> Save As successful")
                self.__setWindowTitle(PuzzleStateMachine.getFileName())

        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save As")

    def __fileSaveMenuHandler(self):

        try:
            status, unusedReturnValue = FileIO.fileSave(self.mainWindow, self.puzzleBoardObject)
            if(status):
                print("File -> Save successful")
                self.__setWindowTitle(PuzzleStateMachine.getFileName())

        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save")

    def __fileNewMenuHandler(self):
        try:
            status, unusedReturnValue = FileIO.fileNew(self.mainWindow, self.puzzleBoardObject)
            if not (status):
                return

        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save")
            return

        resizeResults = GetPuzzleBoardSizeDialog(self.mainWindow)
        rowVal, colVal = resizeResults.showDialog(self.numRows, self.numCols)
        print ("new puzzle size:", rowVal, colVal)
        if ((rowVal != -1) and (colVal != -1)):

            PuzzleStateMachine.reset()
            self.__setWindowTitle(None)

            self.bruteForceBtn['state'] = tk.DISABLED

            pb = PuzzleBoard(size=(rowVal, colVal))
            self.registerPuzzleBoard(pb)

            self.__determineCellsToDisableInThread()

            self.puzzleBoardCanvasManager.refreshCanvas()

            self.enableSmartPlacement['state'] = tk.NORMAL

    def __getItemBounds(self):
        x1 = 0
        y1 = 0
        x2 = (self.ITEM_WIDTH + (self.ITEM_HIGHLIGHT_THICKNESS * 2)) - 1
        y2 = (self.ITEM_HEIGHT + (self.ITEM_HIGHLIGHT_THICKNESS * 2)) - 1
        return(x1, y1, x2, y2)

    def __setWindowTitle(self, puzzleName):
        if (puzzleName == None):
            puzzleName = "<unnamed>"

        self.mainWindow.title("Maysu: " + puzzleName)

    def __itemSelectionHandler(self, event):

        item = event.widget

        if (item != self.selectedItem):
            self.__setActiveItem(item)

            self.__determineCellsToDisableInThread()

            self.puzzleBoardCanvasManager.refreshCanvas()

    def __setActiveItem(self, item):

        if (item == self.selectedItem):
            return

        if (self.selectedItem != None):
            self.selectedItem.itemconfigure('hilite', state='hidden')

        self.selectedItem = item
        item.itemconfigure('hilite', state='normal')

    def __createItem(self, parent, circleSize, circleColor):

        item = tk.Canvas(master=parent, relief=tk.FLAT, borderwidth=0, highlightthickness=0,
                                   height=(self.ITEM_HEIGHT + (2 * self.ITEM_HIGHLIGHT_THICKNESS)),
                                   width=(self.ITEM_WIDTH + (2 * self.ITEM_HIGHLIGHT_THICKNESS)),
                                   bg=self.itemCanvasColor)
        item.pack(side=tk.TOP)
        item.bind('<Button-1>', lambda event: self.__itemSelectionHandler(event))

        itemX1, itemY1, itemX2, itemY2 = self.__getItemBounds()
        print(itemX1, itemY1, itemX2, itemY2)
        itemCenterX = (itemX2 + 1) / 2
        itemCenterY = (itemY2 + 1) / 2
        x1 = itemCenterX - (circleSize / 2)
        y1 = itemCenterY - (circleSize / 2)
        x2 = x1 + circleSize
        y2 = y1 + circleSize
        item.create_oval(x1, y1, x2, y2, fill=circleColor)

        item.create_line(itemX1, itemY1, itemX2, itemY1,
                         itemX2, itemY2, itemX1, itemY2,
                         itemX1, itemY1, fill='red', tags=('hilite'))

        item.itemconfigure('hilite', state = 'hidden')

        return(item)

    def __createItems(self, parent):

        self.whiteItem = self.__createItem(parent, self.MENU_ITEM_WHITE_CIRCLE_SIZE, 'white')
        self.blackItem = self.__createItem(parent, self.MENU_ITEM_BLACK_CIRCLE_SIZE, 'black')
        self.dotItem = self.__createItem(parent, self.MENU_ITEM_DOT_SIZE, 'dark grey')

    def __showProgressCallback(self):
        self.puzzleBoardCanvasManager.setShowProgress(self.showProgressVar.get())

    def __showBlockedPathsCallback(self):
        self.puzzleBoardCanvasManager.setShowBlockedPaths(self.showBlockedPathsVar.get())

    def __smartPlacementModeCallback(self):
        if not (self.smartPlacementModeVar.get()):
            for rowNum in range(0, self.numRows):
                for colNum in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
        else:
            self.__determineCellsToDisableInThread()

        self.puzzleBoardCanvasManager.setShowDisabledCells(self.smartPlacementModeVar.get())

    def __determineCellsToDisableInThread(self):

        if not (self.smartPlacementModeVar.get()):
            for rowNum in range(0, self.numRows):
                for colNum in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
            return

        if (self.selectedItem == self.dotItem):
            for rowNum in range (0, self.numRows):
                for colNum in range (0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
            return

        if (self.selectedItem == self.blackItem):
            selectedItem = Cell.TYPE_BLACK_CIRCLE
        else:
            selectedItem = Cell.TYPE_WHITE_CIRCLE

        determineCellsToDisable = DetermineCellsToDisableWorkThread(self.solver, self.puzzleBoardObject, selectedItem)

        # workingWindow = WorkingWindow(self.mainWindow, determineCellsToDisable)

        determineCellsToDisable.start()
        # workingWindow.showWindow()

    # Llamado a métodos de fuerza bruta para solucionar los caminos que aún estan abiertos.
    def __tryBruteForceSolvingInThread(self):
        self.bruteForceBtn['state'] = tk.DISABLED

        self.__bruteForceSolver = BruteForceSolveWorkThread(self.solver, self.puzzleBoardObject)

        # self.__workingWindow = WorkingWindow(self.mainWindow, self.__bruteForceSolver)

        self.__bruteForceSolver.start()
        # self.__workingWindow.showWindow()

        bruteForceResult = self.__bruteForceSolver.getBruteForceResults()
        if (bruteForceResult != None):
            print("puzzle solved")
            bruteForceResult.setSolved()
            self.registerPuzzleBoard(bruteForceResult)

        else:
            print("No solution found")
            self.bruteForceBtn['state'] = tk.NORMAL
            dialog = NoSolutionDialog(self.mainWindow)
            dialog.showDialog()

    def __cellSelectionCallBack(self, rowNum, colNum):
        if not (self.puzzleBoardObject.isCellEnabled(rowNum, colNum)):
            self.mainWindow.bell()
        else:
            if ((self.selectedItem == self.blackItem) and
                    (self.puzzleBoardObject.isBlackCircleAt(rowNum, colNum))):
                return

            if ((self.selectedItem == self.whiteItem) and
                    (self.puzzleBoardObject.isWhiteCircleAt(rowNum, colNum))):
                return

            if ((self.selectedItem == self.dotItem) and
                    (self.puzzleBoardObject.isDotAt(rowNum, colNum))):
                return

            savedPuzzleBoard = self.puzzleBoardObject.cloneAll()

            if (self.selectedItem == self.blackItem):
                self.puzzleBoardObject.setBlackCircleAt(rowNum, colNum)
            elif (self.selectedItem == self.whiteItem):
                self.puzzleBoardObject.setWhiteCircleAt(rowNum, colNum)
            else:
                self.puzzleBoardObject.setDotAt(rowNum, colNum)

            self.puzzleBoardCanvasManager.refreshCanvas()

            self.puzzleBoardObject.clearSolution()
            for r in range(0, self.numRows):
                for c in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(r, c)
                    self.puzzleBoardObject.setCellValid(r, c)

            self.__determineCellsToDisableInThread()

            try:
                self.solver.solve(self.puzzleBoardObject)

                if not (self.smartPlacementModeVar.get()):
                    self.enableSmartPlacement['state'] = tk.DISABLED

                PuzzleStateMachine.puzzleChanged()

                if (Utilities.checkIfPuzzleIsSolved(self.puzzleBoardObject)):
                    print("puzzle solved")
                    self.puzzleBoardObject.setSolved()
                    self.bruteForceBtn['state'] = tk.DISABLED
                else:
                    print("puzzle not solved")
                    self.puzzleBoardObject.setUnsolved()
                    self.bruteForceBtn['state'] = tk.NORMAL

                self.puzzleBoardCanvasManager.refreshCanvas()

            except MasyuSolverException as e:

                self.puzzleBoardObject.setCellInvalid(rowNum, colNum)
                self.puzzleBoardCanvasManager.refreshCanvas()
                errorDialog = ErrorDialog(self.mainWindow)
                errorDialog.showDialog("Invalid Item Placement", "Cannot place item in the selected cell")
                self.registerPuzzleBoard(savedPuzzleBoard)

    def __init__(self):
        self.numRows = 0
        self.numCols = 0

        frame1Color = "light grey"
        self.itemCanvasColor = "grey"
        frame2Color = "light grey"
        puzzleBoardFrameColor = "light grey"
        puzzleBoardCanvasColor = "light grey"
        checkboxFrameColor = "light grey"
        checkboxColor = "light grey"

        self.state = SolverUIWindow.STATE_1
        self.puzzleBoardObject = None
        self.selectedItem = None

        self.mainWindow = tk.Tk()
        self.__setWindowTitle(None)

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.__fileExitMenuHandler)

        mainFrame = tk.Frame(master=self.mainWindow)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        frame1 = tk.Frame(master=mainFrame, height=100, width=30, bg=frame1Color)
        frame1.pack(fill=tk.Y, side=tk.LEFT)

        itemFrame = tk.Frame(master=frame1, relief=tk.RAISED, borderwidth=5, bg=self.itemCanvasColor)

        self.__createItems(itemFrame)
        self.__setActiveItem(self.dotItem)

        itemFrame.pack(fill=tk.X, side=tk.TOP, padx=15, pady=(75, 0))

        frame2 = tk.Frame(master=mainFrame, height=50, bg=frame2Color)
        frame2.pack(expand=True, fill=tk.BOTH, side=tk.TOP, ipadx=15, ipady=15)

        puzzleBoardFrame = tk.Frame(master=frame2, relief=tk.RAISED, borderwidth=5, bg=puzzleBoardFrameColor)
        puzzleBoardFrame.pack(side=tk.TOP, pady=(15, 0))

        puzzleBoardCanvas = tk.Canvas(master=puzzleBoardFrame, bg=puzzleBoardCanvasColor, height=300, width=300,
                                      highlightthickness=0, relief=tk.FLAT, borderwidth=0)
        puzzleBoardCanvas.pack(side=tk.TOP)
        self.puzzleBoardCanvas = puzzleBoardCanvas

        checkboxFrame = tk.Frame(master=frame2, bg=checkboxFrameColor, relief=tk.GROOVE, borderwidth=5)
        checkboxFrame.pack(pady=(15, 0))

        self.smartPlacementModeVar = tk.BooleanVar()
        self.smartPlacementModeVar.set(True)
        self.enableSmartPlacement = tk.Checkbutton(checkboxFrame, text="Smart placement mode",
                                              variable=self.smartPlacementModeVar,
                                              bg=checkboxColor, command=self.__smartPlacementModeCallback)
        self.enableSmartPlacement.pack(side=tk.BOTTOM, anchor=tk.W)

        self.showProgressVar = tk.BooleanVar()
        self.showProgressVar.set(True)
        showProgressCheckbox = tk.Checkbutton(checkboxFrame, text="Show progress", variable=self.showProgressVar,
                                              bg=checkboxColor, command=self.__showProgressCallback)
        showProgressCheckbox.pack(side=tk.TOP, anchor=tk.W)

        self.showBlockedPathsVar = tk.BooleanVar()
        self.showBlockedPathsVar.set(True)
        showBlockedPaths = tk.Checkbutton(checkboxFrame, text="Show blocked paths", variable=self.showBlockedPathsVar,
                                          bg=checkboxColor, command=self.__showBlockedPathsCallback)
        showBlockedPaths.pack(side=tk.BOTTOM, anchor=tk.W)

        buttonFrame = tk.Frame(master=frame2, bg=checkboxFrameColor, relief=tk.FLAT, borderwidth=0)
        buttonFrame.pack(pady=(15, 0))

        self.bruteForceBtn = tk.Button(master=buttonFrame, state=tk.DISABLED, text="Solve", padx=30,
                                       command=self.__tryBruteForceSolvingInThread)
        self.bruteForceBtn.pack()

        menubar = tk.Menu(self.mainWindow)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.__fileNewMenuHandler)
        filemenu.add_command(label="Open", command=self.__fileOpenHandler)
        filemenu.add_command(label="Save", command=self.__fileSaveMenuHandler)
        filemenu.add_command(label="Save As ..", command=self.__fileSaveAsMenuHandler)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__fileExitMenuHandler)
        menubar.add_cascade(label="File", menu=filemenu)

        self.mainWindow.config(menu=menubar)

        self.puzzleBoardCanvasManager = CanvasManager(self.puzzleBoardCanvas, self.showProgressVar.get(),
                                                      self.showBlockedPathsVar.get(), self.smartPlacementModeVar.get())
        self.puzzleBoardCanvasManager.registerCellSelectionCallback(self.__cellSelectionCallBack)

        self.solver = Solver()

    def showWindow(self):
        self.mainWindow.mainloop()

    def registerPuzzleBoard(self, puzzleBoard):
        self.puzzleBoardCanvasManager.registerPuzzleBoard(puzzleBoard)
        self.puzzleBoardObject = puzzleBoard
        self.numRows, self.numCols = puzzleBoard.getDimensions()

if __name__ == '__main__':
    basePath = os.path.expandvars('$APPDATA')
    appBasePath = os.path.join(basePath, 'MasyuSolver')
    settingsFileName = 'masyuSolverConfig.ini'
    ConfigMgr.loadSettings(appBasePath, settingsFileName)
    uiWindow = SolverUIWindow()
    pb = PuzzleBoard()
    uiWindow.registerPuzzleBoard(pb)
    uiWindow.showWindow()