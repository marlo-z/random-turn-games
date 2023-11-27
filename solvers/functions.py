import numpy as np
from abmn_graph_classes import MatrixGraphSolver
from functions import *


def get_bounds(map: np.ndarray[tuple[int, int]]) -> list[tuple[int, int]]:
    bounds = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] != np.inf and map[i, j] != -np.inf:
                bounds.append((i, j))

    return bounds


def uniform_random(map: np.ndarray[tuple[int, int], float]) -> np.ndarray:
    max_val = np.ma.masked_invalid(map).max()
    min_val = np.ma.masked_invalid(map).min()
    map_copy = map.copy()
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == -np.inf:
                map_copy[i, j] = min_val + max(
                    (max_val - min_val) * np.random.random(),
                    1e-4)

    return map_copy


def find_path_between_bounds(map: np.ndarray[tuple[int, int], float]) -> np.ndarray:
    bounds = get_bounds(map)
    rows, cols = map.shape

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and map[(x, y)] != np.inf
    paths = []
    visited = np.zeros_like(map, dtype=bool)

    def dfs(x, y, path):
        if not is_valid(x, y):
            return
        if (x, y) == bounds[1]:
            paths.append(path + [(x, y)])
            return
        visited[x, y] = True
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y) and not visited[new_x, new_y]:
                dfs(new_x, new_y, path + [(x, y)])
    start_x, start_y = bounds[0]
    dfs(start_x, start_y, [])
    return paths[0] if paths else None


def linear_interp(map, path):
    map_copy = map.copy()
    left_bound = path[0]
    right_bound = path[-1]
    len_path = len(path)
    iterval = np.abs(map[left_bound]-map[right_bound])/(len_path-1)
    min_bound = min(map[left_bound], map[right_bound])
    max_bound = max(map[left_bound], map[right_bound])
    if map[left_bound] > map[right_bound]:
        for i, (x, y) in enumerate(path):
            map_copy[x, y] = max_bound - i * iterval
    else:
        for i, (x, y) in enumerate(path):
            map_copy[x, y] = min_bound + i * iterval
    return map_copy


def lin_interp_full(map):
    map_copy = map.copy()
    map_copy = linear_interp(map, find_path_between_bounds(map))
    return map_copy


def arctan_interp(map, path):
    map_copy = map.copy()
    left_bound = path[0]
    right_bound = path[-1]
    len_path = len(path)
    max_bound = max(map[left_bound], map[right_bound])
    if map[left_bound] > map[right_bound]:
        for i, (x, y) in enumerate(path):
            if (x, y) != left_bound and (x, y) != right_bound:
                t = i / (len_path - 1)
                map_copy[x, y] = max_bound - \
                    (np.arctan(10 * t - 5) / np.pi + 0.5)
    else:
        for i, (x, y) in enumerate(path[::-1]):
            if (x, y) != left_bound and (x, y) != right_bound:
                t = i / (len_path - 1)
                map_copy[x, y] = max_bound - \
                    (np.arctan(10 * t - 5) / np.pi + 0.5)

    return map_copy


def arctan_interp_full(map):
    map_copy = map.copy()
    map_copy = arctan_interp(map, find_path_between_bounds(map))
    return map_copy


def interp_m_matrix(map):
    map_copy = map.copy()
    rows, cols = map_copy.shape
    for x in range(rows):
        for y in range(cols):
            map_copy[(x, y)] = x+y
    return map_copy


def interp_n_matrix(map):
    map_copy = map.copy()
    rows, cols = map_copy.shape
    for x in range(rows):
        for y in range(cols):
            map_copy[(x, y)] = rows+cols-x-y-2
    return map_copy

