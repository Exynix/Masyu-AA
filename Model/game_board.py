# Game_Board.py
from .Board_Cell import BoardCell
from .cell_types_enum import CellTypesEnum

class GameBoard:

    def __init__(self, matrix_size) -> None:

        # Creation of matrix of n x n size.
        self.matrix = [[BoardCell() for _ in range(matrix_size)] for iteration in range(matrix_size)]
