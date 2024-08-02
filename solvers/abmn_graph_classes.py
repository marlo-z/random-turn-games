from collections.abc import Callable
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from functions import get_bounds, interp_n_matrix, interp_m_matrix, initialize_m_n_matrices


class LineGraphSolver:

    def __init__(
        self,
        left: int = 6,
        right: int = 6,
        time_steps: int = 100,
        maxi_reward: float = 100000,
        mina_reward: float = 99994
    ):
        self.left_end = left     # left endpoint: -k
        self.right_end = right      # right endpoint: l
        self.length = self.left + self.right + 1    # total length: k+l
        self.time_steps = time_steps   # Time steps

        # Note: position index i will be shifted
        # before: left end = -k, middle = 0, right end = l
        # now: left end = 0, middle = k, Pright end = k + l (= L)

        self.n_lambda = mina_reward
        self.m_lambda = maxi_reward

        # initialize the m,n values at time t=0,
        # then iterate starting from t=1, use m(t-1), n(t-1) to compute a(t) and b(t)
        # then use a(t) and b(t) to compute m(t) and n(t)

        # Each matrix: vertical axis (rows): time step, horizontal axis (colunmns): position
        # Therefore, m[t][i] access m value at time t, position index i
        self.a = np.zeros((self.time_steps, self.length))
        self.b = np.zeros((self.time_steps, self.length))
        self.m = np.zeros((self.time_steps, self.length))
        self.n = np.zeros((self.time_steps, self.length))

        # Initialize positional boundary values
        self.n[:, 0] = self.n_lambda
        self.m[:, -1] = self.m_lambda

        initial_ratio = np.arctan(np.linspace(
            -self.left_end, self.right_end, self.length-2) * 0.5) / np.pi + 0.5
        self.m[0, 1:-1] = self.m_lambda * initial_ratio
        self.n[0, 1:-1] = self.n_lambda * (1 - initial_ratio)

    def iterateABMN(self, t: int, debug=False) -> None:
        for i in range(1, self.length - 1):
            delta_m = self.m[t-1][i+1] - self.m[t-1][i-1]
            delta_n = self.n[t-1][i-1] - self.n[t-1][i+1]
            # Compute a,b using previous m,n
            self.b[t][i] = delta_m / (delta_m / delta_n + 1) \
                / (delta_m / delta_n + 1)
            self.a[t][i] = (delta_m / delta_n) * self.b[t][i]
            # Compute current m,n using current a,b
            maxi_wager_ratio = self.a[t][i] / (self.a[t][i] + self.b[t][i])
            mina_wager_ratio = self.b[t][i] / (self.a[t][i] + self.b[t][i])
            self.m[t][i] = maxi_wager_ratio * self.m[t-1][i+1] \
                + mina_wager_ratio * self.m[t-1][i-1] - self.a[t][i]
            self.n[t][i] = maxi_wager_ratio * self.n[t-1][i+1] \
                + mina_wager_ratio * self.n[t-1][i-1] - self.b[t][i]

        if debug:
            print(f"-------------- step {t} --------------")
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))
            print("delta_m = {}, delta_n = {}".format(delta_m, delta_n))

    def solve(self, debug=False) -> None:
        for t in range(1, self.time_steps):
            if t % (self.time_steps // 10) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)


class OriginCrossGraphSolver:

    def __init__(
            self,
            left: int = 6,
            right: int = 6,
            top: int = 6,
            bottom: int = 6,
            time_steps: int = 100,
            horizontal_maxi_reward: float = 100000,
            horizontal_mina_reward: float = 99994,
            vertical_maxi_reward: float = 100000,
            vertical_mina_reward: float = 99994
    ):
        self.right_end = left + right
        self.bottom_end = top + bottom
        self.origin = (top, left)
        self.horizontal_length = self.right_end + 1
        self.vertical_length = self.bottom_end + 1
        self.time_steps = time_steps
        self.horizontal_m_lambda = horizontal_maxi_reward
        self.horizontal_n_lambda = horizontal_mina_reward
        self.vertical_m_lambda = vertical_maxi_reward
        self.vertical_n_lambda = vertical_mina_reward

        self.a = np.zeros((
            self.time_steps,
            self.vertical_length,
            self.horizontal_length))
        self.b = self.a.copy()
        self.m = self.a.copy()
        self.n = self.a.copy()
        self.m[:, self.origin[0], -1] = self.horizontal_m_lambda
        self.m[:, -1, self.origin[1]] = self.vertical_m_lambda
        self.n[:, self.origin[0], 0] = self.horizontal_n_lambda
        self.n[:, 0, self.origin[1]] = self.vertical_n_lambda
        horizontal_initial_ratio = np.arctan(np.linspace(
            -left, right, self.horizontal_length-2) * 0.5) / np.pi + 0.5
        vertical_initial_ratio = np.arctan(np.linspace(
            -top, bottom, self.vertical_length-2) * 0.5) / np.pi + 0.5
        self.m[0, self.origin[0], 1:-
               1] = self.horizontal_m_lambda * horizontal_initial_ratio
        self.m[0, 1:-1, self.origin[1]
               ] = self.vertical_m_lambda * vertical_initial_ratio
        self.n[0, self.origin[0], 1:-
               1] = self.horizontal_n_lambda * (1 - horizontal_initial_ratio)
        self.n[0, 1:-1, self.origin[1]
               ] = self.vertical_n_lambda * (1 - vertical_initial_ratio)

    def find_next_move(self, t: int, i: int, j: int) \
            -> tuple[tuple[int, int], tuple[int, int]]:
        m_max = {}
        m_max[(i-1, j)] = self.m[t-1, i-1, j]
        m_max[(i+1, j)] = self.m[t-1, i+1, j]
        m_max[(i, j-1)] = self.m[t-1, i, j-1]
        m_max[(i, j+1)] = self.m[t-1, i, j+1]

        n_max = {}
        n_max[(i-1, j)] = self.n[t-1, i-1, j]
        n_max[(i+1, j)] = self.n[t-1, i+1, j]
        n_max[(i, j-1)] = self.n[t-1, i, j-1]
        n_max[(i, j+1)] = self.n[t-1, i, j+1]
        v_plus = max(m_max.keys(), key=m_max.get)
        v_minus = max(n_max.keys(), key=n_max.get)

        return v_plus, v_minus

    def iterateABMN(self, t: int, debug: bool = False) -> None:
        if debug:
            print(f"-------------- step {t} --------------")

        for i in range(1, self.vertical_length - 1):
            for j in range(1, self.horizontal_length - 1):
                if self.m[t - 1, i, j] == 0 and self.n[t - 1, i, j] == 0:
                    continue
                v_plus, v_minus = self.find_next_move(t, i, j)
                delta_m = self.m[t-1, *v_plus] - self.m[t-1, *v_minus]
                delta_n = self.n[t-1, *v_minus] - self.n[t-1, *v_plus]
                self.b[t, i, j] = delta_m / (delta_m / delta_n + 1) \
                    / (delta_m / delta_n + 1)
                self.a[t, i, j] = (delta_m / delta_n) * self.b[t, i, j]
                maxi_wager_ratio = self.a[t, i, j] / \
                    (self.a[t, i, j] + self.b[t, i, j])
                mina_wager_ratio = self.b[t, i, j] / \
                    (self.a[t, i, j] + self.b[t, i, j])
                self.m[t, i, j] = maxi_wager_ratio * self.m[t-1, *v_plus] \
                    + mina_wager_ratio * \
                    self.m[t-1, *v_minus] - self.a[t, i, j]
                self.n[t, i, j] = maxi_wager_ratio * self.n[t-1, *v_plus] \
                    + mina_wager_ratio * \
                    self.n[t-1, *v_minus] - self.b[t, i, j]

                if debug:
                    print("current position: ({}, {}), v_plus = {}, v_minus = {}, delta_m = {}, delta_n = {}"
                          .format(i, j, v_plus, v_minus, delta_m, delta_n))

        if debug:
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))

    def solve(self, debug: bool = False) -> None:
        for t in range(1, self.time_steps):
            if t % max((self.time_steps // 10), 1) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)


class MatrixGraphSolver:

    def __init__(
            self,
            m_map: np.ndarray[tuple[int, int], float],
            # [(left corner), (right corner)]
            n_map: np.ndarray[tuple[int, int], float],
            boundary_coords: list[tuple[int, int]],
            time_steps: int = 100,
    ):
        self.time_steps = time_steps
        self.bounds = boundary_coords
        self.a = np.zeros((time_steps, *m_map.shape))
        self.b = self.a.copy()
        self.m_map = m_map
        self.n_map = n_map
        self.m = np.tile(m_map, (time_steps, 1, 1))
        self.n = np.tile(n_map, (time_steps, 1, 1))

    def find_next_move(self, t: int, i: int, j: int) \
            -> tuple[tuple[int, int], tuple[int, int]]:
        m_max = {}
        n_max = {}

        for row, col in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if row < 0 or row >= self.m_map.shape[0] \
                    or col < 0 or col >= self.m_map.shape[1] \
                    or self.m_map[row, col] == np.inf:
                continue
            m_max[(row, col)] = self.m[t-1, row, col]
            n_max[(row, col)] = self.n[t-1, row, col]

        v_plus = max(m_max.keys(), key=m_max.get)
        v_minus = max(n_max.keys(), key=n_max.get)

        return v_plus, v_minus

    def iterateABMN(self, t: int, debug: bool = False) -> None:
        if debug:
            print(f"-------------- step {t} --------------")

        for i in range(0, self.m_map.shape[0]):
            for j in range(0, self.m_map.shape[1]):
                if self.m_map[i, j] == np.inf or (i, j) in self.bounds:
                    continue

                v_plus, v_minus = self.find_next_move(t, i, j)
                if v_plus == v_minus:
                    self.a[t, i, j] = 0
                    self.b[t, i, j] = 0
                    self.m[t, i, j] = self.m[t-1, *v_plus]
                    self.n[t, i, j] = self.n[t-1, *v_minus]

                else:
                    delta_m = self.m[t-1, *v_plus] - self.m[t-1, *v_minus]
                    delta_n = self.n[t-1, *v_minus] - self.n[t-1, *v_plus]
                    # need to work on cases when delta_m or delta_n == 0, we should let them cooperate
                    # but need to figure out logic of which direction is correct and that hurts brain
                    if delta_m == 0 or delta_n == 0:
                        self.a[t, i, j] = 0
                        self.b[i, i, j] = 0
                        if delta_m == 0:
                            self.m[t, i, j] = self.m[t-1, *v_minus]
                            self.n[t, i, j] = self.n[t-1, *v_minus]
                        else:
                            self.m[t, i, j] = self.m[t-1, *v_plus]
                            self.n[t, i, j] = self.n[t-1, *v_plus]
                    else:
                        temp_ratio = delta_m/delta_n
                        self.b[t, i, j] = delta_m / (temp_ratio + 1) \
                            / (temp_ratio + 1)
                        self.a[t, i, j] = (temp_ratio) * self.b[t, i, j]

                        a_plus_b = self.a[t, i, j] + self.b[t, i, j]
                        maxi_wager_ratio = self.a[t, i, j] / a_plus_b
                        mina_wager_ratio = self.b[t, i, j] / a_plus_b
                        temp_m = maxi_wager_ratio * self.m[t-1, *v_plus] \
                            + mina_wager_ratio * \
                            self.m[t-1, *v_minus] - self.a[t, i, j]
                        temp_n = maxi_wager_ratio * self.n[t-1, *v_plus] \
                            + mina_wager_ratio * \
                            self.n[t-1, *v_minus] - self.b[t, i, j]
                        self.m[t, i, j] = temp_m
                        self.n[t, i, j] = temp_n
                if debug:
                    print("current position: ({}, {}), v_plus = {}, v_minus = {}, delta_m = {}, delta_n = {}"
                          .format(i, j, v_plus, v_minus, delta_m, delta_n))

        if debug:
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))

    def solve(self, debug: bool = False) -> None:
        if debug:
            print("-------------- initial values --------------")
            print("bounds = {}".format(self.bounds))
            print("m = {}".format(self.m[0]))
            print("n = {}".format(self.n[0]))

        for t in range(1, self.time_steps):
            if t % max((self.time_steps // 10), 1) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)

    def find_batteground(self, t, tolerance_ratio=3):
        battleground = []
        a = self.a
        b = self.b
        _, rows, cols = a.shape
        for i in range(rows):
            for j in range(cols):
                m = max(a[t][i][j], b[t][i][j])
                n = min(a[t][i][j], b[t][i][j])
                ratio = m / n if n != 0 else float('inf')
                if ratio < tolerance_ratio:
                    battleground.append((i, j))
        return battleground


class GridSolver:

    def __init__(
            self,
            boundary_coords: tuple[int, int] = (
                3, 3),        # (top right corner)
            time_steps: int = 100
    ):
        self.time_steps = time_steps
        self.bounds = [(0, 0), boundary_coords]
        self.x_len = boundary_coords[0]
        self.y_len = boundary_coords[1]
        self.a = np.zeros((time_steps, self.x_len, self.y_len))
        self.b = np.zeros((time_steps, self.x_len, self.y_len))
        self.m = np.zeros((time_steps, self.x_len, self.y_len))
        self.n = np.zeros((time_steps, self.x_len, self.y_len))
        self.m_map = np.ones((self.x_len, self.y_len)) * (-np.inf)
        self.n_map = np.ones((self.x_len, self.y_len)) * (-np.inf)

        # boundary values
        for t in range(1, time_steps):
            for x in range(self.x_len):
                for y in range(self.y_len):
                    if x == 0 or y == 0 or x == (self.x_len - 1) or y == (self.y_len - 1):
                        if x == 0 and y == 0:
                            self.m[t][x][y] = 0
                            self.n[t][x][y] = 6
                        else:
                            self.m[t][x][y] = x+y
                            self.n[t][x][y] = 1/(x+y)

        # initial values
        self.a[0] = np.random.rand(self.x_len, self.y_len)
        self.b[0] = np.random.rand(self.x_len, self.y_len)

    def find_next_move(self, t: int, i: int, j: int) \
            -> tuple[tuple[int, int], tuple[int, int]]:
        m_max = {}
        n_max = {}

        for row, col in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if row < 0 or row >= self.m_map.shape[0] \
                    or col < 0 or col >= self.m_map.shape[1] \
                    or self.m_map[row, col] == np.inf:
                continue
            m_max[(row, col)] = self.m[t-1, row, col]
            n_max[(row, col)] = self.n[t-1, row, col]

        v_plus = max(m_max.keys(), key=m_max.get)
        v_minus = max(n_max.keys(), key=n_max.get)

        return v_plus, v_minus

    def iterateABMN(self, t: int, debug: bool = False) -> None:
        if debug:
            print(f"-------------- step {t} --------------")

        for i in range(0, self.m_map.shape[0]):
            for j in range(0, self.m_map.shape[1]):
                if self.m_map[i, j] == np.inf or (i, j) in self.bounds:
                    continue

                v_plus, v_minus = self.find_next_move(t, i, j)

                delta_m = self.m[t-1, *v_plus] - self.m[t-1, *v_minus]
                delta_n = self.n[t-1, *v_minus] - self.n[t-1, *v_plus]

                if debug:
                    print("M", self.m[t])
                    print("N", self.n[t])
                    print("delta m", delta_m)
                    print("delta_n", delta_n)

                self.b[t, i, j] = delta_m / (delta_m / delta_n + 1) \
                    / (delta_m / delta_n + 1)
                self.a[t, i, j] = (delta_m / delta_n) * self.b[t, i, j]

                maxi_wager_ratio = self.a[t, i, j] / \
                    (self.a[t, i, j] + self.b[t, i, j])
                mina_wager_ratio = self.b[t, i, j] / \
                    (self.a[t, i, j] + self.b[t, i, j])
                self.m[t, i, j] = maxi_wager_ratio * self.m[t-1, *v_plus] \
                    + mina_wager_ratio * \
                    self.m[t-1, *v_minus] - self.a[t, i, j]
                self.n[t, i, j] = maxi_wager_ratio * self.n[t-1, *v_plus] \
                    + mina_wager_ratio * \
                    self.n[t-1, *v_minus] - self.b[t, i, j]

                if debug:
                    print("current position: ({}, {}), v_plus = {}, v_minus = {}, delta_m = {}, delta_n = {}"
                          .format(i, j, v_plus, v_minus, delta_m, delta_n))

        if debug:
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))

    def solve(self, debug: bool = False) -> None:
        if debug:
            print("-------------- initial values --------------")
            print("bounds = {}".format(self.bounds))
            print("a = {}".format(self.a[0]))
            print("b = {}".format(self.b[0]))
            print("m = {}".format(self.m[0]))
            print("n = {}".format(self.n[0]))

        for t in range(1, self.time_steps):
            if t % max((self.time_steps // 10), 1) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)


class ContinuousGraphSolver:

    def __init__(
            self,
            m_map: np.ndarray[tuple[int, int], float],
            # [(left corner), (right corner)]
            n_map: np.ndarray[tuple[int, int], float],
            boundary_coords: list[tuple[int, int]],
            move_radius: float,
            time_steps: int = 100,
    ):
        self.time_steps = time_steps
        self.bounds = boundary_coords
        self.radius = move_radius
        self.a = np.zeros((time_steps, *m_map.shape))
        self.b = self.a.copy()
        self.m_map = m_map
        self.n_map = n_map
        self.m = np.tile(m_map, (time_steps, 1, 1))
        self.n = np.tile(n_map, (time_steps, 1, 1))

    def points_within_radius(self, center):
        i, j = center
        radius = self.radius
        result = []

        x_start = int(np.floor(i - radius))
        x_end = int(np.ceil(i + radius))
        y_start = int(np.floor(j - radius))
        y_end = int(np.ceil(j + radius))

        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                if np.sqrt((x - i) ** 2 + (y - j) ** 2) <= radius:
                    result.append((x, y))

        return result

    def find_next_move(self, t: int, i: int, j: int) \
            -> tuple[tuple[int, int], tuple[int, int]]:
        m_max = {}
        n_max = {}
        moves = self.points_within_radius((i, j))
        for row, col in moves:
            if row < 0 or row >= self.m_map.shape[0] \
                    or col < 0 or col >= self.m_map.shape[1] \
                    or self.m_map[row, col] == np.inf:
                continue
            m_max[(row, col)] = self.m[t-1, row, col]
            n_max[(row, col)] = self.n[t-1, row, col]

        v_plus = max(m_max.keys(), key=m_max.get)
        v_minus = max(n_max.keys(), key=n_max.get)

        return v_plus, v_minus

    def iterateABMN(self, t: int, debug: bool = False) -> None:
        # print(t)
        if debug:
            print(f"-------------- step {t} --------------")

        for i in range(0, self.m_map.shape[0]):
            for j in range(0, self.m_map.shape[1]):
                if self.m_map[i, j] == np.inf or (i, j) in self.bounds:
                    continue

                v_plus, v_minus = self.find_next_move(t, i, j)
                if v_plus == v_minus:
                    self.a[t, i, j] = 0
                    self.b[t, i, j] = 0
                    self.m[t, i, j] = self.m[t-1, *v_plus]
                    self.n[t, i, j] = self.n[t-1, *v_minus]
                    if debug:
                        print(t)
                else:
                    delta_m = self.m[t-1, *v_plus] - self.m[t-1, *v_minus]
                    delta_n = self.n[t-1, *v_minus] - self.n[t-1, *v_plus]
                    # need to work on cases when delta_m or delta_n == 0, we should let them cooperate
                    # but need to figure out logic of which direction is correct and that hurts brain
                    if delta_m == 0 or delta_n == 0:
                        self.a[t, i, j] = 0
                        self.b[t, i, j] = 0
                        if delta_m == 0:
                            self.m[t, i, j] = self.m[t-1, *v_minus]
                            self.n[t, i, j] = self.n[t-1, *v_minus]
                        else:
                            self.m[t, i, j] = self.m[t-1, *v_plus]
                            self.n[t, i, j] = self.n[t-1, *v_plus]
                    else:
                        temp_ratio = delta_m/delta_n
                        self.b[t, i, j] = delta_m / (temp_ratio + 1) \
                            / (temp_ratio + 1)
                        self.a[t, i, j] = (temp_ratio) * self.b[t, i, j]

                        a_plus_b = self.a[t, i, j] + self.b[t, i, j]
                        maxi_wager_ratio = self.a[t, i, j] / a_plus_b
                        mina_wager_ratio = self.b[t, i, j] / a_plus_b
                        temp_m = maxi_wager_ratio * self.m[t-1, *v_plus] \
                            + mina_wager_ratio * \
                            self.m[t-1, *v_minus] - self.a[t, i, j]
                        temp_n = maxi_wager_ratio * self.n[t-1, *v_plus] \
                            + mina_wager_ratio * \
                            self.n[t-1, *v_minus] - self.b[t, i, j]
                        self.m[t, i, j] = temp_m
                        self.n[t, i, j] = temp_n
                    if debug:
                        print(t)

        if debug:
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))

    def solve(self, debug: bool = False) -> None:
        if debug:
            print("-------------- initial values --------------")
            print("bounds = {}".format(self.bounds))
            print("m = {}".format(self.m[0]))
            print("n = {}".format(self.n[0]))

        for t in range(1, self.time_steps):
            if t % max((self.time_steps // 10), 1) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)

    def find_batteground(self, t, tolerance_ratio=3):
        battleground = []
        a = self.a
        b = self.b
        _, rows, cols = a.shape
        for i in range(rows):
            for j in range(cols):
                m = max(a[t][i][j], b[t][i][j])
                n = min(a[t][i][j], b[t][i][j])
                ratio = m / n if n != 0 else float('inf')
                if ratio < tolerance_ratio:
                    battleground.append((i, j))
        return battleground


# Main
#GridSolver(boundary_coords=(4, 4), time_steps=5).solve(debug=True)
'''
from abmn_graph_classes import ContinuousGraphSolver
from functions import *
import numpy as np
import matplotlib.pyplot as plt
'''


def solve_abmn(rows, cols, radius, lam, time=100):
    #mat = np.full((rows, cols), -np.inf)
    #n_map = mat.copy()
    #n_map[0, 0] = lam
    #n_map[rows-1, cols-1] = 0
    #bounds = get_bounds(n_map)
    #n_map = interp_n_matrix(n_map)
    #n_map = uniform_random(n_map)
    # print(n_map)

    #m_map = mat.copy()
    #m_map[0, 0] = 0
    #m_map[rows-1, cols-1] = 1
    #m_map = interp_m_matrix(m_map)
    midpoint = (rows // 2, cols // 2)

    m_map, n_map = initialize_m_n_matrices(rows, cols, lam, midpoint)
    bounds = [(0, 0), (rows-1, cols-1)]
    print(m_map)
    print(n_map)
    #m_map = uniform_random(m_map)

    solver = ContinuousGraphSolver(n_map=n_map,
                                   m_map=m_map,
                                   time_steps=time,
                                   boundary_coords=bounds,
                                   move_radius=radius
                                   )

    solver.solve(debug=False)
    print(solver.m[time-1])
    print("break")
    print(solver.n[time-1])
    coords = solver.find_batteground(time - 1, 2)
    plt.scatter(*zip(*[(i, j) for i in range(m_map.shape[0])
                for j in range(m_map.shape[1])]), c='purple')
    if coords:
        plt.scatter(*zip(*coords), c='red', marker='o', s=100)
    plt.scatter(*zip(*bounds), c='black', marker='x', s=100)
    plt.title(f'lambda = {lam}')
    plt.grid(True)
    plt.show()


def solve_abmn2(rows, cols, radius, lam, time=100):
    mat = np.full((rows, cols), -np.inf)
    n_map = mat.copy()
    n_map[0, 0] = lam
    n_map[rows-1, cols-1] = 0
    bounds = get_bounds(n_map)
    n_map = interp_n_matrix(n_map)
    #n_map = uniform_random(n_map)
    # print(n_map)

    m_map = mat.copy()
    m_map[0, 0] = 0
    m_map[rows-1, cols-1] = 1
    m_map = interp_m_matrix(m_map)
    #midpoint = (rows // 2, cols // 2)

    #m_map, n_map = initialize_m_n_matrices(rows, cols, lam, midpoint)
    #bounds = [(0, 0), (rows-1, cols-1)]
    #m_map = uniform_random(m_map)
    # print(m_map)

    solver = ContinuousGraphSolver(n_map=n_map,
                                   m_map=m_map,
                                   time_steps=time,
                                   boundary_coords=bounds,
                                   move_radius=radius
                                   )

    solver.solve(debug=False)
    print(solver.m)
    coords = solver.find_batteground(time - 1, 3)
    plt.scatter(*zip(*[(i, j) for i in range(m_map.shape[0])
                for j in range(m_map.shape[1])]), c='purple')
    if coords:
        plt.scatter(*zip(*coords), c='red', marker='o', s=100)
    plt.scatter(*zip(*bounds), c='black', marker='x', s=100)
    plt.title(f'lambda = {lam}')
    plt.grid(True)
    plt.show()


l = .999
r = 3
#solve_abmn(50, 50, r, l, 1000)
solve_abmn2(50, 50, r, l, 1000)
