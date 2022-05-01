#!/usr/bin/env python3

# Simple MineSweeper program
# Initially configure all spots in 'unknown_grid' as "." aka unknown.
# Randomly position the mines and then calculate all neighbour counts in 'known_grid'.
# Copy user guess (x,y) value from 'known_grid' into 'unknown_grid'.

# Import
import random

# Constants
X = 30  # width (left-most column = 0)
Y = 15  # height (top-most row = 0)
BEGINNER = 25 # number of mines based on difficulty level (out of 450 spots)
MEDIUM = 50
ADVANCED = 75
EXPERT = 99
CUSTOM = 0

UNKNOWN = "."
UNKNOWN_MINE = "U"
KNOWN_MINE = "M"
BLANK = " "

# Where (x,y) of (0,0) is top left square
# Where (x,y) of (X-1, Y-1) is bottom right square


def init_grid(width, height, init_value):
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
    elif level == "4":
        print("Game level is Expert")
    else:   # level == 5  # Custom grid
        print("Game level is Custom")
      
           
def get_level():  # determine what level of game to play
    print() # blank line
    print() # blank line
    valid_value = False
    while not valid_value:
        level = input("What level of game do you want:\n 1. Beginner\n 2. Medium\n 3. Advanced\n 4. Expert\n 5. Custom\n")
        if level not in ["1", "2", "3", "4", "5"]:
            print()  # blank spacer line
            print("\033[1m{} is not a valid value ... try again!\033[0m".format(level))
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
    elif level == "4":
        num_mines = EXPERT
    else:
        num_mines = 1
        pass  # Invalid option

#    print("DEBUG____ grid=", grid)  #DEBUG

    for j in range(num_mines):
        random.seed()   # randomize seed
        index = random.randint(0, len(grid) - 1)
        grid[index] = UNKNOWN_MINE
    return grid


def make_custom_grid(grid, level, UNKNOWN_MINE):
    # Create a two rows of mines in middle of grid (to help test debugging)
    min1 = 150
    max1 = 179
    min2 = 300
    max2 = 329
    for j in range(min1, max1 + 1):
        grid[j] = UNKNOWN_MINE 
    for j in range(min2, max2 + 1):
        grid[j] = UNKNOWN_MINE 
    return grid


def create_grid(grid, level, UNKNOWN_MINE):
    if level == "5":
        grid = make_custom_grid(grid, level, UNKNOWN_MINE)
    else:
        grid = add_mines(grid, level, UNKNOWN_MINE)
    return grid
    

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
            print("\033[1m{} is not a valid value, try again\033[0m".format(x))

    valid_y = False
    while not valid_y:
        y = input("Enter y value choice: ")
        if y.isnumeric():
            y = int(y)
            if y in range(height):
                valid_y = True
        else:
            print("{} is not a valid value, try again".format(y))
    print("You entered (x,y) co-ordinates of ({},{}). ".format(x, y), end = "")
    return (x,y)


def count_above(grid, x, y, X, Y):  # check three squares above          
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


def count_below(grid, x, y, X, Y):  # check three squares below          
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


def count_left(grid, x, y, X, Y):  # check one square to the left
    count = 0
    if x > 0:
        if grid[x - 1 + y * X] == UNKNOWN_MINE:
            count = count + 1
    else:  # x = 0
        pass
    return count


def count_right(grid, x, y, X, Y):  # check one square to the right
    count = 0
    if x < X - 1:
        if grid[x + 1 + y * X] == UNKNOWN_MINE:
            count = count + 1
    return count


def calculate_neighbours(grid, X, Y):
    for x in range(X):
        for y in range(Y):
            if grid[x + y * X] == UNKNOWN:  # if not a mine
                num_above = count_above(grid, x, y, X, Y)  # check three squares above          
                num_below = count_below(grid, x, y, X, Y)  # check three squares below 
                num_left = count_left(grid, x, y, X, Y)   # check square to the left 
                num_right = count_right(grid, x, y, X, Y)  # check square to the right 
                sum = num_above + num_below + num_left + num_right
                if sum == 0:
                    sum = "."  # DEBUG - replace "0" with "." to allow easy visual checking
                else:
                    #print(x,y, "above:", count_above,"below:", count_below,"L:", count_left,"R:",count_right)   # DEBUG
                    sum = str(sum)      #DEBUG
                grid[x + y * X] = sum     # convert integer to string
    return grid


def check_left(known_grid, unknown_grid, x, y, X, Y):  # check one square to the left
    if x > 0:
        if known_grid[x - 1 + y * X] == UNKNOWN:
            pass
    else:  # x = 0
        pass
    return unknown_grid


def check_right(known_grid, unknown_grid, x, y, X, Y):  # check one square to the right
    if x < X - 2:
        if known_grid[x + 1 + y * X] == UNKNOWN:
            pass
    return unknown_grid


def reveal_neighbours(x, y, X, Y, known_grid, unknown_grid):
    # Recursively examine all eight positions around spot
    # Start with spot one above and work clockwise
    # Skip if value of a position is known,
    # Continue search until encounter a mine or number (of neighbouring mines)

    # Check spot above
    print("Check spot above")  #DEBUG
    if y > 0:
        (unknown_grid, playing_game) = analyze_choice(x, y-1, X, Y, known_grid, unknown_grid)
    
    # Check spot above and one to the right
    print("Check spot above and to the right")  #DEBUG
    if y > 0 and x < X-1:
        (unknown_grid, playing_game) = analyze_choice(x+1, y-1, X, Y, known_grid, unknown_grid)

    # Check spot one to the right
    print("Check spot one to the right")  #DEBUG
    if x < X-1:
        (unknown_grid, playing_game) = analyze_choice(x+1, y, X, Y, known_grid, unknown_grid)
        
    # Check spot one down and one to the right
    print("Check spot below and to the right")  #DEBUG
    if y < Y and x < X:
        (unknown_grid, playing_game) = analyze_choice(x+1, y+1, X, Y, known_grid, unknown_grid)

    # Check spot one down 
    print("Check spot below")  #DEBUG
    if y < Y-1:
        (unknown_grid, playing_game) = analyze_choice(x, y+1, X, Y, known_grid, unknown_grid)
        
    # Check spot one down and one to the left
    print("Check spot below and to the left")  #DEBUG
    if y < Y-1 and x > 0:
        (unknown_grid, playing_game) = analyze_choice(x-1, y+1, X, Y, known_grid, unknown_grid)
        
    # Check spot one to the left
    print("Check spot to the left")  #DEBUG
    if x > 0:
        (unknown_grid, playing_game) = analyze_choice(x-1, y, X, Y, known_grid, unknown_grid)
        
    # Check spot one above and one to the left
    print("Check spot above and to the left")  #DEBUG
    if x > 0 and y > 0:
       (unknown_grid, playing_game) = analyze_choice(x-1, y-1, X, Y, known_grid, unknown_grid)
        
    return (unknown_grid, playing_game)    # update unknown grid values
#    pass
#    return unknown_grid


def analyze_choice(x, y, X, Y, known_grid, unknown_grid):  
    # First check if spot is already known in 'unknown_grid'
    # If it is known, then quit and return (to prevent infinite recursion loops)
    # Else: Copy spot value from 'known_grid' to 'unknown_grid' 
    playing_game = True # set default
    print("DEBUG____ [x + y * X] = ", x + y * X)  # IndexError when index is max plus one
    unknown_spot = unknown_grid[x + y * X]  # check spot selected in 'unknown_grid' 
    print("Spot ({},{}) is '{}'".format(x, y, unknown_spot))   # DEBUG

    if unknown_spot != UNKNOWN:  # spot is known if not unknown
        return (unknown_grid, playing_game)    # return since this value already unmasked
        
#    print("Spot ({},{}) is '{}'".format(x, y, known_grid[x + y * X]))   # DEBUG
    spot = known_grid[x + y * X]  # check spot selected in 'known_grid'   #Duplicate
    if spot == UNKNOWN_MINE:  # game over - lose
        playing_game = False
        print("Game over since selected mine.")    
        unknown_grid[x + y * X] = UNKNOWN_MINE   # update grid
        show_grid(X, Y, unknown_grid)            # show grid with reason for fail
    elif spot == KNOWN_MINE:   # game over - lose
        playing_game = False
        print("Game over since selected mine.")   
        unknown_grid[x + y * X] = KNOWN_MINE   	# update grid
        show_grid(X, Y, unknown_grid)          	# show grid with reason for fail
    elif spot == UNKNOWN:    # reveal value
       unknown_grid[x + y * X] = BLANK   
       (unknown_grid, playing_game) = reveal_neighbours(x, y, X, Y, known_grid, unknown_grid)
    else:  # spot is numeric value
       unknown_grid[x + y * X] = spot
       (unknown_grid, playing_game) = reveal_neighbours(x, y, X, Y, known_grid, unknown_grid)
       
    return (unknown_grid, playing_game)    # update unknown grid values

    

# Initialize grid
unknown_grid = init_grid(X, Y, UNKNOWN)  # Create empty grid of size X by Y
known_grid = init_grid(X, Y, UNKNOWN)    # Create empty grid of size X by Y

show_grid(X, Y, known_grid)

level = get_level()

#known_grid = add_mines(known_grid, level, UNKNOWN_MINE)   # Add mines to empty grid
known_grid = create_grid(known_grid, level, UNKNOWN_MINE)   # Add mines to empty grid
show_grid(X, Y, known_grid)

known_grid = calculate_neighbours(known_grid, X, Y)      # Calculate number of neighbour mines for each non-mine square

show_grid(X, Y, known_grid)

playing_game = True

while playing_game:
    show_grid(X, Y, unknown_grid)  # Show user guesses
    (x,y) = enter_choice(X, Y)
    
    (unknown_grid, playing_game) = analyze_choice(x, y, X, Y, known_grid, unknown_grid)
    (unknown_grid, playing_game) = reveal_neighbours(x, y, X, Y, known_grid, unknown_grid)
