from Model.Game_Board import GameBoard

def print_game_board(game_board:GameBoard):
    for row in game_board.matrix:
        for cell in row:
            print (row, '\n')
            print (cell, '\n')
            print (cell.type) 