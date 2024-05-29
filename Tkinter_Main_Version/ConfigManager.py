import configparser
import os

# Manejador de confifuraciones del juego.
class ConfigMgr():

    __configFileName = None
    __configFileDirectory = None
    __fullPath = None
    __configParser = None

    # Carga la configuración desde un archivo. Toma el directorio y el nombre del archivo como parámetros.
    @classmethod
    def loadSettings(cls, directory, fileName):

        cls.__configParser = configparser.ConfigParser()

        cls.__fullPath = os.path.join(directory, fileName)
        cls.__configParser.read(cls.__fullPath)

        cls.__configFileDirectory = directory
        cls.__configFileName = fileName

    @classmethod

    # Establece el valor de una configuración específica en una sección específica del archivo de configuración.
    def setSettingValue(cls, section, name, value):

        if not(cls.__configParser.has_section(section)):
            cls.__configParser.add_section(section)

        cls.__configParser.set(section, name, value)

        if not(os.path.exists(cls.__configFileDirectory)):
            os.makedirs(cls.__configFileDirectory)


        with open(cls.__fullPath, 'w') as f:
            cls.__configParser.write(f)

    #  Esta función recupera el valor de una configuración específica de una sección específica del archivo de configuración.
    @classmethod
    def getSettingValue(cls, section, name):
        try:
            value = cls.__configParser.get(section, name)
        except Exception as e:
            value = None
        finally:
            return(value)
