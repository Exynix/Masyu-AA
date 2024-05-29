from tkinter import filedialog as fd
from ModificationPuzzleStateMachine import *
from ConfigManager import *
from GameBoardFileIO import *
from WindowUnsavedChanges import *

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ''))

# Clase encargada de las operoaciones de IO.
# Guardado de archivos, apertura de archivos, etc.
class FileIO():

    __MODE_NEW = 1
    __MODE_OPEN = 2
    __MODE_SAVE = 3
    __MODE_SAVE_AS = 4
    __MODE_EXIT = 5

    __FILE_SECTION = 'File'
    __FILE_DIRECTORY = 'Directory'

    @classmethod
    # File -> New
    def fileNew(cls, parentWindow, puzzleBoard):
        return (cls.__processIO(parentWindow, cls.__MODE_NEW, puzzleBoard))

    @classmethod
    # File -> Open
    def fileOpen(cls, parentWindow, puzzleBoard):
        return (cls.__processIO(parentWindow, cls.__MODE_OPEN, puzzleBoard))

    @classmethod
    # File -> Save
    def fileSave(cls, parentWindow, puzzleBoard):
        return (cls.__processIO(parentWindow, cls.__MODE_SAVE, puzzleBoard))

    @classmethod
    # File -> Save As
    def fileSaveAs(cls, parentWindow, puzzleBoard):
        return (cls.__processIO(parentWindow, cls.__MODE_SAVE_AS, puzzleBoard))

    @classmethod
    # File -> Exit
    def fileExit(cls, parentWindow, puzzleBoard):
        return (cls.__processIO(parentWindow, cls.__MODE_EXIT, puzzleBoard))


    @classmethod

    def __processIO(cls, parentWindow, mode, puzzleBoard):
        supportedFileTypes = [(PuzzleBoardFile.FILE_EXTENSION, "*." + PuzzleBoardFile.FILE_EXTENSION)]

        saveCurrentPuzzle = False

        if ((mode == cls.__MODE_OPEN) or (mode == cls.__MODE_NEW) or (mode == cls.__MODE_EXIT)):
            if PuzzleStateMachine.hasPuzzleChanged():
                saveChangesDialog = UnsavedChangesDialog(parentWindow)
                response = saveChangesDialog.showDialog()
                if (response == None):
                    return ((False, None))
                elif (response == False):
                    if (mode == cls.__MODE_EXIT):
                        return ((True, None))
                    elif (mode == cls.__MODE_NEW):
                        return ((True, None))
                elif (response == True):
                    saveCurrentPuzzle = True

        elif ((mode == cls.__MODE_SAVE) or (mode == cls.__MODE_SAVE_AS)):
            saveCurrentPuzzle = True

        currentFilename = PuzzleStateMachine.getFileName()

        if (saveCurrentPuzzle):
            lastDirectoryUsed = ConfigMgr.getSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY)

            if ((mode == cls.__MODE_SAVE_AS) or (currentFilename == None)):
                saveFilePath = fd.asksaveasfilename(initialfile=currentFilename, initialdir=lastDirectoryUsed, filetypes=supportedFileTypes, defaultextension=supportedFileTypes)

                if (saveFilePath == ''):
                    return ((False, None))

                if not (saveFilePath.endswith('.' + PuzzleBoardFile.FILE_EXTENSION)):
                    saveFilePath += '.' + PuzzleBoardFile.FILE_EXTENSION

            else:
                saveFilePath = os.path.join(lastDirectoryUsed, currentFilename)
            try:
                PuzzleBoardFile.saveToFile(saveFilePath, puzzleBoard)

            except Exception as e:
                raise MasyuFileSaveException("Error while saving puzzle file") from e

            else:
                lastDirectoryUsed, currentFilename = os.path.split(saveFilePath)

                PuzzleStateMachine.fileSavedAs(currentFilename)

                ConfigMgr.setSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY, lastDirectoryUsed)

        if ((mode == cls.__MODE_SAVE) or (mode == cls.__MODE_SAVE_AS)):
            return((True, None))

        elif ((mode == cls.__MODE_EXIT) or (mode == cls.__MODE_NEW)):
            return((True, None))

        lastDirectoryUsed = ConfigMgr.getSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY)

        fileToOpen = fd.askopenfilename(initialfile=currentFilename, initialdir=lastDirectoryUsed, filetypes=supportedFileTypes, defaultextension=supportedFileTypes)
        if (fileToOpen == ""):
            return ((False, None))

        lastDirectoryUsed, currentFilename = os.path.split(fileToOpen)


        try:
            newPuzzleBoard = PuzzleBoardFile.loadFile(fileToOpen)
        except MasyuInvalidPuzzleFileException as mipfe:
            raise
        except Exception as e:
            raise MasyuFileOpenException ("Error during open file") from e
        else:
            # Successful load!
            # Update the directory stored in the Config Mgr, and update the
            # State Mgr state (and filename)
            PuzzleStateMachine.fileOpened(currentFilename)
            ConfigMgr.setSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY, lastDirectoryUsed)

            # Return the new puzzle board
            return((True, newPuzzleBoard))