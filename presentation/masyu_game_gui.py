# masyy_game_gui.py
from tkinter import *
from tkinter import messagebox

from Model.Game_Board import GameBoard  
from Model.cell_types_enum import CellTypesEnum

class MasyuGameGUI:
    def __init__(self, game_board):
        self.game_board = game_board
    
    def print_game_board(self, game_board: GameBoard) -> None :
        lineas_dibujadas = {}

        raiz = Tk()
        raiz.title("Masyu")

        miFrame = Frame(raiz)
        miFrame.pack(expand=True, fill="both", padx=20, pady=20)

        botonesFrame = Frame(miFrame)
        botonesFrame.pack(side=TOP, pady=10)

        boton_limpiar = Button(botonesFrame, text="Limpiar Tablero", command=lambda: self.limpiar_tablero(canvas, lineas_dibujadas))
        boton_limpiar.pack(side=LEFT, padx=5)

        boton_jugador_sintetico = Button(botonesFrame, text="Jugador Sintético")  # Implement its functionality as needed
        boton_jugador_sintetico.pack(side=LEFT, padx=5)

        textoLabel = Label(miFrame, text="Masyu!", fg="red", font=("System", 18))
        textoLabel.pack(side=TOP, pady=(0, 20))

        num_filas_columnas = len(game_board.matrix)
        canvas = Canvas(miFrame, width=50*num_filas_columnas, height=50*num_filas_columnas, bg="white")
        canvas.pack()

        canvas.bind("<Button-1>", lambda event: self.on_cell_click(event, canvas, lineas_dibujadas))
        canvas.bind("<Button-3>", lambda event: self.on_cell_click(event, canvas, lineas_dibujadas))

        # Draw the grid and pearls based on the GameBoard state
        for i, row in enumerate(game_board.matrix):
            for j, cell in enumerate(row):
                canvas.create_rectangle(50 * j, 50 * i, 50 * (j + 1), 50 * (i + 1), outline="grey")
                if cell.type == CellTypesEnum.WHITEPEARL:
                    canvas.create_oval(50 * j + 10, 50 * i + 10, 50 * (j + 1) - 10, 50 * (i + 1) - 10, fill="white", outline="black")
                elif cell.type == CellTypesEnum.BLACKPEARL:
                    canvas.create_oval(50 * j + 10, 50 * i + 10, 50 * (j + 1) - 10, 50 * (i + 1) - 10, fill="black")
                
        self.root =  raiz
        self.root.mainloop()

    def on_cell_click(self, event):
        cell_size = 50
        x, y = event.x, event.y
        column, row = x // cell_size, y // cell_size

        current_cell = self.game_board.matrix[row][column]

        if current_cell.type in [CellTypesEnum.WHITEPEARL, CellTypesEnum.BLACKPEARL]:
            messagebox.showwarning("Invalid action", "Cannot draw lines on pearls!")
            return  # Exit the function to prevent drawing a line

        # Additional logic for handling valid clicks...

    def limpiar_tablero(canvas, lineas_dibujadas):
        for id_linea, _ in lineas_dibujadas.values():
            canvas.delete(id_linea)
        lineas_dibujadas.clear()