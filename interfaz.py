#para hacer esto me guie de este video y de los siguientes de la lista de repro https://www.youtube.com/watch?v=hTUJC8HsC2I

from tkinter import *


#  Leer el archivo de configuración
with open('archivo10.txt', 'r') as archivo:
    primera_linea = archivo.readline().strip()
    num_filas_columnas = int(primera_linea)
    configuraciones = archivo.readlines()  # Leer el resto de las líneas para las configuraciones


raiz = Tk()
raiz.title("Masyu")

miFrame = Frame(raiz)
miFrame.pack(expand=True, fill="both")
miFrame.config(bd=15)
miFrame.config(relief="groove")
miFrame.config(cursor="hand2")
miFrame.config(width="650", height="350")


#esto es el titulo del juego (dodne dice masyu xd)
textoLabel=Label(miFrame, text="Masyu!", fg="red",justify="center", font=("Comic Sans MS", 18))
textoLabel.grid(row=0, column=0, sticky="ew", columnspan=num_filas_columnas)

# Crear la cuadrícula como Canvas
celdas = {}
for fila in range(1, num_filas_columnas + 1):
    for columna in range(1, num_filas_columnas + 1):
        canvas = Canvas(miFrame, width=50, height=50, bg="white")
        canvas.grid(row=fila, column=columna, padx=5, pady=5)
        celdas[(fila, columna)] = canvas

# Dibujar las formas según las configuraciones
for configuracion in configuraciones:
    fila, columna, forma = map(int, configuracion.strip().split(','))  # Ajustar aquí para dividir por comas
    if (fila, columna) in celdas:
        canvas = celdas[(fila, columna)]
        if forma == 1:  # Dibujar un círculo blanco
            canvas.create_oval(10, 10, 40, 40, fill="white", outline="black")
        elif forma == 2:  # Dibujar un círculo negro
            canvas.create_oval(10, 10, 40, 40, fill="black")

raiz.mainloop() #esto hace q se ejecute la ventana

