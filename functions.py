import numpy as np

def get_bounds(map: np.ndarray[tuple[int, int], float]) \
    -> list[tuple[int, int]]:
    bounds = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] != np.inf:
                bounds.append((i, j))
    
    return bounds
            

def uniform_random(map: np.ndarray[tuple[int, int], float],
                   boundary_coords: list[tuple[int, int]]) \
                    -> np.ndarray[tuple[int, int], float]:
    max_val = np.max([map[i, j] for i, j in boundary_coords])
    min_val = np.min([map[i, j] for i, j in boundary_coords])
    map_copy = map.copy()
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == np.inf or (i, j) in boundary_coords:
                continue
            map_copy[i, j] = min_val + max(
                (max_val - min_val) * np.random.random(),
                1e-4)
    
    return map_copy
