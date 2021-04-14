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
    print() # blank line
    print() # blank line
    for j in range(y):
        row = "{:2d}".format(y-j-1)  # first character is Y axis value
        for k in range(x):
            row = row + grid[k + j*x]  # add to row
        print(row)

def show_level(level):
    if level == "1":
        print("Game level is Beginner")
    elif level == "2":
        print("Game level is Medium")
    elif level == "3":
        print("Game level is Advanced")
    else:   # level == 4
        print("Game level is Expert")
      
           
def get_level():  # determine what level of game to play
    valid_value = False
    while not valid_value:
        level = input("What level of game do you want:\n 1. Beginner\n 2. Medium\n 3. Advanced\n 4. Expert\n")
        if level not in ["1", "2", "3", "4"]:
            print("{} is not a valid value ... try again!".format(level))
        else:
            show_level(level)
            valid_value = True
    return level

def add_mines(grid, level, MINE):
    if level == "1":
        num_mines = BEGINNER
    elif level == "2":
        num_mines = MEDIUM
    elif level == "3":
        num_mines = ADVANCED
    else:    # level == 4
        num_mines = EXPERT

    for j in range(num_mines):
        index = random.randint(0, len(grid) - 1)
        grid[index] = KNOWN_MINE

    return(grid)
    
def enter_choice():
    x = input("Enter x value choice: ")
    y = input("Enter y value choice: ")
    print("You entered co-ordinates of {},{}".format(x, y))
    return (x,y)



grid = create_grid(X, Y, UNKNOWN)

show_grid(X, Y, grid)

level = get_level()

grid = add_mines(grid, level, UNKNOWN_MINE)
show_grid(X, Y, grid)

playing_game = True

while playing_game:
    show_grid(X, Y, grid)
    (x,y) = enter_choice()
