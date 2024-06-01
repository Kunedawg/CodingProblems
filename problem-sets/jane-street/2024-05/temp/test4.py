import matplotlib.pyplot as plt
import networkx as nx


class GridGraph:
    def __init__(self, rows=None, cols=None, filename=None):
        if filename:
            self._initialize_from_file(filename)
        elif rows is not None and cols is not None:
            self.rows = rows
            self.cols = cols
            self.adj_list = {
                (r, c): [] for r in range(rows) for c in range(cols)
            }
            self.data = {
                (r, c): None for r in range(rows) for c in range(cols)
            }
        else:
            raise ValueError(
                "Either rows and cols or filename must be provided."
            )

    def _initialize_from_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        self.rows = len(lines) // 2 + 1
        self.cols = len(lines[0].strip()) // 2 + 1

        self.adj_list = {
            (r, c): [] for r in range(self.rows) for c in range(self.cols)
        }
        self.data = {
            (r, c): None for r in range(self.rows) for c in range(self.cols)
        }

        for r in range(0, self.rows * 2 - 1, 2):
            for c in range(self.cols - 1):
                if lines[r][2 * c + 1] == "-":
                    self.add_edge((r // 2, c), (r // 2, c + 1))

        for r in range(1, self.rows * 2 - 1, 2):
            for c in range(self.cols):
                if lines[r][2 * c] == "|":
                    self.add_edge((r // 2, c), (r // 2 + 1, c))

    def add_edge(self, cell1, cell2):
        if not self._are_adjacent(cell1, cell2):
            raise ValueError(f"Cells {cell1} and {cell2} are not adjacent.")

        self.adj_list[cell1].append(cell2)
        self.adj_list[cell2].append(cell1)

    def remove_edge(self, cell1, cell2):
        self.adj_list[cell1].remove(cell2)
        self.adj_list[cell2].remove(cell1)

    def neighbors(self, cell):
        return self.adj_list[cell]

    def _are_adjacent(self, cell1, cell2):
        r1, c1 = cell1
        r2, c2 = cell2
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def find_all_regions(self):
        visited = set()
        regions = []

        def dfs(cell):
            stack = [cell]
            region = []
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    region.append(current)
                    for neighbor in self.neighbors(current):
                        if neighbor not in visited:
                            stack.append(neighbor)
            return region

        for cell in self.adj_list:
            if cell not in visited:
                region = dfs(cell)
                regions.append(region)

        return regions

    def are_regions_adjacent(self, region1, region2):
        for cell1 in region1:
            for cell2 in region2:
                if self._are_adjacent(cell1, cell2):
                    return True
        return False

    def find_region_adjacency(self):
        regions = self.find_all_regions()
        region_graph = nx.Graph()

        for i, region in enumerate(regions):
            region_graph.add_node(i, cells=region)
            for j in range(i):
                if self.are_regions_adjacent(regions[i], regions[j]):
                    region_graph.add_edge(i, j)

        return region_graph

    def visualize(self):
        G = nx.Graph()
        for cell in self.adj_list:
            G.add_node(cell)
            for neighbor in self.adj_list[cell]:
                G.add_edge(cell, neighbor)

        pos = {
            (r, c): (c, -r) for r in range(self.rows) for c in range(self.cols)
        }

        # Create labels for nodes based on their data
        labels = {cell: self.get_cell_data(cell) for cell in G.nodes}

        # Create a list of colors based on the data
        node_color = [
            "black" if self.get_cell_data(cell) == 10 else "lightblue"
            for cell in G.nodes
        ]

        plt.figure(figsize=(8, 8))
        nx.draw(
            G,
            pos,
            labels=labels,
            with_labels=True,
            node_size=500,
            node_color=node_color,
            font_size=10,
            font_color="white" if self.get_cell_data(cell) == 10 else "black",
        )
        plt.show()

    def set_cell_data(self, cell, data):
        try:
            if data is None or (isinstance(data, int) and 0 <= data <= 10):
                self.data[cell] = data
            else:
                raise ValueError(
                    f"Data {data} is not a valid value. Must be None or an integer between 0 and 10."
                )
        except KeyError:
            raise ValueError(f"Cell {cell} is out of bounds.")

    def get_cell_data(self, cell):
        try:
            return self.data[cell]
        except KeyError:
            raise ValueError(f"Cell {cell} is out of bounds.")

    def create_subset(self, start_cell, subset_rows, subset_cols):
        sr, sc = start_cell
        subset = GridGraph(rows=subset_rows, cols=subset_cols)

        for r in range(subset_rows):
            for c in range(subset_cols):
                orig_cell = (sr + r, sc + c)
                subset_cell = (r, c)
                subset.set_cell_data(
                    subset_cell, self.get_cell_data(orig_cell)
                )
                if r > 0 and (sr + r - 1, sc + c) in self.adj_list[orig_cell]:
                    subset.add_edge(subset_cell, (r - 1, c))
                if c > 0 and (sr + r, sc + c - 1) in self.adj_list[orig_cell]:
                    subset.add_edge(subset_cell, (r, c - 1))
                if (
                    r < subset_rows - 1
                    and (sr + r + 1, sc + c) in self.adj_list[orig_cell]
                ):
                    subset.add_edge(subset_cell, (r + 1, c))
                if (
                    c < subset_cols - 1
                    and (sr + r, sc + c + 1) in self.adj_list[orig_cell]
                ):
                    subset.add_edge(subset_cell, (r, c + 1))

        return subset

    def apply_mask(self, mask):
        for r, row_mask in enumerate(mask):
            for c, char in enumerate(row_mask):
                if char == "1":
                    cell = (r, c)
                    self.set_cell_data(cell, 10)
                    # Remove all edges for this cell
                    for neighbor in self.neighbors(cell).copy():
                        self.remove_edge(cell, neighbor)


# Usage example
grid_graph = GridGraph(filename="graph5x5.txt")


# Apply mask
mask = ["00000", "00001", "00000", "00000", "00000"]
grid_graph.apply_mask(mask)

# Visualize the graph
grid_graph.visualize()
