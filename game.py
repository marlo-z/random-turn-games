import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

from Player import DefaultPlayer


class Game:
    def __init__(self, advantage = 0.5, graph_type='random'):
        self.graph = Graph()                                            # upon initialization, every node will be set to color blue
        # TODO: actually well define min and max
        self.min_player = DefaultPlayer(True)
        self.max_player = DefaultPlayer(False)
        self.curr_vertex = random.choice(list(self.graph.graph.nodes))  # random vertex
        self.graph.set_node_color(self.curr_vertex, 'red')              # curr_vertx = red, others = blue

        self.advantage = advantage                                      # advantage = probability that MAX player moves

    def display(self):
        self.graph.display()

    def turn(self):
        self.graph.set_node_color(self.curr_vertex, 'blue')
        
        min_or_max_player = np.random.choice([0,1], p = [1-self.advantage, self.advantage])
        chosen_player = [self.min_player, self.max_player][min_or_max_player]
        self.curr_vertex = chosen_player.strategy(self.graph, self.curr_vertex)

        self.graph.set_node_color(self.curr_vertex, 'red')

        # return whether or not game has ended
        return False

    def at_boundary(self):
        return self.graph.at_boundary()


class Graph:
    # TODO: add attributes to each vertex --> representing value of boundary vertices
    def __init__(self, n=10, p=0.1):
        
        # all nodes (0, ..., n-1) initially set to color blue
        # N: Number of nodes in the graph
        # P: Desired probability of an edge between any two nodes for connectivity

        # Create an initially empty graph
        self.graph = nx.Graph()             # this is the underlying Networkx graph object
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

        self.node_pos = nx.spring_layout(self.graph)                                    # returns a dict keyed by nodes

        # TODO:
        self.nodes = list(range(n))                                                     # this is the bare nodes
        self.node_colors = {node : 'blue' for node in range(n)}                         # a dict mapping {node : color}
        # self.boundaries = ...                                                           # a dict mapping {node : bool}
        self.boundary_func = ... # function mapping boundary to score                               # a dict mapping {node : score} --> or could be added as an attribute of the node
    
    def find_boundaries(self):
        pass

    def display(self):
        # Draw the graph using NetworkX and Matplotlib
        # colors = [self.node_colors[node]
        #           if node in self.node_colors else 'skyblue' for node in self.graph.nodes]
        node_colors = [self.node_colors[node] for node in self.nodes]
        nx.draw(self.graph, pos=self.node_pos, with_labels=True, node_size=500,
                node_color=node_colors, font_size=10, font_color='black')
        plt.title("Connected Random Graph")
        plt.show()

    def set_node_color(self, node, color):
        self.node_colors[node] = color

    def neighbors(self, vertex):
        return self.graph.neighbors(vertex)

    def at_boundary(self):
        return self.curr_vertex in self.boundary_func


# main
def main():
    num_turns = 10
    game = Game()
    print(game.graph.node_pos)
    for _ in range(num_turns):
        end = game.turn()
        game.display()
        if end:
           break 

main()