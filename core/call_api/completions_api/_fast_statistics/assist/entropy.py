import numpy as np


def calculate_entropy(data: np.ndarray[tuple[int]]) -> np.float64:
    if len(data) == 0:
        return np.float64(0.0)
    
    # 1. 统计每个唯一值出现的次数
    _, counts = np.unique(data, return_counts=True)
    # 2. 计算每个值的概率
    probabilities = counts / len(data)
    # 3. 计算熵: -sum(p * log2(p))
    # 添加一个极小值 np.finfo(float).eps 防止概率为0时出现 log(0) 的警告
    entropy = -np.sum(probabilities * np.log2(probabilities + np.finfo(float).eps))
    return entropy