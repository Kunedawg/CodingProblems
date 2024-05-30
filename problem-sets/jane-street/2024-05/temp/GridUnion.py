from collections import defaultdict


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def are_adjacent(x1, y1, x2, y2):
    return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)


def link_elements(graph, uf, x1, y1, x2, y2, width):
    index1 = y1 * width + x1
    index2 = y2 * width + x2
    if are_adjacent(x1, y1, x2, y2):
        graph[index1].append(index2)
        graph[index2].append(index1)
        uf.union(index1, index2)


def track_region_adjacency(uf, region_adjacency, x1, y1, x2, y2, width):
    index1 = y1 * width + x1
    index2 = y2 * width + x2
    region1 = uf.find(index1)
    region2 = uf.find(index2)
    if region1 != region2:
        region_adjacency.add((min(region1, region2), max(region1, region2)))


def validate_grid(grid, uf, width, height):
    region_properties = defaultdict(set)
    for y in range(height):
        for x in range(width):
            index = y * width + x
            region = uf.find(index)
            region_properties[region].add(grid[y][x])

    for properties in region_properties.values():
        if len(properties) > 1:
            return False

    return True


# Example usage
width, height = 5, 5  # Example grid size
total_number_of_elements = width * height

# Initialize grid
grid = [[None for _ in range(width)] for _ in range(height)]
# Example: Filling the grid with some properties
properties = [
    [1, 1, 2, 2, 2],
    [1, 1, 2, 3, 3],
    [4, 4, 4, 3, 3],
    [4, 5, 5, 3, 6],
    [5, 5, 5, 6, 6],
]

for y in range(height):
    for x in range(width):
        grid[y][x] = properties[y][x]

# Initialize graph and Union-Find
graph = defaultdict(list)
uf = UnionFind(total_number_of_elements)
region_adjacency = set()

# Link elements (example links, these can be modified as needed)
link_elements(graph, uf, 0, 0, 1, 0, width)
link_elements(graph, uf, 0, 0, 0, 1, width)
link_elements(graph, uf, 2, 2, 2, 3, width)
link_elements(graph, uf, 4, 4, 3, 4, width)

# Validate the grid based on current links
is_valid = validate_grid(grid, uf, width, height)

# Displaying results
print("Grid:")
for row in grid:
    print(row)

print("\nGraph Adjacency List:")
for node, neighbors in graph.items():
    print(f"{node}: {neighbors}")

print("\nRegion Adjacency:")
for region_pair in region_adjacency:
    print(region_pair)

print(f"\nIs the grid valid based on current links? {is_valid}")
