import threading
import abc

class WorkThread():

    @abc.abstractmethod
    def codeToRunInThread(self):
        pass

    def __init__(self, solver, puzzleBoard):

        self.solver = solver

        self.pb = puzzleBoard

        self.__threadHandle = threading.Thread(target=self.codeToRunInThread, args=(), daemon=True)

        self.showResultsEvent = threading.Event()
        self.showResultsEvent.clear()

        self.resumeEvent = threading.Event()
        self.resumeEvent.clear()

        self.cancelEvent = threading.Event()
        self.cancelEvent.clear()

    def cancelWorkThread(self):
        self.cancelEvent.set()

    def start(self):
        self.__threadHandle.start()

    def isAlive(self):
        return((self.__threadHandle.is_alive()))

    def supportsCancelRequest(self):
        return(False)

    def timerHandler(self, parentWindow):
        return(False)