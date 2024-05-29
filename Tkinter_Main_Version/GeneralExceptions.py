class MasyuException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return(self.msg)

class MasyuSolverException(MasyuException):
    def __init__(self, msg, location):
        super().__init__(msg)
        self.location = location

    def __str__(self):
        return(self.msg + " : " + repr(self.location))

class MasyuFileSaveException(MasyuException):
    def __init__(self, msg):
        super().__init__(msg)

class MasyuFileOpenException(MasyuException):
    def __init__(self, msg):
        super().__init__(msg)

class MasyuInvalidPuzzleFileException(MasyuException):
    def __init__(self, msg):
        super().__init__(msg)

class MasyuOrphanedRegionException(MasyuException):
    def __init__(self, msg, startingLocation, endingLocation):
        super().__init__(msg)
        self.startingLocation = startingLocation
        self.endingLocation = endingLocation

    def __str__(self):
        return(self.msg + " : " + repr(self.startingLocation) + " - " + repr(self.endingLocation))