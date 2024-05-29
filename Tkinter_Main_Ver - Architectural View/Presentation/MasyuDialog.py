class MasyuDialog():
    def __init__(self, parentWindow):
        self.__parentWindow = parentWindow
        self.__dialogWindow = None

    def showDialog(self, dialogWindow):

        self.__dialogWindow = dialogWindow
        self.__dialogWindow.withdraw()
        self.__dialogWindow.update_idletasks()

        dialogX = self.__parentWindow.winfo_x() + (self.__parentWindow.winfo_width() / 2) - (self.__dialogWindow.winfo_width() / 2)
        dialogY = self.__parentWindow.winfo_y() + (self.__parentWindow.winfo_height() / 2) - (self.__dialogWindow.winfo_height() / 2)

        if (dialogX < 0):
            dialogX = 0

        if (dialogY < 0):
            dialogY = 0

        screenWidth = self.__parentWindow.winfo_screenwidth()
        screenHeight = self.__parentWindow.winfo_screenheight()

        if ((dialogX + self.__dialogWindow.winfo_width()) >= screenWidth):
            dialogX = screenWidth - self.__dialogWindow.winfo_width()

        if ((dialogY + self.__dialogWindow.winfo_height()) >= screenHeight):
            dialogY = screenHeight - self.__dialogWindow.winfo_height()

        self.__dialogWindow.geometry("+%d+%d" % (dialogX, dialogY))
        self.__dialogWindow.deiconify()

        self.__parentWindow.attributes('-disabled', True)

        self.__dialogWindow.focus_set()
        self.__dialogWindow.grab_set()
        self.__dialogWindow.wait_window()

        self.__parentWindow.attributes('-disabled', False)
        self.__parentWindow.lift()