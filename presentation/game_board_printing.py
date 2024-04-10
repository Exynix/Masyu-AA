# game_board_printing.py
import tkinter as tk

from Model.Game_Board import GameBoard
from Model.cell_types_enum import CellTypesEnum

def print_game_board(game_board):
    # Define the size of the window and the cells
    cell_size = 50
    window_size = cell_size * len(game_board.matrix)
    
    # Create the Tkinter window
    root = tk.Tk()
    canvas = tk.Canvas(root, width=window_size, height=window_size)
    canvas.pack()

    # Loop over the matrix and draw the board
    for i, row in enumerate(game_board.matrix):
        for j, cell in enumerate(row):
            # Calculate the top-left corner of the cell
            x1 = j * cell_size
            y1 = i * cell_size
            # Calculate the bottom-right corner of the cell
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            # Draw the cell as a rectangle
            canvas.create_rectangle(x1, y1, x2, y2)
            
            # Check the cell type and draw pearls accordingly
            if cell.type == CellTypesEnum.WHITEPEARL:
                # Calculate the center of the cell for the pearl
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                # Draw a white pearl (oval) inside the cell
                canvas.create_oval(center_x - 10, center_y - 10, center_x + 10, center_y + 10, fill='white')
            elif cell.type == CellTypesEnum.BLACKPEARL:
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                # Draw a black pearl (oval) inside the cell
                canvas.create_oval(center_x - 10, center_y - 10, center_x + 10, center_y + 10, fill='black')

    # Run the Tkinter loop
    root.mainloop()
