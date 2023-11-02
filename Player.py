import random
import numpy as np


class DefaultPlayer():
    def __init__(self, min_or_max):
        self.objective = min_or_max

    def strategy(self, game, curr_vertex) -> int:
        graph = game.graph
        # default strat is just choose a random neighbor
        neighbors = list(graph.neighbors(curr_vertex))
        if neighbors:
            return random.choice(neighbors)
        else:
            return None


class WagerPlayer(DefaultPlayer):
    def __init__(self, min_or_max, starting_money=1):
        super().__init__(min_or_max)
        self.starting_money = starting_money
        self.money = starting_money

    def money_lost(self):
        return self.starting_money-self.money

    def strategy(self, game, curr_vertex) -> int:
        return super().strategy(game, curr_vertex)

    def wager_strategy(self):
        wager = random.uniform(0, 0.05)
        self.money -= wager
        if self.money < 0:
            return None
        return wager
