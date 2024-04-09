
from presentation.interfaz import crear_interfaz
from FileHandling.file_handling import leer_archivo

def main():
    nombre_archivo = input("Ingrese el nombre del archivo con el que desea jugar (incluya el .txt en el nombre): ")
    num_filas_columnas, configuraciones = leer_archivo(nombre_archivo)

    if num_filas_columnas > 0:
        app = crear_interfaz(num_filas_columnas, configuraciones)
        app.mainloop()
    else:
        print("Error al leer el archivo de configuración.")

if __name__ == "__main__":
    main()
