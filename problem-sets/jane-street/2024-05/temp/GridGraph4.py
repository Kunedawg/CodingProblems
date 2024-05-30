import matplotlib.pyplot as plt
import networkx as nx


class GridGraph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.adj_list = {(r, c): [] for r in range(rows) for c in range(cols)}
        self.data = {(r, c): None for r in range(rows) for c in range(cols)}

    def add_edge(self, cell1, cell2):
        if self._are_adjacent(cell1, cell2):
            self.adj_list[cell1].append(cell2)
            self.adj_list[cell2].append(cell1)
        else:
            raise ValueError(f"Cells {cell1} and {cell2} are not adjacent.")

    def remove_edge(self, cell1, cell2):
        self.adj_list[cell1].remove(cell2)
        self.adj_list[cell2].remove(cell1)

    def neighbors(self, cell):
        return self.adj_list[cell]

    def _are_adjacent(self, cell1, cell2):
        r1, c1 = cell1
        r2, c2 = cell2
        return (abs(r1 - r2) == 1 and c1 == c2) or (
            abs(c1 - c2) == 1 and r1 == r2
        )

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

        plt.figure(figsize=(8, 8))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=500,
            node_color="lightblue",
            font_size=10,
            font_color="black",
        )
        plt.show()

    def visualize_regions(self, region_graph):
        pos = nx.spring_layout(region_graph)
        labels = {i: f"Region {i+1}" for i in region_graph.nodes()}

        plt.figure(figsize=(8, 8))
        nx.draw(
            region_graph,
            pos,
            labels=labels,
            with_labels=True,
            node_size=500,
            node_color="lightgreen",
            font_size=10,
            font_color="black",
        )
        plt.show()

    def set_cell_data(self, cell, data):
        if cell in self.data:
            self.data[cell] = data
        else:
            raise ValueError(f"Cell {cell} is out of bounds.")

    def get_cell_data(self, cell):
        if cell in self.data:
            return self.data[cell]
        else:
            raise ValueError(f"Cell {cell} is out of bounds.")


# Example usage
grid_graph = GridGraph(5, 5)

# Region 1
grid_graph.add_edge((0, 0), (1, 0))  # Valid
grid_graph.add_edge((1, 0), (2, 0))  # Valid
grid_graph.add_edge((2, 0), (3, 0))  # Valid
grid_graph.add_edge((3, 0), (4, 0))  # Valid

# Region 2
grid_graph.add_edge((0, 1), (1, 1))  # Valid
grid_graph.add_edge((1, 1), (2, 1))  # Valid
grid_graph.add_edge((2, 1), (3, 1))  # Valid
grid_graph.add_edge((3, 1), (4, 1))  # Valid
grid_graph.add_edge((3, 1), (3, 2))  # Valid
grid_graph.add_edge((4, 1), (4, 2))  # Valid
grid_graph.add_edge((3, 2), (4, 2))  # Valid

# Region 3
grid_graph.add_edge((0, 2), (1, 2))  # Valid
grid_graph.add_edge((1, 2), (2, 2))  # Valid
grid_graph.add_edge((2, 2), (2, 3))  # Valid
grid_graph.add_edge((2, 3), (3, 3))  # Valid
grid_graph.add_edge((3, 3), (4, 3))  # Valid

# Region 4
grid_graph.add_edge((0, 4), (1, 4))  # Valid
grid_graph.add_edge((1, 4), (2, 4))  # Valid
grid_graph.add_edge((2, 4), (3, 4))  # Valid
grid_graph.add_edge((3, 4), (4, 4))  # Valid
grid_graph.add_edge((1, 3), (1, 4))  # Valid

# Set data for some cells
grid_graph.set_cell_data((0, 0), "Start")
grid_graph.set_cell_data((4, 4), "End")
grid_graph.set_cell_data((1, 1), {"terrain": "mountain", "altitude": 3000})

# Get data for a cell
print(grid_graph.get_cell_data((0, 0)))  # Output: Start
print(grid_graph.get_cell_data((4, 4)))  # Output: End
print(
    grid_graph.get_cell_data((1, 1))
)  # Output: {'terrain': 'mountain', 'altitude': 3000}

regions = grid_graph.find_all_regions()
for i, region in enumerate(regions):
    print(f"Region {i+1}: {region}")

# Find and visualize region adjacency graph
region_graph = grid_graph.find_region_adjacency()
grid_graph.visualize_regions(region_graph)

# Visualize the grid
grid_graph.visualize()
