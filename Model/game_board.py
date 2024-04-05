from board_cell import BoardCell

class GameBoard:

    def __init__(self, matrix_size) -> None:

        # Creation of matrix of n x n size.
        self.matrix_cells = [[BoardCell() for iteration in range(matrix_size)] for iteration in range(matrix_size)]


