import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random


class Game:
    def __init__(self, graph_type='random'):
        self.graph = Graph()
        # TODO: actually well define min and max
        self.min_player = DefaultPlayer(True)
        self.max_player = DefaultPlayer(False)
        self.curr_vertex = random.choice(
            list(self.graph.graph.nodes))  # random vertex
        self.graph.set_node_color(self.curr_vertex, 'red')

    def display(self):
        self.graph.display()

    def turn(self):
        advantage = random.randint(0, 1)
        self.graph.set_node_color(self.curr_vertex, 'skyblue')
        if advantage == 1:
            self.curr_vertex = self.max_player.strategy(
                self.graph, self.curr_vertex)

        else:
            self.curr_vertex = self.min_player.strategy(
                self.graph, self.curr_vertex)
        self.graph.set_node_color(self.curr_vertex, 'red')


class Graph:
    # TODO: add attributes to each vertex --> representing value of boundary vertices
    def __init__(self, n=10, p=0.1):
        self.node_colors = {}
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
        colors = [self.node_colors[node]
                  if node in self.node_colors else 'skyblue' for node in self.graph.nodes]

        nx.draw(self.graph, with_labels=True, node_size=500,
                node_color=colors, font_size=10, font_color='black')
        plt.title("Connected Random Graph")
        plt.show()

    def set_node_color(self, node, color):
        self.node_colors[node] = color


class DefaultPlayer():
    def __init__(self, min_or_max):
        self.objective = min_or_max

    def strategy(self, graph, curr_vertex) -> int:
        # default strat is just choose a random neighbor
        neighbors = list(graph.neighbors(curr_vertex))
        if neighbors:
            return random.choice(neighbors)
        else:
            return None


# main
for _ in range(10):
    game = Game()
