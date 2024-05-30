from grid_graph import GridGraph


# Usage example
grid_graph = GridGraph(filename="graph5x5.txt")


# Apply mask
mask = ["00000", "00001", "00000", "00000", "00000"]
grid_graph.apply_mask(mask)

# Visualize the graph
grid_graph.visualize()


# get subset
sub_graph = grid_graph.create_subset((1, 0), 1, 5)

# Visualize the grid
sub_graph.visualize()


# Find and visualize region adjacency grid_graph
region_graph = grid_graph.find_region_adjacency()
grid_graph.visualize_regions(region_graph)
