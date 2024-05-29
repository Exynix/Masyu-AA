# interfaz.py
#para hacer esto me guie de este video y de los siguientes de la lista de repro https://www.youtube.com/watch?v=hTUJC8HsC2I
from tkinter import *
from tkinter import messagebox


from Model.Game_Board import GameBoard  
from Model.cell_types_enum import CellTypesEnum

def on_celda_click(event, canvas, lineas_dibujadas):
    x, y = event.x, event.y
    columna = x // 50
    fila = y // 50
    celda = (fila, columna)  # Utilizamos índices base 0 para la celda

    if event.num == 1:  # Clic izquierdo, manejo de líneas
        if celda in lineas_dibujadas:
            id_linea, estado_linea = lineas_dibujadas[celda]
            canvas.delete(id_linea)  # Elimina la línea existente

            if estado_linea == 'vertical':
                id_linea = canvas.create_line(50 * columna, 50 * fila + 25, 50 * (columna + 1), 50 * fila + 25, fill="black", width=2)
                lineas_dibujadas[celda] = (id_linea, 'horizontal')
            else:
                del lineas_dibujadas[celda]
        else:
            id_linea = canvas.create_line(50 * columna + 25, 50 * fila, 50 * columna + 25, 50 * (fila + 1), fill="black", width=2)
            lineas_dibujadas[celda] = (id_linea, 'vertical')
    elif event.num == 3:  # Clic derecho, dibujar/rotar/eliminar curva
        dibujar_rotar_eliminar_curva(canvas, fila, columna, lineas_dibujadas)

def dibujar_rotar_eliminar_curva(canvas, fila, columna, lineas_dibujadas):
    # Identifica si ya existe una curva y su estado
    if (fila, columna, 'curva') in lineas_dibujadas:
        ids_curva, estado_curva = lineas_dibujadas[(fila, columna, 'curva')]
        # Elimina las líneas actuales de la curva
        for id_curva in ids_curva:
            canvas.delete(id_curva)
        if estado_curva < 270:
            # Incrementa la rotación de la curva en 90 grados
            estado_curva += 90
        else:
            # Elimina la curva después de la cuarta rotación
            del lineas_dibujadas[(fila, columna, 'curva')]
            return  # Sale de la función para no dibujar una nueva curva
    else:
        estado_curva = 0  # Estado inicial de la curva
    
    # Calcula las posiciones iniciales y finales para las dos líneas basadas en el estado de rotación
    x1, y1 = 50 * columna, 50 * fila
    if estado_curva == 0:
        coords = [(x1 + 25, y1, x1 + 25, y1 + 25), (x1 + 25, y1 + 25, x1 + 50, y1 + 25)]  # Abajo y luego derecha
    elif estado_curva == 90:
        coords = [(x1, y1 + 25, x1 + 25, y1 + 25), (x1 + 25, y1 + 25, x1 + 25, y1)]  # Izquierda y luego arriba
    elif estado_curva == 180:
        coords = [(x1 + 25, y1 + 50, x1 + 25, y1 + 25), (x1 + 25, y1 + 25, x1, y1 + 25)]  # Arriba y luego izquierda
    elif estado_curva == 270:
        coords = [(x1 + 50, y1 + 25, x1 + 25, y1 + 25), (x1 + 25, y1 + 25, x1 + 25, y1 + 50)]  # Derecha y luego abajo
    
    # Dibuja las nuevas líneas de la curva
    ids_curva = [canvas.create_line(*coord, fill="black", width=2) for coord in coords]
    lineas_dibujadas[(fila, columna, 'curva')] = (ids_curva, estado_curva)








# Ejemplo de cómo podrías usar `crear_interfaz`
# num_filas_columnas, configuraciones = 10, ["1,1,1", "2,2,2"]  # Esto debería ser leído de un archivo o algo similar
# app = crear_interfaz(num_filas_columnas, configuraciones)
# app.mainloop()








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