#!/usr/bin/env python3

# Simple MineSweeper program
# Initially configure all spots in 'game_grid' as "." aka unknown.
# Randomly position the mines and then calculate all neighbour counts in 'known_grid'.
# Copy user guess (x,y) value from 'known_grid' into 'game_grid'.

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
    print_top_x_value(X)   # move X-axis label to top of grid
    print_bottom_x_value(X)


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
    print("Enter 'm' or 'M' in front of x to guess at mine position")
    valid_x = False
    mine_guess = False  # Add ability to guess at mine locations
    while not valid_x:
        x = input("Enter x value choice: ")
        if x == "":
            continue
        if x[0] == "m" or x[0] == "M":
            mine_guess = True
            if "m" in x:
                x = x.replace("m","")  # Remove "m" from value
            if "M" in x:
                x = x.replace("M","")  # Remove "M" from value
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
    return (x,y,mine_guess)


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


def check_left(known_grid, game_grid, x, y, X, Y):  # check one square to the left
    if x > 0:
        if known_grid[x - 1 + y * X] == UNKNOWN:
            pass
    else:  # x = 0
        pass
    return game_grid


def check_right(known_grid, game_grid, x, y, X, Y):  # check one square to the right
    if x < X - 2:
        if known_grid[x + 1 + y * X] == UNKNOWN:
            pass
    return game_grid


def reveal_neighbours(x, y, is_mine, X, Y, known_grid, game_grid):
    # Recursively examine all eight positions around spot
    # Start with spot one above and work clockwise
    # Skip if value of a position is known,
    # Continue search until encounter a mine or number (of neighbouring mines)
    is_neighbour = True

    # Check spot above
    if y > 0:
        (game_grid, playing_game) = analyze_choice(x, y-1, is_mine, X, Y, known_grid, game_grid, is_neighbour)
    
    # Check spot above and one to the right
    if y > 0 and x < X-1:
        (game_grid, playing_game) = analyze_choice(x+1, y-1, is_mine, X, Y, known_grid, game_grid, is_neighbour)

    # Check spot one to the right
    if x < X-1:
        (game_grid, playing_game) = analyze_choice(x+1, y, is_mine, X, Y, known_grid, game_grid, is_neighbour)
        
    # Check spot one down and one to the right
    if y < Y-1 and x < X-1:
        (game_grid, playing_game) = analyze_choice(x+1, y+1, is_mine, X, Y, known_grid, game_grid, is_neighbour)

    # Check spot one down 
    if y < Y-2:
        (game_grid, playing_game) = analyze_choice(x, y+1, is_mine, X, Y, known_grid, game_grid, is_neighbour)
        
    # Check spot one down and one to the left
    if y < Y-2 and x > 0:
        (game_grid, playing_game) = analyze_choice(x-1, y+1, is_mine, X, Y, known_grid, game_grid, is_neighbour)
        
    # Check spot one to the left
    if x > 0:
        (game_grid, playing_game) = analyze_choice(x-1, y, is_mine, X, Y, known_grid, game_grid, is_neighbour)
        
    # Check spot one above and one to the left
    if x > 0 and y > 0:
       (game_grid, playing_game) = analyze_choice(x-1, y-1, is_mine, X, Y, known_grid, game_grid, is_neighbour)
        
    return (game_grid, playing_game)    # update unknown grid values
#    pass
#    return game_grid

def analyze_choice(x, y, is_mine, X, Y, known_grid, game_grid, is_neighbour):  
    # First check if spot is already known in 'game_grid'
    # If it is known, then quit and return (to prevent infinite recursion loops)
    # If it is a mine, then quit and return
    # Else: Copy spot value from 'known_grid' to 'game_grid' 
    # Use "is_neighbour" parameter to prevent game ending if neighbour is a known or unknown mine
    playing_game = True # set default
    unknown_spot = game_grid[x + y * X]  # check spot selected in 'game_grid' 
    known_spot = known_grid[x + y * X]  # check spot selected in 'known_grid' 
    print("Game grid spot ({},{}) is '{}'".format(x, y, unknown_spot), end = "")   # DEBUG
    print(" Known grid spot is '{}'".format(known_spot))   # DEBUG

    if is_neighbour:
        is_mine = False  # Always False if checking neighbouring values
                         # Only True if the is the user's attempt at selecting a mine
        pass  # Add code to examine values surrounded location entered by user
    else:  # Case where handling user entered location
        pass  # Add code to examine value of user entered location


    if is_mine:
        if (known_spot == UNKNOWN_MINE) or (known_spot == KNOWN_MINE):
#            is_mine = False  # Update value for neighbour recursion
            playing_game = True
            game_grid[x + y * X] = KNOWN_MINE   # update grid
            show_grid(X, Y, game_grid)            # show updated grid
            return (game_grid, playing_game)    # return updated grid
        else:  # Fail since did not correctly select a mine
            print("DEBUG, known_spot = ", known_spot)  #DEBUG
#            is_mine = False  # Update value for neighbour recursion
            playing_game = False
            print("\033[1m\033[6mGame over! Did not select desired mine at spot({},{}).\033[0m".format(x,y))    
            game_grid[x + y * X] = known_spot   # update grid
            show_grid(X, Y, game_grid)            # show grid with reason for fail
            return (game_grid, playing_game)    # return updated grid

    if unknown_spot != UNKNOWN:  # spot is known if not unknown
        if unknown_spot == KNOWN_MINE:
            if not is_mine:
                playing_game = False  # Lose game since deliberately selected known mine value
                print("\033[1m\033[6mGame over since selected known mine at spot({},{}).\033[0m".format(x,y))    
            else:
                game_grid[x + y * X] = KNOWN_MINE   	# update grid
                
        return (game_grid, playing_game)    # return since this value already unmasked
        
#    print("Spot ({},{}) is '{}'".format(x, y, known_grid[x + y * X]))   # DEBUG
    else: # Spot is unknown
        spot = known_grid[x + y * X]  # check spot selected in 'known_grid'   #Duplicate
        if spot == UNKNOWN_MINE:  # show it as known mine but continue playing
            playing_game = False
            print("\033[1m\033[6mGame over since selected unknown mine at spot({},{}).\033[0m".format(x,y))    
            game_grid[x + y * X] = UNKNOWN_MINE   # update grid
            show_grid(X, Y, game_grid)            # show grid with reason for fail
            return (game_grid, playing_game)    # return since this value already unmasked
        elif spot == KNOWN_MINE:   # game over - lose
            playing_game = False
            print("\033[1m\033[6mGame over since selected mine at spot({},{}).\033[0m".format(x,y))    
            game_grid[x + y * X] = KNOWN_MINE   	# update grid
            show_grid(X, Y, game_grid)          	# show grid with reason for fail
            return (game_grid, playing_game)    # return since this value already unmasked
        elif spot == UNKNOWN:    # reveal value
            game_grid[x + y * X] = BLANK   
            (game_grid, playing_game) = reveal_neighbours(x, y, False, X, Y, known_grid, game_grid)
            return (game_grid, playing_game)    # return since this value already unmasked
        else:  # spot is numeric value
            game_grid[x + y * X] = spot
    #       (game_grid, playing_game) = reveal_neighbours(x, y, X, Y, known_grid, game_grid)
            return (game_grid, playing_game)    # return since this value already unmasked
       

# Initialize grid
game_grid = init_grid(X, Y, UNKNOWN)  # Create empty grid of size X by Y
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
    show_grid(X, Y, game_grid)  # Show user guesses
    (x, y, is_mine) = enter_choice(X, Y)
    
    (game_grid, playing_game) = analyze_choice(x, y, is_mine, X, Y, known_grid, game_grid, False)
    if playing_game:
        (game_grid, playing_game) = reveal_neighbours(x, y, False, X, Y, known_grid, game_grid)
