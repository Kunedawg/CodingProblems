from grid_graph import GridGraph

# Using a filename
graph = GridGraph(filename="graph5x5.txt")

# get subset

sub_graph = graph.create_subset((1, 0), 1, 5)

# Visualize the grid
graph.visualize()
sub_graph.visualize()


# Find and visualize region adjacency graph
region_graph = graph.find_region_adjacency()
graph.visualize_regions(region_graph)

print(sub_graph.adj_list)
