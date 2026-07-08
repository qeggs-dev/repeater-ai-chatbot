import numpy as np

def calculate_mad(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
    """使用平均绝对偏差衡量数据稳定性"""
    assert isinstance(intervals, np.ndarray), "intervals Must be a numpy array"

    if len(intervals) < 2:
        return np.inf

    mad = float(np.mean(np.abs(intervals - np.mean(intervals))))
    return mad