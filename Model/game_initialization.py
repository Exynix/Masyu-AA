from FileHandling import file_handling
from presentation import interfaz
from presentation.game_board_printing import print_game_board
from .Game_Board import GameBoard
from .cell_types_enum import CellTypesEnum

#---------------------------------------------------------------
def initiateGame():
    nombre_archivo = input("Ingrese el nombre del archivo con el que desea jugar (incluya el .txt en el nombre): ")
    num_filas_columnas, configuraciones = file_handling.leer_archivo(nombre_archivo)
    createBoard(num_filas_columnas, configuraciones)
    
    if num_filas_columnas > 0:
        app = interfaz.crear_interfaz(num_filas_columnas, configuraciones)
        app.mainloop()
    else:
        print("Error al leer el archivo de configuración. El tamaño indicado de la matriz es 0 o negativo.")

# --------------------------------------------------------------- 
"""
    Input:  file_configurations is a list. Each item from the list is a line from the provided configuration file.
        Each row contains 3 numerical parts, or tokens.
        - The first part is the row number.
        - The second part is the column number.
        - The third part is the type of pearl.
"""
def createBoard(matrix_size: int, file_configurations: list):
    game_board = GameBoard(matrix_size)

    for line in file_configurations:
        row, column, pearl_type = line.strip().split(",")  # Remove whitespace after splitting
        row, column, pearl_type = int(row), int(column), int(pearl_type)  # Convert to integers

        # Directly use the enum to change the type
        if pearl_type == 1:  # 1 -> Perla Blanca, 2 -> Perla Negra
            game_board.matrix[row-1][column-1].change_type(CellTypesEnum.WHITEPEARL)
        elif pearl_type == 2:
            game_board.matrix[row-1][column-1].change_type(CellTypesEnum.BLACKPEARL)

    print_game_board(game_board)




    