#!/usr/bin/env python3

# Simple MineSweeper program

# Import
import random

# Constants
X = 30  # width
Y = 15  # height
BEGINNER = 25 # number of mines based on difficulty level
MEDIUM = 50
ADVANCED = 75
EXPERT = 99

UNKNOWN = "."
UNKNOWN_MINE = "U"
KNOWN_MINE = "M"
BLANK = " "

# Where (x,y) of (0,0) is top left square
# Where (x,y) of (X-1, Y-1) is bottom right square


def create_grid(width, height, init_value):
    game_list = [] # initialize blank list
    for j in range(height * width):
        game_list.append(init_value)
    return game_list

def print_top_x_value(x):
    s = "  " # initialize blank string for two digit wide y column
    for j in range(x):
        s = s + str(j // 10)
    print(s)

def print_bottom_x_value(x):
    s = "  " # initialize blank string for two digit wide y column
    for j in range(x):
        s = s + str(j % 10)
    print(s)

def show_grid(x, y, grid):
    print() # blank line
    print() # blank line
    print_top_x_value(X)   # move X-axis label to top of grid
    print_bottom_x_value(X)
    for j in range(y):
        row = "{:2d}".format(j)  # first character is Y axis value
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
    print() # blank line
    print() # blank line
    valid_value = False
    while not valid_value:
        level = input("What level of game do you want:\n 1. Beginner\n 2. Medium\n 3. Advanced\n 4. Expert\n")
        if level not in ["1", "2", "3", "4"]:
            print("{} is not a valid value ... try again!".format(level))
        else:
            show_level(level)
            valid_value = True
    return level

def add_mines(grid, level, UNKNOWN_MINE):
    if level == "1":
        num_mines = BEGINNER
    elif level == "2":
        num_mines = MEDIUM
    elif level == "3":
        num_mines = ADVANCED
    else:    # level == 4
        num_mines = EXPERT

    for j in range(num_mines):
        random.seed()   # randomize seed
        index = random.randint(0, len(grid) - 1)
        grid[index] = UNKNOWN_MINE

    return(grid)
    
def enter_choice(width, height):
    print() # blank line
    valid_x = False
    while not valid_x:
        x = input("Enter x value choice: ")
        if x.isnumeric():
            x = int(x)
            if x in range(width):
                valid_x = True
        else:
            print("{} is not a valid value, try again".format(x))

    valid_y = False
    while not valid_y:
        y = input("Enter y value choice: ")
        if y.isnumeric():
            y = int(y)
            if y in range(height):
                valid_y = True
        else:
            print("{} is not a valid value, try again".format(y))
    print("You entered (x,y) co-ordinates of ({},{})".format(x, y))
    return (x,y)

def check_above(grid, x, y, X, Y):  # check three squares above          
    count = 0
    if y > 0:
        if x > 0 and x < X - 1:  # majority of cases without boundary conditions
            if grid[x - 1 + (y - 1) * X] == UNKNOWN_MINE:  # above left
                count = count + 1
            if grid[x + (y - 1) * X] == UNKNOWN_MINE:      # directory above
                count = count + 1
            if grid[x + 1 + (y - 1) * X] == UNKNOWN_MINE:  # above right
                count = count + 1
        elif x == 0:  # left boundary conditions
            if grid[x + (y - 1) * X] == UNKNOWN_MINE:      # left-most
                count = count + 1
            if grid[x + 1 + (y - 1) * X] == UNKNOWN_MINE:  # second from left
                count = count + 1
        elif x == X - 1:  # right boundary conditions
            if grid[x - 1 + (y - 1) * X] == UNKNOWN_MINE:  # second from right
                count = count + 1
            if grid[x + (y - 1) * X] == UNKNOWN_MINE:      # right-most
                count = count + 1
        else:
            pass
    else:   # y == 0
        pass
    return count

def check_below(grid, x, y, X, Y):  # check three squares below          
    count = 0
    if y < Y - 1:
        if x > 0 and x < X - 1:  # majority of cases without boundary conditions
            if grid[x - 1 + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
            if grid[x + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
            if grid[x + 1 + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
        elif x == 0:  # bottom left boundary conditions
            if grid[x + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
            if grid[x + 1 + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
        elif x == X - 1:  # bottom right boundary conditions
            if grid[x - 1 + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
            if grid[x + (y + 1) * X] == UNKNOWN_MINE:
                count = count + 1
        else:
            pass
    else:   # y == Y-1
        pass
    return count

def check_left(grid, x, y, X, Y):  # check one square to the left
    count = 0
    if x > 0:
        if grid[x - 1 + y * X] == UNKNOWN_MINE:
            count = count + 1
    else:  # x = 0
        pass
    return count

def check_right(grid, x, y, X, Y):  # check one square to the right
    count = 0
    if x < X - 1:
        if grid[x + 1 + y * X] == UNKNOWN_MINE:
            count = count + 1
    return count

def calculate_neighbours(grid, X, Y):
    for x in range(X):
        for y in range(Y):
            if grid[x + y * X] == UNKNOWN:  # if not a mine
                count_above = check_above(grid, x, y, X, Y)  # check three squares above          
                count_below = check_below(grid, x, y, X, Y)  # check three squares below 
                count_left = check_left(grid, x, y, X, Y)   # check square to the left 
                count_right = check_right(grid, x, y, X, Y)  # check square to the right 
                sum = count_above + count_below + count_left + count_right
                if sum == 0:
                    sum = "."  # DEBUG - replace "0" with "." to allow easy visual checking
                else:
                    #print(x,y, "above:", count_above,"below:", count_below,"L:", count_left,"R:",count_right)   # DEBUG
                    sum = str(sum)      #DEBUG
                grid[x + y * X] = sum     # convert integer to string
    return grid

def reveal_neighbours(x, y, X, Y, known_grid, unknown_grid):
    pass
    return unknown_grid

def analyze_choice(x, y, X, Y, known_grid, unknown_grid):  # check spot selected
    playing_game = True # set default
    print("Spot ({},{}) is {}".format(x, y, known_grid[x + y * X]))   # DEBUG
    spot = known_grid[x + y * X]
    if spot == UNKNOWN_MINE:  # game over - lose
        playing_game = False
        print("Game over since selected mine.")    
    if spot == KNOWN_MINE:   # game over - lose
        playing_game = False
        print("Game over since selected mine.")   
    if spot == UNKNOWN:    # reveal value
       unknown_grid[x + y * X] = BLANK   
       unknown_grid = reveal_neighbours(x, y, X, Y, known_grid, unknown_grid)
    return (unknown_grid, playing_game)    # update unknown grid values

    

# Initialize grid
unknown_grid = create_grid(X, Y, UNKNOWN)  # Create empty grid of size X by Y
known_grid = create_grid(X, Y, UNKNOWN)          # Create empty grid of size X by Y

show_grid(X, Y, known_grid)

level = get_level()

known_grid = add_mines(known_grid, level, UNKNOWN_MINE)   # Add mines to empty grid
show_grid(X, Y, known_grid)

known_grid = calculate_neighbours(known_grid, X, Y)      # Calculate number of neighbour mines for each non-mine square

show_grid(X, Y, known_grid)

playing_game = True

while playing_game:
    show_grid(X, Y, unknown_grid)
    (x,y) = enter_choice(X, Y)
    
    (unknown_grid, playing_game) = analyze_choice(x, y, X, Y, known_grid, unknown_grid)
