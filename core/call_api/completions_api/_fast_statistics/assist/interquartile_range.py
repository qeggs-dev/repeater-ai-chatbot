import numpy as np

def calculate_interquartile_range(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
    """使用四分位距衡量数据稳定性"""
    if len(intervals) < 2:
        return np.inf
    
    q75, q25 = np.percentile(intervals, [75 ,25])
    iqr = float(q75 - q25)
    return iqr