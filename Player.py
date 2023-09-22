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

# Return true if the node in the game tree is the coin flip, pls note that we're
# going to have to mindful of the formatting of this
def is_chance(state):
    if state[0] == True:
        return True

def monte_carlo_cfr(game, state, player, t, max_strat, min_strat):
    # if you're at a terminal node, return it's value
    if terminal_state(game.graph, state):
        return game.graph.boundary_func([state[0]])
    # if you're at coin flip stage
    if is_chance(state):
        odds = state[1]/(state[1]+state[2])
        min_or_max_player = np.random.choice([0, 1], p=[1-odds, odds])
        chosen_strat = [min_strat, max_strat][min_or_max_player]
        return
    