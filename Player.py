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


class WagerPlayer(DefaultPlayer):
    def __init__(self, min_or_max, starting_money=1):
        super().__init__(min_or_max)
        self.money = starting_money

    def strategy(self, graph, curr_vertex) -> int:
        return super().strategy(graph, curr_vertex)

    def wager_strategy(self):
        wager = random.uniform(0, 0.05)
        self.money -= wager
        if self.money < 0:
            return None
        return wager


def monte_carlo_cfr(game, num_iterations):
    # Initialize cumulative regrets and strategy for both players
    cumulative_regrets = {}  # Dictionary to store cumulative regrets
    cumulative_strategy = {}  # Dictionary to store cumulative strategies

    for iteration in range(num_iterations):
        # Perform a single MCCFR iteration
        utility = traverse_game_tree(game, cumulative_strategy)

        # Backpropagate utility and update cumulative regrets
        update_regrets(game, cumulative_regrets, utility)

    # Compute average strategy from cumulative strategy values
    average_strategy = compute_average_strategy(cumulative_strategy)

    return average_strategy


def traverse_game_tree(game, cumulative_strategy):
    # Perform a single traversal of the game tree
    # Start from the root of the game tree
    # Choose actions for both players using their strategies
    # Simulate the game and return the utility (e.g., win or loss)
    pass


def update_regrets(game, cumulative_regrets, utility):
    # Backpropagate utility and update cumulative regrets
    # Calculate regrets for each player based on the utility
    # Update cumulative regrets with these values
    pass


def compute_average_strategy(cumulative_strategy):
    # Compute the average strategy from cumulative strategy values
    # Normalize cumulative strategy values to get the average strategy
    pass
