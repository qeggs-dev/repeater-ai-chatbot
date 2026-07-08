import numpy as np

def calculate_skewness(data: np.ndarray[tuple[int]]) -> float:
    assert isinstance(data, np.ndarray), "data must be a numpy array"

    n = len(data)
    if n < 3:
        return 0.0
    mean = np.mean(data)
    # 计算中心矩
    m2 = np.sum((data - mean) ** 2) / n      # 二阶矩
    m3 = np.sum((data - mean) ** 3) / n      # 三阶矩
    # 修正后的样本偏度
    g1 = m3 / (m2 ** 1.5)
    # 小样本修正因子
    correction = np.sqrt(n * (n - 1)) / (n - 2)
    return g1 * correction