# Board_Cell.py
from .cell_types_enum import CellTypesEnum

class BoardCell:

    # Constructor
    def __init__(self) -> None:
        self.type = CellTypesEnum.NOTYPE  # Use the enum directly
        self.connecting_cells = []  # List of "squares" this cell is connecting.

    def change_type(self, new_type: CellTypesEnum):
        if not isinstance(new_type, CellTypesEnum):
            raise ValueError("new_type must be an instance of CellTypesEnum")
        self.type = new_type

    def __str__(self):
        return f"BoardCell({self.type.name})"
