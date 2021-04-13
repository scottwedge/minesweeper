#!/usr/bin/env python3

# Simple MineSweeper program

# Import
import random

# Constants
X = 30  # width
Y = 16  # height
BEGINNER = 25 # number of mines based on difficulty level
MEDIUM = 50
ADVANCED = 75
EXPERT = 99
UNKNOWN = "."
UNKNOWN_MINE = "."
KNOWN_MINE = "M"
BLANK = " "



def create_grid(height, width, init_value):
    game_list = [] # initialize blank list
    for j in range(height * width):
        game_list.append(init_value)
    return game_list

def show_grid(x, y, grid):
    for j in range(y):
        row = ""  # initialize blank row
        for k in range(x):
            row = row + grid[k + j*x]  # add to row
        print(row)
           
def get_level():  # determine what level of game to play
    valid_value = False
    while not valid_value:
        level = input("What level of game do you want:\n 1. Beginner\n 2. Medium\n 3. Expert\n")
        if level not in ["1", "2", "3", "4"]:
            print("{} is not a valid value ... try again!".format(level))
        else:
            valid_value = True
    return level

def add_mines(grid, level, MINE):
    if level == "1":
        num_mines = BEGINNER
    elif level == "2":
        num_mines = MEDIUM
    else:
        num_mines = EXPERT

    for j in range(num_mines):
        index = random.randint(0, len(grid) - 1)
        grid[index] = MINE

    return(grid)
    



grid = create_grid(X, Y, UNKNOWN)

show_grid(X, Y, grid)

level = get_level()

print(level)   # DEBUG

grid = add_mines(grid, level, UNKNOWN_MINE)
show_grid(X, Y, grid)
