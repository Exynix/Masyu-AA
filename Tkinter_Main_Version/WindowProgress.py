from WindowMasyu import *
import tkinter as tk
from WindowsCanvasManager import *
class ProgressDialog(MasyuDialog):
    def __init__(self, parentWindow, puzzleBoard, cancelEvent, resumeEvent):
        super().__init__(parentWindow)
        self.__puzzleBoard = puzzleBoard
        self.__cancelEvent = cancelEvent
        self.__resumeEvent = resumeEvent

    def cancelHandler(self):
        self.__cancelButton['state'] = tk.DISABLED
        self.__cancelEvent.set()
        self.__toplevel.destroy()

    def resumeHandler(self):
        self.__resumeButton['state'] = tk.DISABLED
        self.__resumeEvent.set()
        self.__toplevel.destroy()

    def showDialog(self):
        self.__toplevel = tk.Toplevel()
        self.__toplevel.protocol("WM_DELETE_WINDOW", self.cancelHandler)
        puzzleBoardFrame = tk.Frame(master=self.__toplevel, relief=tk.RAISED, highlightthickness=0, borderwidth=10)
        puzzleBoardFrame.grid(row=0, column=0)

        self.__puzzleBoardCanvas = tk.Canvas(master=puzzleBoardFrame, height=300, width=300,
                                      highlightthickness=0, relief=tk.FLAT, borderwidth=0)
        self.__puzzleBoardCanvas.grid(row=0, column=0)

        self.__canvasManager = CanvasManager(self.__puzzleBoardCanvas, True, True, True)
        self.__canvasManager.registerPuzzleBoard(self.__puzzleBoard)

        buttonFrame = tk.Frame(master=self.__toplevel, relief=tk.RAISED, borderwidth=0)
        buttonFrame.grid(row=1, column=0)
        self.__cancelButton = tk.Button(buttonFrame, text="Cancel", command=self.cancelHandler, width=10)
        self.__cancelButton.grid(row=0, column=0, padx=(2, 35), pady=(15, 15), sticky="e")
        self.__resumeButton = tk.Button(buttonFrame, text="Resume", command=self.resumeHandler, width=10)
        self.__resumeButton.grid(row=0, column=1, padx=(2, 35), pady=(15, 15), sticky="e")

        super().showDialog(self.__toplevel)
