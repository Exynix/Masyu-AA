class PuzzleStateMachine():

    __STATE1 = 1
    __STATE2 = 2
    __STATE3 = 3
    __STATE4 = 4
    __STATE5 = 5
    __STATE6 = 6

    __lastFileName = None
    __state = __STATE1

    @classmethod
    def reset(cls):
        cls.__state = cls.__STATE1
        cls.__lastFileName = None

    @classmethod
    def fileOpened(cls, fileName):
        cls.__state = cls.__STATE3
        cls.__lastFileName = fileName

    @classmethod
    def fileSavedAs(cls, fileName):
        cls.__state = cls.__STATE5
        cls.__lastFileName = fileName

    @classmethod
    def puzzleChanged(cls):

        if (cls.__state == cls.__STATE1):
            cls.__state = cls.__STATE2
        elif (cls.__state == cls.__STATE3):
            cls.__state = cls.__STATE4
        elif (cls.__state == cls.__STATE5):
            cls.__state = cls.__STATE6

    @classmethod
    def hasPuzzleChanged(cls):
        return ((cls.__state == cls.__STATE2) or (cls.__state == cls.__STATE4) or
                (cls. __state == cls.__STATE6))

    @classmethod
    def getFileName(cls):
        return(cls.__lastFileName)

