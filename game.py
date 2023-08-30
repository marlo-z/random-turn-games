import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def create_random_graph():
    # Number of nodes in the graph
    n = 10
    # Desired probability of an edge between any two nodes for connectivity
    p = 0.1
    # Create an initially empty graph
    connected_graph = nx.Graph()
    # Add nodes
    connected_graph.add_nodes_from(range(n))
    # Start connecting nodes to form a connected graph
    for node in range(1, n):
        target_node = node - 1
        connected_graph.add_edge(node, target_node)
        # Add additional edges with probability p
        for potential_target in range(target_node - 1, -1, -1):
            if potential_target != node and potential_target not in connected_graph.neighbors(node):
                if np.random.rand() < p:
                    connected_graph.add_edge(node, potential_target)
    # Draw the graph using NetworkX and Matplotlib
    nx.draw(connected_graph, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black')
    plt.title("Connected Random Graph")
    plt.show()

for _ in range(10):
    create_random_graph()