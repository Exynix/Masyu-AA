import tkinter as tk
from threading import Thread
import time

class WorkingWindow():

    WORKING_MESSAGE = "WORKING "

    INITIAL_DOT_COUNTER_VALUE = 10

    INITIAL_ITERATION_COUNTER_VALUE = 5

    MAX_DOTS = 5

    def __cancelButtonCallback(self):
        self.cancelButton['state'] = tk.DISABLED

        print("cancel")
        self.__workThread.cancelWorkThread()

    def __init__(self, parentWindow, workThread):

        self.iterationCounter = self.INITIAL_ITERATION_COUNTER_VALUE
        self.dotCounter = self.INITIAL_DOT_COUNTER_VALUE
        self.numDots = 0

        self.__workThread = workThread

        self.parentWindow = parentWindow

        self.dialogWindow = tk.Toplevel(master=parentWindow)
        self.dialogWindow.wm_overrideredirect(True)
        self.messageFrame = tk.Frame(master=self.dialogWindow, relief=tk.RAISED, borderwidth=5)
        self.messageFrame.pack(expand=True, fill=tk.BOTH)
        self.workingMessage = tk.StringVar()
        self.workingMessage.set(self.WORKING_MESSAGE + "      ")
        self.message = tk.Label(master=self.messageFrame, textvariable=self.workingMessage)
        self.message.pack(side=tk.TOP, padx=20, pady=20, anchor=tk.SW)

        if (self.__workThread.supportsCancelRequest()):
            self.cancelButton = tk.Button(master=self.messageFrame, text="Cancel", command=self.__cancelButtonCallback, width=10)
            self.cancelButton.pack(side=tk.TOP, pady=(0,15))
        else:
            self.cancelButton = None

    def checkForThreadDone(self):
        if not (self.__workThread.isAlive()):

            self.dialogWindow.destroy()

        else:

            if (self.iterationCounter > 0):
                self.iterationCounter -= 1
                if (self.iterationCounter == 0):

                    self.dialogWindow.geometry("")
                    self.dialogWindow.geometry(self.savedGeometry)

            self.dotCounter -= 1
            if (self.dotCounter <= 0):

                self.numDots += 1
                if (self.numDots > self.MAX_DOTS):
                    self.numDots = 0

                message = self.WORKING_MESSAGE
                for i in range(self.numDots):
                    message = message + "."

                self.messageFrame.pack_propagate(False)
                self.workingMessage.set(message)

                self.dotCounter = self.INITIAL_DOT_COUNTER_VALUE

            raiseParentWindow = self.__workThread.timerHandler(self.dialogWindow)

            if (raiseParentWindow):
                self.parentWindow.lift()
                self.dialogWindow.lift()

            self.dialogWindow.after(100, self.checkForThreadDone)

    def showWindow(self):

        self.dialogWindow.withdraw()

        self.dialogWindow.update_idletasks()

        dialogX = self.parentWindow.winfo_x() + (self.parentWindow.winfo_width() / 2) - (self.dialogWindow.winfo_width() / 2)
        dialogY = self.parentWindow.winfo_y() + (self.parentWindow.winfo_height() / 2) - (self.dialogWindow.winfo_height() / 2)

        if (dialogX < 0):
            dialogX = 0

        if (dialogY < 0):
            dialogY = 0

        screenWidth = self.parentWindow.winfo_screenwidth()
        screenHeight = self.parentWindow.winfo_screenheight()

        if ((dialogX + self.dialogWindow.winfo_width()) >= screenWidth):
            dialogX = screenWidth - self.dialogWindow.winfo_width()

        if ((dialogY + self.dialogWindow.winfo_height()) >= screenHeight):
            dialogY = screenHeight - self.dialogWindow.winfo_height()

        self.savedGeometry = "+%d+%d" % (dialogX, dialogY)

        self.dialogWindow.geometry("0x0")

        self.dialogWindow.deiconify()

        self.parentWindow.attributes('-disabled', True)

        self.dialogWindow.focus_set()
        self.dialogWindow.grab_set()

        self.dialogWindow.after(100, self.checkForThreadDone)

        self.dialogWindow.wait_window()

        self.parentWindow.attributes('-disabled', False)
        self.parentWindow.lift()