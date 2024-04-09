#para hacer esto me guie de este video y de los siguientes de la lista de repro https://www.youtube.com/watch?v=hTUJC8HsC2I

from tkinter import *

def crear_interfaz(num_filas_columnas, configuraciones):
    raiz = Tk()
    raiz.title("Masyu")

    miFrame = Frame(raiz)
    miFrame.pack(expand=True, fill="both")
    miFrame.config(bd=15, relief="groove", cursor="hand2", width="650", height="350")

    textoLabel = Label(miFrame, text="Masyu!", fg="red", justify="center", font=("Comic Sans MS", 18))
    textoLabel.grid(row=0, column=0, sticky="ew", columnspan=num_filas_columnas)

    celdas = {}
    for fila in range(1, num_filas_columnas + 1):
        for columna in range(1, num_filas_columnas + 1):
            canvas = Canvas(miFrame, width=50, height=50, bg="white")
            canvas.grid(row=fila, column=columna, padx=5, pady=5)
            celdas[(fila, columna)] = canvas

    for configuracion in configuraciones:
        fila, columna, forma = map(int, configuracion.strip().split(','))
        if (fila, columna) in celdas:
            canvas = celdas[(fila, columna)]
            if forma == 1:
                canvas.create_oval(10, 10, 40, 40, fill="white", outline="black")
            elif forma == 2:
                canvas.create_oval(10, 10, 40, 40, fill="black")

    return raiz



#esto es una cosa q esta medio rota pero me lo dio el panita xd, abre el archivo de una forma exotica 
"""
from tkinter import *
from tkinter import filedialog

# Función para seleccionar el archivo de configuración
def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta_archivo:  # Verificar si el usuario seleccionó un archivo
        with open(ruta_archivo, 'r') as archivo:
            primera_linea = archivo.readline().strip()
            num_filas_columnas = int(primera_linea)
            configuraciones = archivo.readlines()
        return num_filas_columnas, configuraciones
    else:
        return 0, []  # Retornar valores predeterminados si no se selecciona un archivo

# Inicialización de la raíz de Tkinter
raiz = Tk()
raiz.title("Masyu")

# Solicitar al usuario que seleccione un archivo antes de construir la GUI
num_filas_columnas, configuraciones = seleccionar_archivo()

# Si el usuario ha seleccionado un archivo, proceder con la construcción de la GUI
if num_filas_columnas > 0:
    miFrame = Frame(raiz)
    miFrame.pack(expand=True, fill="both")
    miFrame.config(bd=15, relief="groove", cursor="hand2", width="650", height="350")

    # Título del juego
    textoLabel = Label(miFrame, text="Masyu!", fg="red", justify="center", font=("Comic Sans MS", 18))
    textoLabel.grid(row=0, column=0, sticky="ew", columnspan=num_filas_columnas)

    # Creación de la cuadrícula del juego
    celdas = {}
    for fila in range(1, num_filas_columnas + 1):
        for columna in range(1, num_filas_columnas + 1):
            canvas = Canvas(miFrame, width=50, height=50, bg="white")
            canvas.grid(row=fila, column=columna, padx=5, pady=5)
            celdas[(fila, columna)] = canvas

    # Dibujar configuraciones en las celdas
    for configuracion in configuraciones:
        fila, columna, forma = map(int, configuracion.strip().split(','))
        if (fila, columna) in celdas:
            canvas = celdas[(fila, columna)]
            if forma == 1:  # Círculo blanco
                canvas.create_oval(10, 10, 40, 40, fill="white", outline="black")
            elif forma == 2:  # Círculo negro
                canvas.create_oval(10, 10, 40, 40, fill="black")

    # Mantener la ventana abierta
    raiz.mainloop()
else:
    raiz.destroy()  # Cerrar la aplicación si el usuario no selecciona un archivo

"""