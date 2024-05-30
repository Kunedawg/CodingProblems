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
