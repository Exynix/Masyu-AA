# Función para leer el archivo de configuración
def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            primera_linea = archivo.readline().strip()
            num_filas_columnas = int(primera_linea)
            configuraciones = archivo.readlines()
        return num_filas_columnas, configuraciones
    except FileNotFoundError:
        print("No se encontro el archivo, revise que haya escrito bien el nombre y que el archivo este en la carpeta del programa.")
        return 0, []
