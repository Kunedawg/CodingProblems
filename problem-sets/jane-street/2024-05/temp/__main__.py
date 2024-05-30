# TODO print board, color backgrounds different colors. At most we need
# 5 different colors

# TODO need to write checkers for each row.
#   TODO function that does in a row and gives an array of numbers to
#   check

# TODO need to write a checker to ensure that the region rules are
# adhered to
#   TODO each number in a region must be the same

# TODO need a way to input the starting region and encode the idea of a
# region
#   TODO need a way to recognize when a region has been split

# TODO formalize the strategy of solving row by row and combining
# solutions

# TODO need to enforce the sparse rule

# TODO function for sums up the numbers


# Define ANSI escape codes for colors
RESET = "\033[0m"
WHITE_BG = "\033[48;5;15m"
BLACK_BG = "\033[48;5;0m"
BLACK_TEXT = "\033[48;5;0m"


def print_grid_with_colors(grid):
    for row in grid:
        for cell in row:
            if cell == 'X':
                print(f"{BLACK_BG}{BLACK_TEXT} {cell} {RESET}", end='')
            else:
                print(f"{WHITE_BG} {cell} {RESET}", end='')
        print()  # Newline after each row


# Example data
data = [
    [1, 2, 3, 'X'],
    [4, 5, 'X', 6],
    [7, 'X', 8, 9],
    ['X', 0, 1, 2]
]

# Print the grid with colors
print_grid_with_colors(data)

