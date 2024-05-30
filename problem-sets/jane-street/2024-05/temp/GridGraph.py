import matplotlib.pyplot as plt
import networkx as nx


class GridGraph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.adj_list = {(r, c): [] for r in range(rows) for c in range(cols)}

    def add_edge(self, cell1, cell2):
        self.adj_list[cell1].append(cell2)
        self.adj_list[cell2].append(cell1)

    def remove_edge(self, cell1, cell2):
        self.adj_list[cell1].remove(cell2)
        self.adj_list[cell2].remove(cell1)

    def neighbors(self, cell):
        return self.adj_list[cell]

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
        # plt.gca().invert_yaxis()
        plt.show()


# Example usage
grid_graph = GridGraph(4, 4)
grid_graph.add_edge((0, 0), (0, 1))
grid_graph.add_edge((0, 1), (0, 2))
grid_graph.add_edge((1, 1), (1, 2))
grid_graph.add_edge((2, 2), (2, 3))
grid_graph.add_edge((3, 3), (3, 2))
grid_graph.add_edge((0, 0), (1, 0))
grid_graph.add_edge((0, 0), (3, 3))

regions = grid_graph.find_all_regions()
for i, region in enumerate(regions):
    print(f"Region {i+1}: {region}")

grid_graph.visualize()
