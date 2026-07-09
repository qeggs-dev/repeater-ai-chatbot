import numpy as np

def min_max_normalize(arr: np.ndarray[tuple[int]]):
    """最小-最大归一化"""
    array_range = arr.max() - arr.min()
    if array_range == 0:
        raise ZeroDivisionError("Array range is zero, cannot normalize")
    return (arr - arr.min()) / array_range