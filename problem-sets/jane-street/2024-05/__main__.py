from grid_graph import GridGraph
import math
import copy
import networkx as nx
import os
from functools import lru_cache
import threading
import concurrent.futures


def generate_masks(n):
    def helper(current_string, length):
        if length == n:
            yield current_string
        else:
            if not current_string or current_string[-1] == "0":
                yield from helper(current_string + "1", length + 1)
            yield from helper(current_string + "0", length + 1)

    return helper("", 0)


def get_all_colorings(graph: nx.Graph, m, initial_colors=None):
    def is_valid(graph: nx.Graph, color, node, c):
        for neighbor in graph.neighbors(node):
            if color[neighbor] == c:
                return False
        return True

    def graph_coloring(graph: nx.Graph, m, color, node):
        if node == len(graph):
            yield color.copy()
            return

        nodes = list(graph.nodes())
        current_node = nodes[node]

        if color[current_node] is not None:
            yield from graph_coloring(graph, m, color, node + 1)
            return

        for c in range(m):
            if is_valid(graph, color, current_node, c):
                color[current_node] = c
                yield from graph_coloring(graph, m, color, node + 1)
                color[current_node] = None

    # Initialize the color dictionary with initial colors if provided
    color = {node: None for node in graph.nodes()}
    if initial_colors:
        color.update(initial_colors)

    return graph_coloring(graph, m, color, 0)


def is_square(n):
    if n < 0:
        return False
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n


@lru_cache(None)
def is_palindrome(num):
    s = str(num)
    return s == s[::-1]


def is_one_more_than_palindrome(num):
    return is_palindrome(num - 1)


def get_row_array(row_graph: GridGraph, row_length):
    array = []
    for c in range(row_length):
        array.append(row_graph.get_cell_data((0, c)))
    return array


def get_row_numbers(row_array):
    result = []
    current_number = ""

    for num in row_array:
        if num == 10:
            if current_number:
                result.append(int(current_number))
                current_number = ""
        else:
            current_number += str(num)

    if current_number:  # Append the last number if exists
        result.append(int(current_number))

    return result


def all_numbers_pass_checker(array, checker):
    for num in array:
        if checker(num) is False:
            return False
    return True


file_lock = threading.Lock()


class CompletedCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1
            print(f"Completed masks: {self.count}")


def process_mask(
    file_name,
    mask,
    row_graph,
    row_rule_checker,
    row_length,
    counter,
):
    masked_graph = copy.deepcopy(row_graph)
    masked_graph.apply_mask([mask])
    region_graph = masked_graph.find_region_adjacency()
    initial_colors = masked_graph.get_region_coloring(region_graph)
    colors_iter = get_all_colorings(
        region_graph, 10, initial_colors=initial_colors
    )

    valid_rows = []
    for color in colors_iter:
        color_graph = copy.deepcopy(masked_graph)
        for node, value in color.items():
            color_graph.set_region_data(
                region_graph.nodes[node]["cells"], value
            )
        row_array = get_row_array(color_graph, row_length)
        row_numbers = get_row_numbers(row_array)
        if all_numbers_pass_checker(row_numbers, row_rule_checker):
            valid_rows.append(row_array)

    with file_lock:
        with open(file_name, "a") as file:
            for row_array in valid_rows:
                file.write(f"{row_array}\n")

    counter.increment()


def solve_row(file_name, row_graph: GridGraph, row_rule_checker, row_length):
    masks = list(generate_masks(row_length))
    counter = CompletedCounter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        futures = [
            executor.submit(
                process_mask,
                file_name,
                mask,
                row_graph,
                row_rule_checker,
                row_length,
                counter,
            )
            for mask in masks
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

    print("Processed masks")


# def solve_row(file_name, row_graph: GridGraph, row_rule_checker, row_length):
#     masks_completed = 0
#     for mask in generate_masks(row_length):
#         masked_graph = copy.deepcopy(row_graph)
#         masked_graph.apply_mask([mask])  # mask is array of rows
#         region_graph = masked_graph.find_region_adjacency()
#         initial_colors = masked_graph.get_region_coloring(region_graph)
#         colors_iter = get_all_colorings(
#             region_graph, 10, initial_colors=initial_colors
#         )
#         for color in colors_iter:
#             color_graph = copy.deepcopy(masked_graph)
#             for node, value in color.items():
#                 color_graph.set_region_data(
#                     region_graph.nodes[node]["cells"], value
#                 )
#             row_array = get_row_array(color_graph, row_length)
#             row_numbers = get_row_numbers(row_array)
#             if all_numbers_pass_checker(row_numbers, row_rule_checker):
#                 with open(file_name, "a") as file:
#                     file.write(f"{row_array}\n")
#         masks_completed = masks_completed + 1
#         print(masks_completed)


# load base graph
grid_graph = GridGraph(filename="graph11.txt")

# row rule checkers
row_rule_checkers = [is_square, is_one_more_than_palindrome]

# solve rows
for r in range(1):
    os.makedirs("solution", exist_ok=True)
    file_name = f"solution/row_again{r}.txt"
    with open(file_name, "w") as file:
        file.write("")  # clear file

    row_graph = grid_graph.create_subset((r, 0), 1, 11)
    rule_checker = row_rule_checkers[r]
    solve_row(file_name, row_graph, rule_checker, 11)

# Apply mask
# mask = ["00000", "00001", "00000", "00000", "00000"]
# grid_graph.apply_mask(mask)

# Assign some values
# grid_graph.set_cell_data((0, 0), 1)
# grid_graph.set_cell_data((1, 0), 1)
# grid_graph.set_cell_data((2, 0), 1)
# grid_graph.set_cell_data((3, 0), 1)
# grid_graph.set_cell_data((4, 0), 1)

# Visualize the graph
# grid_graph.visualize()


# # get subset
# sub_graph = grid_graph.create_subset((0, 0), 1, 11)

# # Visualize the grid
# sub_graph.visualize()


# # Find and visualize region adjacency grid_graph
# region_graph = grid_graph.find_region_adjacency()
# grid_graph.visualize_regions(region_graph)
