import numpy as np

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
