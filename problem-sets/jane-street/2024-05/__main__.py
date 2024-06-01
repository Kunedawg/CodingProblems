from grid_graph import GridGraph
import math
import copy
import networkx as nx
import os
from functools import lru_cache
import multiprocessing
from multiprocessing import Manager, Pool
import time
from prime_to_prime.prime_power_checker import PrimePowerChecker


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

    color = {node: None for node in graph.nodes()}
    if initial_colors:
        color.update(initial_colors)

    return graph_coloring(graph, m, color, 0)


@lru_cache(None)
def is_square(n):
    if n < 0:
        return False
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n


# @lru_cache(None)
def is_palindrome(num):
    s = str(num)
    return s == s[::-1]


@lru_cache(None)
def is_prime(num):
    """Helper function to check if a number is prime."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


@lru_cache(None)
def is_prime_raised_to_prime_power(num):
    """Check if a number is a prime raised to a prime power."""
    for base in range(2, int(math.sqrt(num)) + 1):
        if is_prime(base):
            power = 1
            while True:
                num_to_check = base**power
                if is_prime(power):
                    if num_to_check == num:
                        return True
                if num_to_check > num:
                    break
                power += 1
    return False


prime_power_checker = PrimePowerChecker()


def is_prime_raised_to_prime_power2(num):
    """Check if a number is a prime raised to a prime power."""
    return prime_power_checker.is_prime_power(num)


@lru_cache(None)
def is_digits_sum_to_7(num):
    """Check if the sum of the digits of a number is 7."""
    return sum(int(digit) for digit in str(num)) == 7


@lru_cache(None)
def is_fibonacci(num):
    """Check if a number is a Fibonacci number."""

    def is_perfect_square(x):
        s = int(math.sqrt(x))
        return s * s == x

    return is_perfect_square(5 * num * num + 4) or is_perfect_square(
        5 * num * num - 4
    )


@lru_cache(None)
def is_multiple_of_37(num):
    """Check if a number is a multiple of 37."""
    return num % 37 == 0


@lru_cache(None)
def is_palindrome_and_multiple_of_23(num):
    """Check if a number is a palindrome and a multiple of 23."""
    return is_palindrome(num) and (num % 23 == 0)


@lru_cache(None)
def is_product_of_digits_end_in_1(num):
    """Check if the product of the digits of a number ends in 1."""
    product = 1
    for digit in str(num):
        product *= int(digit)
    return str(product).endswith("1")


@lru_cache(None)
def is_multiple_of_88(num):
    """Check if a number is a multiple of 88."""
    return num % 88 == 0


# @lru_cache(None)
def is_one_less_than_palindrome(num):
    """Check if a number is one less than a palindrome."""
    return is_palindrome(num + 1)


# @lru_cache(None)
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


class CompletedCounter:
    def __init__(self, manager):
        self.count = manager.Value("i", 0)
        self.lock = manager.Lock()

    def increment(self):
        with self.lock:
            self.count.value += 1


def process_mask(args):
    start_time = time.time()
    file_name, mask, row_graph, row_rule_checker, row_length, counter = args
    masked_graph: GridGraph = copy.deepcopy(row_graph)
    masked_graph.apply_mask([mask])
    region_graph = masked_graph.find_region_adjacency()
    initial_colors = masked_graph.get_region_coloring(region_graph)
    colors_iter = get_all_colorings(
        region_graph, 10, initial_colors=initial_colors
    )

    valid_rows = []
    deepcopy_time = 0
    # color_end = time.time()
    # color_sum = 0
    # num_check_sum = 0
    for colors_done, color in enumerate(colors_iter):
        # color_start = time.time()
        # color_sum += color_start - color_end
        # print(
        #     f"#{colors_done}\tcolor t: {color_sum}\t"
        #     f"num_check t: {num_check_sum}",
        #     end="\r",
        # )
        deep_copy_start = time.time()
        color_graph = masked_graph.custom_copy()
        deep_copy_end = time.time()
        deepcopy_time += deep_copy_end - deep_copy_start
        for node, value in color.items():
            color_graph.set_region_data(
                region_graph.nodes[node]["cells"], value
            )
        row_array = get_row_array(color_graph, row_length)
        row_numbers = get_row_numbers(row_array)
        # num_check_start = time.time()
        if all_numbers_pass_checker(row_numbers, row_rule_checker):
            valid_rows.append(row_array)
        # color_end = time.time()
        # num_check_sum += color_end - num_check_start

    with counter.lock:
        with open(file_name, "a") as file:
            for row_array in valid_rows:
                file.write(f"{row_array}\n")

    counter.increment()
    end_time = time.time()

    print(
        (
            f"Completed masks: {counter.count.value}\t"
            f"mask: {mask}\tnum_of_colors: {colors_done+1}\t"
            f"Time: {end_time-start_time} s \t"
            f"DeepT {deepcopy_time} s "
        )
    )


def solve_row_single_core(
    file_name, row_graph, row_rule_checker, row_length, num_processes=None
):
    # masks = list(generate_masks(row_length))
    masks = ["00000100100"]
    # masks = ["00000000000"]
    with Manager() as manager:
        counter = CompletedCounter(manager)
        for mask in masks:
            args = (
                file_name,
                mask,
                row_graph,
                row_rule_checker,
                row_length,
                counter,
            )
            process_mask(args)

    print(f"Processed {len(masks)} masks")


def solve_row(
    file_name, row_graph, row_rule_checker, row_length, num_processes=None
):
    masks = list(generate_masks(row_length))
    with Manager() as manager:
        counter = CompletedCounter(manager)

        if num_processes is None:
            num_processes = multiprocessing.cpu_count()

        with Pool(processes=num_processes) as pool:
            args = [
                (
                    file_name,
                    mask,
                    row_graph,
                    row_rule_checker,
                    row_length,
                    counter,
                )
                for mask in masks
            ]
            pool.map(process_mask, args)

    print(f"Processed {len(masks)} masks")


def are_blacks_sparse(array_of_rows):
    # expects array of length two. objects in a array are equal length arrays.
    # Initialize a set to keep track of positions where the value is found
    positions = set()
    for row in array_of_rows:
        for idx, element in enumerate(row):
            if element == 10:  # 10 represents black
                if idx in positions:
                    return False  # Value found in the same position
                positions.add(idx)
    return True


def read_file_generator(file_path):
    """Reads a file line by line and yields each line as a list of integers."""
    with open(file_path, "r") as file:
        for line in file:
            yield list(map(int, line.strip().split(",")))


def generate_combinations(file1_path, file2_path):
    """Generates all combinations of selecting one row from each file in
    a streaming manner.
    """
    file1_gen = read_file_generator(file1_path)
    file2_gen = list(
        read_file_generator(file2_path)
    )  # Convert the second file to a list to iterate multiple times

    for row1 in file1_gen:
        for row2 in file2_gen:
            yield (row1, row2)


if __name__ == "__main__":
    # Parameters
    solve_rows = True
    solve_row_range = range(2, 3)  # max 11
    combine_rows = False
    combine_row_range = range(0)  # max 10
    use_multi_core = True

    # load base graph
    grid_graph = GridGraph(filename="graph11.txt")

    # row rule checkers
    row_rule_checkers = [
        is_square,
        is_one_more_than_palindrome,
        is_prime_raised_to_prime_power2,
        is_digits_sum_to_7,
        is_fibonacci,
        is_square,
        is_multiple_of_37,
        is_palindrome_and_multiple_of_23,
        is_product_of_digits_end_in_1,
        is_multiple_of_88,
        is_one_less_than_palindrome,
    ]

    # solve rows
    if solve_rows:
        for r in solve_row_range:
            os.makedirs("solution", exist_ok=True)
            file_name = f"solution/row_new{r}.txt"
            with open(file_name, "w") as file:
                file.write("")  # clear file

            row_graph = grid_graph.create_subset((r, 0), 1, 11)
            rule_checker = row_rule_checkers[r]
            if use_multi_core:
                solve_row(file_name, row_graph, rule_checker, 11)
            else:
                solve_row_single_core(file_name, row_graph, rule_checker, 11)

            print(f"Row {r}: complete")

    # combine rows
    if combine_rows:
        for r in combine_row_range:
            os.makedirs("solution", exist_ok=True)
            file_name = f"solution/combine{r+1}.txt"
            with open(file_name, "w") as file:
                file.write("")  # clear file
            if r == 0:
                file_top = f"solution/row{r}.txt"
                file_bottom = f"solution/row{r+1}.txt"
            else:
                file_top = f"solution/combine{r}.txt"
                file_bottom = f"solution/row{r+1}.txt"
            combinations = generate_combinations(file_top, file_bottom)
            sub_graph: GridGraph = grid_graph.create_subset((0, 0), r + 1, 11)
            # Print combinations
            for combo in combinations:
                top, bot = combo
                if r == 0:
                    potential_solution = [top, bot]
                else:
                    potential_solution = top.append(bot)
                if not are_blacks_sparse(potential_solution[-2:]):
                    continue
                test_graph = copy.deepcopy(sub_graph)
                for r, row in enumerate(potential_solution):
                    for c, data in enumerate(row):
                        test_graph.set_cell_data((r, c), data)

                if test_graph.region_data_is_okay:
                    with open(file_name, "a") as file:
                        file.write(f"{potential_solution}\n")

                print(combo)
