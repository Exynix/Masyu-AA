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
            self.canvas.create_rectangle(column * cell_size, row * cell_size,
                                        (column + 1) * cell_size, (row + 1) * cell_size, outline="grey")
            return

        # Increment click count or initialize if not already set
        if hasattr(current_cell, 'click_count'):
            current_cell.click_count += 1
        else:
            current_cell.click_count = 1

        
            # For other cells, cycle through options
        click_type = current_cell.click_count % 5

    
        # First, clear any existing line/connection for the current cell
        self.erase_line(current_cell)

        # Draw the line/connection based on click type
        if click_type == 1:
            self.draw_vertical_line(current_cell, row, column)
            
            if self.check_for_cycle():
                messagebox.showinfo("Cycle Detected", "A closed loop has been formed!")

        elif click_type == 2:
            self.draw_horizontal_line(current_cell, row, column)        
            if self.check_for_cycle():
                messagebox.showinfo("Cycle Detected", "A closed loop has been formed!")    
        elif click_type == 3 or (current_cell.type == CellTypesEnum.BLACKPEARL and click_type in [1, 2]):
        # Draw the right angle for black pearls or as per click count
            self.draw_right_angle(current_cell, row, column, current_cell.click_count)
            if self.check_for_cycle():
                messagebox.showinfo("Cycle Detected", "A closed loop has been formed!")

        # If click_type is 0, the line/connection has been cleared by erase_line


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


    def draw_right_angle(self, cell, row, column, click_count):
        # Calculate the angle orientation based on the click count
        angle_orientation = click_count % 4  # There are four possible orientations for a right angle

        # Clear any existing drawing on the cell
        self.erase_line(cell)

        # Define the cells to connect and lines to draw based on the orientation
        if angle_orientation == 0:  # Right and down
            connected_cells = (self.get_cell(row, column + 1), self.get_cell(row + 1, column))
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, (column + 1) * 50, row * 50 + 25, fill="black", width=2)  # Horizontal line
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, column * 50 + 25, (row + 1) * 50, fill="black", width=2)  # Vertical line
        elif angle_orientation == 1:  # Down and left
            connected_cells = (self.get_cell(row + 1, column), self.get_cell(row, column - 1))
            self.canvas.create_line(column * 50, row * 50 + 25, column * 50 + 25, row * 50 + 25, fill="black", width=2)  # Horizontal line
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, column * 50 + 25, (row + 1) * 50, fill="black", width=2)  # Vertical line
        elif angle_orientation == 2:  # Left and up
            connected_cells = (self.get_cell(row, column - 1), self.get_cell(row - 1, column))
            self.canvas.create_line(column * 50, row * 50 + 25, column * 50 + 25, row * 50 + 25, fill="black", width=2)  # Horizontal line
            self.canvas.create_line(column * 50 + 25, row * 50, column * 50 + 25, row * 50 + 25, fill="black", width=2)  # Vertical line
        elif angle_orientation == 3:  # Up and right
            connected_cells = (self.get_cell(row - 1, column), self.get_cell(row, column + 1))
            self.canvas.create_line(column * 50 + 25, row * 50 + 25, (column + 1) * 50, row * 50 + 25, fill="black", width=2)  # Horizontal line
            self.canvas.create_line(column * 50 + 25, row * 50, column * 50 + 25, row * 50 + 25, fill="black", width=2)  # Vertical line

        # Remove any previous connections
        while cell.connected_cells:
            cell.connected_cells.pop()

        # Add the new connections
        if all(connected_cells):
            cell.add_connection(*connected_cells)


    def get_cell(self, row, column):
        # Safely retrieve a cell object if within bounds
        if 0 <= row < len(self.game_board.matrix) and 0 <= column < len(self.game_board.matrix[0]):
            return self.game_board.matrix[row][column]
        return None




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


    def check_for_cycle(self):
        visited = set()
    
        def dfs(cell, origin):
            # If we've returned to the origin cell via different paths, it's a loop.
            if cell in visited:
                if origin in cell.connected_cells:
                    return True
                return False
            visited.add(cell)

            # Explore each connected cell.
            for conn_cells in cell.connected_cells:
                # Determine which cell is the next one to explore.
                next_cell = conn_cells[0] if conn_cells[1] == cell else conn_cells[1]

                # Skip backtracking to the cell we came from.
                if origin is not None and next_cell == origin:
                    continue

                # Continue the DFS from the next cell.
                if dfs(next_cell, cell if origin is None else origin):
                    return True

            return False

        # Start the DFS from each cell that has connections
        for row in self.game_board.matrix:
            for cell in row:
                visited.clear()  # Clear visited before each new DFS
                if cell.connected_cells and dfs(cell, None):
                    return True
        return False


