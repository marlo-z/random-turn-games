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
        self.money = starting_money

    def strategy(self, game, curr_vertex) -> int:
        return super().strategy(game, curr_vertex)

    def wager_strategy(self):
        wager = random.uniform(0, 0.05)
        self.money -= wager
        if self.money < 0:
            return None
        return wager

# Initialize strategy as a dictionary where strategy is defined by
# a move on the graph and a wager for the turn
# the corresponding value is the percent of the time a player would make such a move
# initialized to 0
def initialize_strategy(graph, curr_vertex, money):
    strat = {}
    for neighbor in graph.neighbors(curr_vertex):
        for wager in range(money // 100):
            strat[(neighbor, wager)] = 0
    return strat

# We initialize the regret for each move to be 0
def initialize_regret(strat):
    regret = {}
    for move in strat.keys():
        regret[move] = 0
    return regret

# Return true if the move being made takes you to a boundary
def terminal_state(graph, state):
    return graph.at_boundary(state[0])


def monte_carlo_cfr(game, state, player, t, max_strat, min_strat, chance = False, wager = (0, 0)):
    # if you're at coin flip stage
    if chance:
        odds = wager[0]/(wager[0]+wager[1])
        min_or_max_player = np.random.choice([0, 1], p=[1-odds, odds])
        if min_or_max_player == 1:
            return monte_carlo_cfr(game, state, player, initialize_strategy(game.graph, max_strat[0][0], 0), min_strat)
        else:
            return monte_carlo_cfr(game, state, player, max_strat, initialize_strategy(game.graph, min_strat[0][0], 0))

    # if you're at a terminal node, return it's value
    if terminal_state(game.graph, state):
        return game.graph.boundary_func([state[0]])
    
    