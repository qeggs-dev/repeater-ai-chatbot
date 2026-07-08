import numpy as np

def sample(data: np.ndarray[tuple[int], np.dtype[np.int64]], target_length: int):
    """
    从可变长度数据中均匀采样固定长度
    """
    assert isinstance(data, np.ndarray), "data Must be a numpy array"
    assert isinstance(target_length, int), "target_length Must be a integer"

    if target_length <= 0:
        raise ValueError("target_length must be a positive integer")
    
    n = len(data)
    if n <= target_length:
        # 数据太短，直接返回原数据（或重复最后一个元素）
        return data.copy()
    
    # 生成均匀间隔的索引
    indices = np.linspace(0, n-1, target_length, dtype=int)
    return data[indices]