def create_special_chars_remover():
    """创建优化的字符移除器"""
    # 构建要删除的字符集（除了字母数字下划线之外的所有ASCII字符）
    delete_chars = []
    for i in range(32, 127):  # ASCII可打印字符范围
        c = chr(i)
        if not (('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('0' <= c <= '9') or c == '_'):
            delete_chars.append(c)
    
    delete_str = ''.join(delete_chars)
    trans_table = str.maketrans('', '', delete_str)
    
    def remover(text: str):
        # 先处理ASCII字符
        result = text.translate(trans_table)
        # 对于非ASCII字符，我们保留（因为您说可以放行）
        return result
    
    return remover