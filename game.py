import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Game:
    def __init__(self, graph_type='random'):
        self.graph = Graph()
        self.min_player = ...
        self.max_player = ...
        self.curr_vertex = ... # random vertex
        
    def display(self):
        self.graph.display()


class Graph:
    #TODO: add attributes to each vertex --> representing value of boundary vertices
    def __init__(self, n = 10, p = 0.1):
        # N: Number of nodes in the graph
        # P: Desired probability of an edge between any two nodes for connectivity
        
        # Create an initially empty graph
        self.graph = nx.Graph()
        # Add nodes
        self.graph.add_nodes_from(range(n))
        # Start connecting nodes to form a connected graph
        for node in range(1, n):
            target_node = node - 1
            self.graph.add_edge(node, target_node)
            # Add additional edges with probability p
            for potential_target in range(target_node - 1, -1, -1):
                if potential_target != node and potential_target not in self.graph.neighbors(node):
                    if np.random.rand() < p:
                        self.graph.add_edge(node, potential_target)

    def display(self):
        # Draw the graph using NetworkX and Matplotlib
        nx.draw(self.graph, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black')
        plt.title("Connected Random Graph")
        plt.show()

class DefaultPlayer():
    def __init__(self, min_or_max):
        self.objective = min_or_max

    def strategy(self, graph, curr_vertex) -> int:
        pass

# main
for _ in range(10):
    game = Game()
