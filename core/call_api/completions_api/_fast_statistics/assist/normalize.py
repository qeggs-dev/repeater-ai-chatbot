import numpy as np

def min_max_normalize(arr: np.ndarray[tuple[int]]):
    """最小-最大归一化"""
    array_range = arr.max() - arr.min()
    if array_range == 0:
        return arr
    return (arr - arr.min()) / array_range