from collections import namedtuple, defaultdict

import time
import os
import sys
import random

WIDTH, HEIGHT = os.get_terminal_size()
Cell = namedtuple("Cell", ["x", "y"])
Board = dict[Cell, int]

# return set of alive x y co-ordinates
def getNextState(board):
    new_board = set()
    for cell, count in getNeighbourCounts(board).items():
        if count == 3 or (cell in board and count == 2):
            new_board.add(cell)
    return new_board

# for each alive cell, return total number of alive cells that are adjacent
def getNeighbourCounts(board) -> Board:
    neighbour_counts = defaultdict(int)
    for cell in board:
        for neighbour in get8Neighbours(cell):
            neighbour_counts[neighbour] += 1
    return neighbour_counts

# generator/yield (https://book.pythontips.com/en/latest/generators.html#id1)
def get8Neighbours(cell: Cell):
    for x in range(cell.x - 1, cell.x + 2):
        for y in range(cell.y - 1, cell.y + 2):
            if (x, y) != (cell.x, cell.y):
                yield Cell(x, y)

def randomSeed():
    board = set()
    for x in range(WIDTH // 2):
        for y in range(HEIGHT // 2):
            if random.randint(0, 1) == 0:
                board.add(Cell(x, y))
        return board

def boardStringify(board, xypad=0):
    if not board:
        return "empty"
    board_str = ""
    xs = [x for (x, _) in board]
    ys = [y for (_, y) in board]
    for y in range(min(ys) - xypad, max(ys) + 1 + xypad):
        for x in range(min(xs) - xypad, max(xs) + 1 + xypad):
            board_str += "X" if Cell(x, y) in board else "█"
        board_str += "\n"
    return board_str.strip()

def clearscreen():
    if os.name == "posix":  # Unix/Linux/MacOS/BSD/and so on
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):  # DOS/Windows
        os.system('CLS')


if __name__ == "__main__":
    board = randomSeed()
    while board:
        board = getNextState(board)
        # if board == 'empty':
        #   os._exit()
        clearscreen()
        print(boardStringify(board))
        print('press ctrl+C to quit')
        time.sleep(0.3)
