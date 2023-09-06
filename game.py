import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from Player import DefaultPlayer

class Game:
    def __init__(self, graph_type='random'):
        self.graph = Graph()
        self.min_player = ...
        self.max_player = ...
        self.curr_vertex = ... # random vertex
        
    def display(self):
        self.graph.display()

    def next_step(self):
        self.graph.next_step()


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

        self.color_list = ['blue'] * n

        self.curr_node = np.random.randint(1, n+1)

        # offset index = node number - 1 
        self.color_list[self.curr_node - 1] = 'red'

        self.min_player = DefaultPlayer()
        self.max_player = DefaultPlayer()

    def next_step(self):
        neighbors = list(self.graph.neighbors(self.curr_node))

        print("DEBUG:", self.curr_node, neighbors)

        # get random neighbor
        next_node_index = np.random.randint(0, len(neighbors))
        next_node = list(self.graph.nodes)[next_node_index]

        # update colors of current node
        self.color_list[self.curr_node - 1] = 'blue'
        self.color_list[next_node - 1] = 'red'

        self.curr_node = next_node
        
        return

    def display(self):
        # Draw the graph using NetworkX and Matplotlib
        nx.draw(self.graph, with_labels=True, node_size=500, node_color=self.color_list, font_size=10, font_color='black')
        plt.title("Connected Random Graph")
        plt.show()


# main
# for _ in range(10):
#     game = Game()
#     game.display()

num_rounds = 10

game = Game()
game.display()
for _ in range(num_rounds):
    game.next_step()
    game.display()
