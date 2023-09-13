import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy.spatial import ConvexHull, convex_hull_plot_2d

from Player import DefaultPlayer, WagerPlayer


class Game:
    def __init__(self, advantage=0.5, graph_type='random', wager=True):
        # upon initialization, every node will be set to color blue
        self.graph = Graph()
        # TODO: actually well define min and max
        self.wager = wager
        if not wager:
            self.min_player = DefaultPlayer(True)
            self.max_player = DefaultPlayer(False)
        else:
            self.min_player = WagerPlayer(True)
            self.max_player = WagerPlayer(False)
        # self.curr_vertex = random.choice(list(self.graph.graph.nodes))
        self.curr_vertex = self.graph.find_central_node()
        # curr_vertx = red, others = blue
        self.graph.set_node_color(self.curr_vertex, 'red')

        # advantage = probability that MAX player moves
        self.advantage = advantage

    def display(self):
        self.graph.display()

    def turn(self):
        if self.at_boundary():
            self.graph.set_node_color(self.curr_vertex, 'green')
            return True
        else:
            self.graph.set_node_color(self.curr_vertex, 'blue')
        if self.wager:
            a = self.max_player.wager_strategy()
            b = self.min_player.wager_strategy()
            if a == None or b == None:
                return True
            self.advantage = a/(a+b)
        min_or_max_player = np.random.choice(
            [0, 1], p=[1-self.advantage, self.advantage])
        chosen_player = [self.min_player, self.max_player][min_or_max_player]
        self.curr_vertex = chosen_player.strategy(self.graph, self.curr_vertex)

        self.graph.set_node_color(self.curr_vertex, 'red')

        # return whether or not game has ended
        return False

    def at_boundary(self):
        return self.graph.at_boundary(self.curr_vertex)


class Graph:
    # TODO: add attributes to each vertex --> representing value of boundary vertices
    def __init__(self, n=30, p=0.1):

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

        # returns a dict keyed by nodes
        self.node_pos = nx.spring_layout(self.graph)
        # print(self.node_pos)

        # this is the bare nodes
        self.nodes = list(range(n))
        # a dict mapping {node : color}
        self.node_colors = {node: 'blue' for node in range(n)}
        self.boundaries = self.set_boundaries()
        self.boundary_func = {}
        for bound in self.boundaries:
            # a hash set containing all boundary nodes # function mapping boundary to score                               # a dict mapping {node : score} --> or could be added as an attribute of the node
            self.boundary_func[bound] = random.randint(0, 10)

    def find_central_node(self):
        def dist(pos): return pos[0]**2 + pos[1]**2
        min_dist = np.inf
        closest_to_center = None
        for node, pos in self.node_pos.items():
            if dist(pos) < min_dist:
                min_dist = dist(pos)
                closest_to_center = node
        return closest_to_center

    def set_boundaries(self):
        coords = np.array([self.node_pos[node] for node in self.nodes])
        hull = ConvexHull(coords)
        boundary_nodes = set()
        for i, j in hull.simplices:
            if i not in boundary_nodes:
                boundary_nodes.add(i)
                self.set_node_color(i, 'green')
            if j not in boundary_nodes:
                boundary_nodes.add(j)
                self.set_node_color(j, 'green')
        # print(coords)
        # print(hull.simplices)
        # print(boundary_nodes)
        return boundary_nodes

    def display(self):
        # Draw the graph using NetworkX and Matplotlib
        # colors = [self.node_colors[node]
        #           if node in self.node_colors else 'skyblue' for node in self.graph.nodes]
        node_colors = [self.node_colors[node] for node in self.nodes]
        nx.draw(self.graph, pos=self.node_pos, with_labels=True, node_size=300,
                node_color=node_colors, font_size=10, font_color='black')
        plt.title("Connected Random Graph")
        plt.show()

    def set_node_color(self, node, color):
        self.node_colors[node] = color

    def neighbors(self, vertex):
        return self.graph.neighbors(vertex)

    def at_boundary(self, node):
        return node in self.boundaries


# main
def main():
    num_turns = 10
    game = Game()
    for _ in range(num_turns):
        game.display()
        end = game.turn()
        if end:
            return game.graph.boundary_func[game.curr_vertex]


print(main())
