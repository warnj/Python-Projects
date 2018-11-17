from library import *

def sudoku(board, should_print=False):
    todo = []
    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] == '.':
                todo.append((i, j))
    assn = {}
    solve(board, todo, assn)

    if should_print:
        print_board(board, assn)

def Distinct(L):
    L.sort()
    for i in range(len(L) - 1):
        if L[i] == L[i + 1]:
            return False
    return True

def check(board, square, value):
    a, b = square
    row = [board[a][j] for j in range(0, 9) if type(board[a][j]) != str] + [value]
    col = [board[i][b] for i in range(0, 9) if type(board[i][b]) != str] + [value]
    sqx, sqy = a - a % 3, b - b % 3
    square = [board[i][j] for i in range(sqx, sqx + 3) for j in range(sqy, sqy + 3) if type(board[i][j]) != str] + [value]

    return Distinct(row) and Distinct(col) and Distinct(square)

def solve(board, todo, assn):
    if len(todo) == 0:
        return True
    s = todo.pop() 
    for i in range(0, 9):
        if check(board, s, i + 1):
            assn[str(s[0]) + "," + str(s[1])] = i + 1 
            board[s[0]][s[1]] = i + 1
            if solve(board, todo, assn):
                return True
            del assn[str(s[0]) + "," + str(s[1])]
            board[s[0]][s[1]] = '.' 
    todo.append(s)
    return False