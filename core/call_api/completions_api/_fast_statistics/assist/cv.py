import numpy as np

def calculate_cv(intervals: np.ndarray[tuple[int], np.dtype[np.int64]]):
    """使用变异系数衡量数据稳定度"""
    if len(intervals) == 0:
        return np.inf  # 无穷大表示不稳定
    
    std_dev = np.std(intervals)
    mean_val = np.mean(intervals)
    
    if mean_val == 0:
        return np.inf  # 防止除以零错误
    
    cv = std_dev / mean_val  # 变异系数
    stability = 1 / (1 + cv)  # 转换为稳定度分数 (0-1之间，越大越稳定)
    return float(stability)