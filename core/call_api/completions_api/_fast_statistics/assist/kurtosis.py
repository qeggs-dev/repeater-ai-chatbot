import numpy as np


def calculate_kurtosis(data: np.ndarray[tuple[int]]) -> np.float64:
    assert isinstance(data, np.ndarray), "data must be a numpy array"

    n = len(data)
    if n < 4:
        raise ValueError("Data set too small to calculate kurtosis")
    mean = np.mean(data)
    variance = np.var(data) # 注意：这是有偏的总体方差
    # 计算四阶中心矩并除以方差平方，最后减去3得到超额峰度
    kurtosis = np.sum((data - mean) ** 4 / (variance ** 2)) / n - 3
    return kurtosis