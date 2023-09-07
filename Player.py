import random

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