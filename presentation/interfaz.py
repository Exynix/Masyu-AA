#para hacer esto me guie de este video y de los siguientes de la lista de repro https://www.youtube.com/watch?v=hTUJC8HsC2I
from tkinter import *

def on_celda_click(event, canvas, lineas_dibujadas):
    x, y = event.x, event.y
    columna = x // 50
    fila = y // 50
    celda = (fila, columna)  # Utilizamos índices base 0 para la celda

     # Imprime las coordenadas de la celda donde se hizo clic
    print(f"Clic en celda: Fila {fila + 1}, Columna {columna + 1}")

    # Si ya existe una línea en esta celda, determinar la acción basada en el estado actual
    if celda in lineas_dibujadas:
        id_linea, estado_linea = lineas_dibujadas[celda]
        canvas.delete(id_linea)  # Elimina la línea existente
        
        if estado_linea == 'vertical':
            # Si la línea actual es vertical, dibujar una horizontal
            id_linea = canvas.create_line(50 * columna, 50 * fila + 25, 50 * (columna + 1), 50 * fila + 25, fill="black", width=2)
            lineas_dibujadas[celda] = (id_linea, 'horizontal')
        else:
            # Si la línea es horizontal (o en cualquier otro estado), eliminar la línea
            del lineas_dibujadas[celda]
    else:
        # No existe línea: dibujar una línea vertical
        id_linea = canvas.create_line(50 * columna + 25, 50 * fila, 50 * columna + 25, 50 * (fila + 1), fill="black", width=2)
        lineas_dibujadas[celda] = (id_linea, 'vertical')


def limpiar_tablero(canvas, lineas_dibujadas):
    for id_linea, _ in lineas_dibujadas.values():
        canvas.delete(id_linea)
    lineas_dibujadas.clear()

def crear_interfaz(num_filas_columnas, configuraciones):
    global lineas_dibujadas
    lineas_dibujadas = {}

    raiz = Tk()
    raiz.title("Masyu")

    # Organiza la interfaz usando un Frame principal
    miFrame = Frame(raiz)
    miFrame.pack(expand=True, fill="both", padx=20, pady=20)

    # Frame para contener los botones y organizarlos horizontalmente
    botonesFrame = Frame(miFrame)
    botonesFrame.pack(side=TOP, pady=10)

    # Botón para limpiar el tablero, colocado dentro del botonesFrame
    boton_limpiar = Button(botonesFrame, text="Limpiar Tablero", command=lambda: limpiar_tablero(canvas, lineas_dibujadas))
    boton_limpiar.pack(side=LEFT, padx=5)

    # Botón de Jugador Sintético, colocado al lado del botón Limpiar Tablero
    boton_jugador_sintetico = Button(botonesFrame, text="Jugador Sintético")
    boton_jugador_sintetico.pack(side=LEFT, padx=5)

    textoLabel = Label(miFrame, text="Masyu!", fg="red", font=("Comic Sans MS", 18))
    textoLabel.pack(side=TOP, pady=(0, 20))

    # Canvas para el tablero, también en el Frame principal
    canvas = Canvas(miFrame, width=50*num_filas_columnas, height=50*num_filas_columnas, bg="white")
    canvas.pack()

    canvas.bind("<Button-1>", lambda event: on_celda_click(event, canvas, lineas_dibujadas))

    # Dibuja la cuadrícula
    for i in range(num_filas_columnas):
        for j in range(num_filas_columnas):
            canvas.create_rectangle(50 * j, 50 * i, 50 * (j + 1), 50 * (i + 1), outline="grey")

    # Dibuja las perlas
    for fila, columna, tipo in (configuracion.strip().split(',') for configuracion in configuraciones):
        if tipo == '1':  # Perla blanca
            canvas.create_oval(50 * (int(columna) - 1) + 10, 50 * (int(fila) - 1) + 10, 50 * int(columna) - 10, 50 * int(fila) - 10, fill="white", outline="black")
        else:  # Perla negra
            canvas.create_oval(50 * (int(columna) - 1) + 10, 50 * (int(fila) - 1) + 10, 50 * int(columna) - 10, 50 * int(fila) - 10, fill="black")

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