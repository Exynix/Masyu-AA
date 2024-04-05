from Proyect_Masyu.Model.CellTypesEnumerations import CellTypesEnum

class BoardCell:

    # Constructor
    def __init__(self) -> None:
        self.type = CellTypesEnum.NOTYPE
        self.connecting_cells = [] # List of "squares" this cell is connecting.