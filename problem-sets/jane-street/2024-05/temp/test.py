# Define ANSI escape codes for colors
RESET = "\033[0m"
BLACK_BG = "\033[48;5;0m"
RED_BG = "\033[48;5;1m"
GREEN_BG = "\033[48;5;2m"
YELLOW_BG = "\033[48;5;3m"
BLUE_BG = "\033[48;5;4m"
MAGENTA_BG = "\033[48;5;5m"
CYAN_BG = "\033[48;5;6m"
WHITE_BG = "\033[48;5;7m"


# Create a function to print colored text
def print_colored(text, bg_color):
    print(f"{bg_color}{text}{RESET}")


# Example data
data = [
    [1, 'Alice', 25],
    [2, 'Bob', 30],
    [3, 'Charlie', 22]
]

# Define a color scheme for the table cells
color_scheme = [
    [RED_BG, GREEN_BG, BLUE_BG],
    [CYAN_BG, MAGENTA_BG, YELLOW_BG],
    [WHITE_BG, BLACK_BG, RED_BG]
]

# Print the table with colored backgrounds
for row, colors in zip(data, color_scheme):
    for cell, color in zip(row, colors):
        print_colored(f" {cell} ", color)
    print()  # Newline after each row


print("Hello")