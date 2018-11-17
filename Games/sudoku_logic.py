from solver import *
from library import *

def sudoku(board, should_print=False):
    reset()

    # Set up the variables for each cell
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == '.': 
                board[i][j] = declare(str(i) + "," + str(j), Integer)
 
    # Numbers are between 1 and 9
    for i in range(0, 9):
        for j in range(0, 9):
            assume(board[i][j] > 0)
            assume(board[i][j] < 10)

    # Numbers in each row are unique
    for i in range(0, 9): assume(Distinct([board[i][j] for j in range(9)]))

    # Numbers in each column are unique
    for j in range(0, 9): assume(Distinct([board[i][j] for i in range(9)]))

    # Numbers in each square are unique
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            assume(Distinct([board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)])) 

    if should_print:
        print_board(board, solve(1)[0])