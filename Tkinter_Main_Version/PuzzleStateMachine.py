# Clase usada para mantener un registro del estado de la aplicación, con respecto a las operaciones IO.
# También permite saber si hay un nombre asociado al archivo o juego actual.
class PuzzleStateMachine():
    __STATE1 = 1    # Sin modificaciones y sin guardar un archivo.
    __STATE2 = 2    # Con modificaciones y sin guardar un archivo.
    __STATE3 = 3    # Sin modificaciones desde la última operacioón de apertura de un archivo. File - open.
    __STATE4 = 4    # Con modificaciones desde la última operacioón de apertura de un archivo. File - open.
    __STATE5 = 5    # Sin modificaciones desde la última operacioón de guardado de un archivo. File - save.
    __STATE6 = 6    # Con modificaciones desde la última operacioón de guardado de un archivo. File - save.

    # El estado inicial es 1. Es decir, un tablero nuevo.
    __lastFileName = None
    __state = __STATE1

    @classmethod
    def fileOpened(cls, fileName):
        cls.__state = cls.__STATE3
        cls.__lastFileName = fileName

    @classmethod
    def fileSavedAs(cls, fileName):
        cls.__state = cls.__STATE5
        cls.__lastFileName = fileName

    # Reinicia el estado de la aplicación al estado 1, cuando se crea un nuevo tablero.
    @classmethod
    def reset(cls):
        cls.__state = cls.__STATE1
        cls.__lastFileName = None

    # Llamaado cada vez que el tablero es cambiado por el usuario. Cambia el estado de la aplicación
    # de aquellos estados que indican no modificación a aquellos que indican modificación.
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

