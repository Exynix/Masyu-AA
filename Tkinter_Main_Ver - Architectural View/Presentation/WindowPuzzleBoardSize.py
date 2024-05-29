import tkinter as tk
from WindowMasyu import *

class GetPuzzleBoardSizeDialog(MasyuDialog):

    def __processOKButton(self):

        self.numRows = self.rowVar.get()
        self.numCols = self.colVar.get()

        self.__dialogWindow.destroy()

    def __processCancelButton(self):

        self.numRows = -1
        self.numCols = -1

        self.__dialogWindow.destroy()

    def __init__(self, parentWindow, rowConstraints=(5, 15), colConstraints=(5, 15)):
        super().__init__(parentWindow)

        self.numRows = -1
        self.numCols = -1

        self.rowMin, self.rowMax = rowConstraints
        self.colMin, self.colMax = colConstraints

    def showDialog(self, initialRow=-1, initialCol=-1):

        if (initialRow == -1):
            initialRow = self.rowMin

        if (initialCol == -1):
            initialCol = self.colMin

        self.__dialogWindow = tk.Toplevel()
        self.__dialogWindow.title("Enter Puzzle Board Size")

        self.__dialogWindow.resizable(False, False)

        mainFrame = tk.Frame(master=self.__dialogWindow)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        inputFrame = tk.LabelFrame(master=mainFrame, text="New Puzzle Size")
        inputFrame.pack(fill=tk.X, side=tk.TOP, pady=5, padx=10)

        rowFrame = tk.Frame(master=inputFrame)
        rowFrame.pack(fill=tk.X, side=tk.TOP, padx=15)
        rowLabelString = "Number of rows (min=" + str(self.rowMin) + ", max=" + str(self.rowMax) + "):   "
        rowLabel = tk.Label(master=rowFrame, text=rowLabelString)
        rowLabel.pack(side=tk.LEFT, pady=10)
        self.rowVar = tk.IntVar()
        self.rowVar.set(initialRow)
        numRowsSpinbox = tk.Spinbox(master=rowFrame, state='readonly', width=5, from_=self.rowMin, to=self.rowMax, textvariable=self.rowVar)
        numRowsSpinbox.pack(side=tk.RIGHT, pady=10)

        colFrame = tk.Frame(master=inputFrame)
        colFrame.pack(fill=tk.X, side=tk.TOP, padx=15)
        colLabelString = "Number of columns (min=" + str(self.colMin) + ", max=" + str(self.colMax) + "):   "
        colLabel = tk.Label(master=colFrame, text=colLabelString)
        colLabel.pack(side=tk.LEFT, pady=10, anchor=tk.SW)
        self.colVar = tk.IntVar()
        self.colVar.set(initialCol)
        self.numColsSpinbox = tk.Spinbox(master=colFrame, state='readonly', width=5, from_=self.colMin, to=self.colMax, textvariable=self.colVar)
        self.numColsSpinbox.pack(side=tk.RIGHT, pady=10)

        buttonFrame = tk.Frame(master=mainFrame)
        buttonFrame.pack(fill=tk.X, side=tk.LEFT, padx=40, pady=10, ipadx=30)

        okButton = tk.Button(master=buttonFrame, text="OK", command=self.__processOKButton)
        okButton.pack(side=tk.LEFT, ipadx=30)
        cancelButton = tk.Button(master=buttonFrame, text="Cancel", command=self.__processCancelButton)
        cancelButton.pack(side=tk.RIGHT, ipadx=30)

        super().showDialog(self.__dialogWindow)

        return((self.numRows, self.numCols))
