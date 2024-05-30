# Define ANSI escape codes for colors
RESET = "\033[0m"
WHITE_BG = "\033[48;5;15m"
BLACK_BG = "\033[48;5;0m"
BLACK_TEXT = "\033[48;5;0m"


# Define the size of the grid
GRID_SIZE = 10

# Initialize the grid with some default values (e.g., 0-9 or 'X')
grid = [
    [1, 2, 3, 'X', 5, 6, 7, 8, 9, 'X'],
    [4, 5, 'X', 6, 7, 8, 9, 'X', 1, 2],
    [7, 'X', 8, 9, 'X', 0, 1, 2, 3, 4],
    ['X', 0, 1, 2, 3, 4, 5, 6, 7, 8],
    [9, 'X', 0, 1, 2, 3, 4, 5, 6, 7],
    [8, 9, 'X', 0, 1, 2, 3, 4, 5, 6],
    [7, 8, 9, 'X', 0, 1, 2, 3, 4, 5],
    [6, 7, 8, 9, 'X', 0, 1, 2, 3, 4],
    [5, 6, 7, 8, 9, 'X', 0, 1, 2, 3],
    ['X', 5, 6, 7, 8, 9, 'X', 0, 1, 2]
]

# Initialize the regions
regions = [['B'] * GRID_SIZE for _ in range(GRID_SIZE)]

# Define region A in the top left 2x2 square
for i in range(2):
    for j in range(2):
        regions[i][j] = 'A'

# Function to print the grid with regions
def print_grid_with_regions(grid, regions):
    for row, region_row in zip(grid, regions):
        for cell, region in zip(row, region_row):
            if cell == 'X':
                print(f"{BLACK_BG}{BLACK_TEXT} {cell} {RESET}", end=' ')
            else:
                if region == 'A':
                    print(f"{WHITE_BG} {cell} {RESET}", end=' ')
                else:
                    print(f"{WHITE_BG} {cell} {RESET}", end=' ')
        print()  # Newline after each row

# Print the grid with regions
print_grid_with_regions(grid, regions)
