import numpy as np

def calculate_interdecile_range(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
    """使用十分位距衡量数据稳定性"""
    assert isinstance(intervals, np.ndarray), "intervals Must be a numpy array"

    if len(intervals) < 2:
        return np.inf
    
    q90, q10 = np.percentile(intervals, [90 ,10])
    percentile_range = float(q90 - q10)
    return percentile_range