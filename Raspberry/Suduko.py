import numpy as np

import pandas as pd

import time

import itertools

sudoku_df = ""

def shape(sudoku_df):
    for n in range(len(sudoku_df)):
        sudoku_df= np.reshape(list(sudoku_df), (9, 9)).astype(int)

    return sudoku_df

def checkPuzzle(sudoku_puzzle):
    checkRow = all([all([x in sudoku_puzzle[nrow,:] for x in range(1,10)]) for nrow in range(9)])
    checkCol = all([all([x in sudoku_puzzle[:,ncol] for x in range(1,10)]) for ncol in range(9)])

    checkUpperLeft = all([x in sudoku_puzzle[0:3,0:3] for x in range(1,10)])
    checkUpperMid = all([x in sudoku_puzzle[0:3,3:6] for x in range(1,10)])
    checkUpperRight = all([x in sudoku_puzzle[0:3,6:9] for x in range(1,10)])

    checkMidLeft = all([x in sudoku_puzzle[3:6,0:3] for x in range(1,10)])
    checkMidMid = all([x in sudoku_puzzle[3:6,3:6] for x in range(1,10)])
    checkMidRight = all([x in sudoku_puzzle[3:6,6:9] for x in range(1,10)])

    checkLowerLeft = all([x in sudoku_puzzle[6:9,0:3] for x in range(1,10)])
    checkLowerMid = all([x in sudoku_puzzle[6:9,3:6] for x in range(1,10)])
    checkLowerRight = all([x in sudoku_puzzle[6:9,6:9] for x in range(1,10)])

    solved = all([checkRow,checkCol,checkUpperLeft,checkUpperMid,checkUpperRight,
                  checkMidLeft,checkMidMid,checkMidRight,checkLowerLeft,checkLowerMid,checkLowerRight])
    if solved:
        for line in sudoku_puzzle:
            print(*line)
    return solved



def checkGrids(r,c,sudoku_puzzle,n):
    if r < 3:
        if c < 3:
            subgrid = n in sudoku_puzzle[0:3, 0:3]
        elif c < 6:
            subgrid = n in sudoku_puzzle[0:3, 3:6]
        else:
            subgrid = n in sudoku_puzzle[0:3, 6:9]
    elif r < 6:
        if c < 3:
            subgrid = n in sudoku_puzzle[3:6, 0:3]
        elif c < 6:
            subgrid = n in sudoku_puzzle[3:6, 3:6]
        else:
            subgrid = n in sudoku_puzzle[3:6, 6:9]
    else:
        if c < 3:
            subgrid = n in sudoku_puzzle[6:9, 0:3]
        elif c < 6:
            subgrid = n in sudoku_puzzle[6:9, 3:6]
        else:
            subgrid = n in sudoku_puzzle[6:9, 6:9]
    return subgrid

def solve(sudoku_puzzle,puzzle_values):
    count = 0
    solution = False
    rows = np.array(np.where(sudoku_puzzle == 0))[0]
    cols = np.array(np.where(sudoku_puzzle == 0))[1]
    dic = dict(zip(list(range(len(rows))), np.zeros(len(rows),dtype = int).tolist()))
    while solution == False:
        if count >= len(rows):
            solution = checkPuzzle(sudoku_puzzle)
            return sudoku_puzzle
            break
        r = rows[count]
        c = cols[count]
        len_num = len(np.array(puzzle_values).reshape(9, 9)[r, c])
        num = dic[count]
        while num < len_num:
            cell = np.array(puzzle_values).reshape(9, 9)[r, c][num]
            checkRow = cell in sudoku_puzzle[r, :]
            if checkRow:
                num += 1
                continue
            checkCol = cell in sudoku_puzzle[:, c]
            if checkCol:
                num += 1
                continue
            checkGrid = checkGrids(r, c, sudoku_puzzle, cell)
            if checkGrid:
                num += 1
                continue
            dic[count] = num
            count += 1
            sudoku_puzzle[r, c] = cell
            break
        else:
            sudoku_puzzle[r, c] = 0
            dic[count] = 0
            count -= 1



def determineValues(sudoku_puzzle):
    puzzle_values = list()
    for r in range(9):
        for c in range(9):
            if sudoku_puzzle[r,c] == 0:
                cell_values = np.array(range(1,10))
                cell_values = np.setdiff1d(cell_values,sudoku_puzzle[r,:][np.where(sudoku_puzzle[r,:] != 0)]).tolist()
                cell_values = np.setdiff1d(cell_values,sudoku_puzzle[:,c][np.where(sudoku_puzzle[:,c] != 0)]).tolist()
            else:
                cell_values = [sudoku_puzzle[r,c]]
            puzzle_values.append(cell_values)
    return puzzle_values

def solverController(values):
    sudoku_df = values
    sudoku_df_arr = sudoku_df
    sudoku_df = shape(sudoku_df)
    puzzle_values = determineValues(sudoku_df)
    solved_puzzle = solve(sudoku_df, puzzle_values)
    solved_puzzle_arr = solved_puzzle.reshape(-1)
    solution = np.empty(81)
    for i in range (0,81):
        solution[i] = abs(int(sudoku_df_arr[i])-int(solved_puzzle_arr[i]))

    mat_sol = np.reshape(solution, (9,9))
    #print(mat_sol)
    return mat_sol.astype(int).tolist()
