# masyy_game_gui.py
from tkinter import *
from tkinter import messagebox

from Model.Game_Board import GameBoard  
from Model.cell_types_enum import CellTypesEnum

class MasyuGameGUI:
    def __init__(self, game_board):
        self.game_board = game_board
        self.lineas_dibujadas = {}  # Initialize here
        self.canvas = None  # Will be initialized in print_game_board
    
    def print_game_board(self, game_board: GameBoard) -> None :
        lineas_dibujadas = {}

        raiz = Tk()
        raiz.title("Masyu")

        miFrame = Frame(raiz)
        miFrame.pack(expand=True, fill="both", padx=20, pady=20)

        botonesFrame = Frame(miFrame)
        botonesFrame.pack(side=TOP, pady=10)

        boton_limpiar = Button(botonesFrame, text="Limpiar Tablero", command=self.limpiar_tablero)
        boton_limpiar.pack(side=LEFT, padx=5)

        boton_jugador_sintetico = Button(botonesFrame, text="Jugador Sintético")  # Implement its functionality as needed
        boton_jugador_sintetico.pack(side=LEFT, padx=5)

        textoLabel = Label(miFrame, text="Masyu!", fg="red", font=("System", 18))
        textoLabel.pack(side=TOP, pady=(0, 20))

        num_filas_columnas = len(game_board.matrix)
        self.canvas = Canvas(miFrame, width=50*num_filas_columnas, height=50*num_filas_columnas, bg="white")  # Set self.canvas here
        self.canvas.pack()

        self.canvas.bind("<Button-1>", lambda event: self.on_cell_click(event))
        self.canvas.bind("<Button-3>", lambda event: self.on_cell_click(event))


        # Draw the grid and pearls based on the GameBoard state
        for i, row in enumerate(game_board.matrix):
            for j, cell in enumerate(row):
                self.canvas.create_rectangle(50 * j, 50 * i, 50 * (j + 1), 50 * (i + 1), outline="grey")
                if cell.type == CellTypesEnum.WHITEPEARL:
                    self.canvas.create_oval(50 * j + 10, 50 * i + 10, 50 * (j + 1) - 10, 50 * (i + 1) - 10, fill="white", outline="black")
                elif cell.type == CellTypesEnum.BLACKPEARL:
                    self.canvas.create_oval(50 * j + 10, 50 * i + 10, 50 * (j + 1) - 10, 50 * (i + 1) - 10, fill="black")
                
        self.root =  raiz
        self.root.mainloop()

    def on_cell_click(self, event):
        cell_size = 50
        x, y = event.x, event.y
        column, row = x // cell_size, y // cell_size
        current_cell = self.game_board.matrix[row][column]

        # Right-click to erase a line
        if event.num == 3:
            self.erase_line(current_cell)
            # Redraw the grid line to ensure consistency in the visual representation
            self.canvas.create_rectangle(column * cell_size, row * cell_size,
                                         (column + 1) * cell_size, (row + 1) * cell_size, outline="grey")
            return

        # Increment click count or initialize if not already set
        if hasattr(current_cell, 'click_count'):
            current_cell.click_count += 1
        else:
            current_cell.click_count = 1

        # Cycle through line/connection types with each left click
        click_type = current_cell.click_count % 5  # 0: Clear, 1: Vertical, 2: Horizontal, 3: Right angle 1, 4: Right angle 2

        # First, clear any existing line/connection for the current cell
        self.erase_line(current_cell)
        # Then, based on the click count, draw the appropriate line/connection
        if click_type == 1:
            self.draw_vertical_line(current_cell, row, column)
        elif click_type == 2:
            self.draw_horizontal_line(current_cell, row, column)
        elif click_type == 3:
            self.draw_right_angle_line_1(current_cell, row, column)
        elif click_type == 4:
            self.draw_right_angle_line_2(current_cell, row, column)
        # If click_type is 0, the line/connection is already cleared by erase_line

    def draw_vertical_line(self, cell, row, column):
        # Draw a vertical line through the current cell
        self.canvas.create_line(column * 50 + 25, row * 50, column * 50 + 25, (row + 1) * 50, fill="black", width=2)
        # Update connections
        if row > 0 and row < len(self.game_board.matrix) - 1:
            top_cell = self.game_board.matrix[row - 1][column]
            bottom_cell = self.game_board.matrix[row + 1][column]
            cell.add_connection(top_cell, bottom_cell)

    def draw_horizontal_line(self, cell, row, column):
        # Draw a horizontal line through the current cell
        self.canvas.create_line(column * 50, row * 50 + 25, (column + 1) * 50, row * 50 + 25, fill="black", width=2)
        # Update connections
        if column > 0 and column < len(self.game_board.matrix[0]) - 1:
            left_cell = self.game_board.matrix[row][column - 1]
            right_cell = self.game_board.matrix[row][column + 1]
            cell.add_connection(left_cell, right_cell)

    def draw_right_angle_line_1(self, cell, row, column):
    # Assuming this right angle turns down then right
    # Clear any existing drawing on the cell
        self.erase_line(cell)

        # Draw the right angle only if it doesn't go out of bounds
        if row < len(self.game_board.matrix) - 1 and column < len(self.game_board.matrix[0]) - 1:
            # Get the bottom and right cells for the connection
            bottom_cell = self.game_board.matrix[row + 1][column]
            right_cell = self.game_board.matrix[row][column + 1]
            
            # Add a connection between these cells
            cell.add_connection(bottom_cell, right_cell)

            # Draw the lines representing the right angle
            # First line: Current cell to the bottom cell
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, column * 50 + 25, (row + 1) * 50, fill="black", width=2)
            # Second line: Bottom cell to the right cell (this line starts from the bottom cell center)
            self.canvas.create_line(column * 50 + 25, (row + 1) * 50, (column + 1) * 50 + 25, (row + 1) * 50, fill="black", width=2)



    def draw_right_angle_line_2(self, cell, row, column):
    # This example assumes a right angle pointing up and right from the cell
        if row > 0 and column < len(self.game_board.matrix[0]) - 1:
            top_cell = self.game_board.matrix[row - 1][column]
            right_cell = self.game_board.matrix[row][column + 1]
            cell.add_connection(top_cell, right_cell)
            # Draw the lines representing the right angle
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, column * 50 + 25, row * 50, fill="black", width=2)  # Up
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, (column + 1) * 50, row * 50 + 25, fill="black", width=2)  # Right


    def erase_line(self, cell):
        # Clear any visual line from the cell
        row, column = cell.row, cell.column
        # Recreate the rectangle to "erase" any line
        self.canvas.create_rectangle(column * 50, row * 50, (column + 1) * 50, (row + 1) * 50, fill="white", outline="grey")
        # Redraw the pearl if present
        if cell.type == CellTypesEnum.WHITEPEARL:
            self.canvas.create_oval(column * 50 + 10, row * 50 + 10, (column + 1) * 50 - 10, (row + 1) * 50 - 10, fill="white", outline="black")
        elif cell.type == CellTypesEnum.BLACKPEARL:
            self.canvas.create_oval(column * 50 + 10, row * 50 + 10, (column + 1) * 50 - 10, (row + 1) * 50 - 10, fill="black")
        # Remove all existing connections
        while cell.connected_cells:
            conn = cell.connected_cells.pop()
            cell.remove_connection(*conn)


    def limpiar_tablero(self):
        for id_linea, _ in self.lineas_dibujadas.values():
            self.canvas.delete(id_linea)
        self.lineas_dibujadas.clear()