from typing import Callable

def create_special_chars_remover() -> Callable[[str], str]:
    """创建优化的字符移除器"""
    delete_chars = []
    for i in range(32, 127):
        c = chr(i)
        if not (('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('0' <= c <= '9') or c == '_'):
            delete_chars.append(c)
    
    delete_str = ''.join(delete_chars)
    trans_table = str.maketrans('', '', delete_str)
    
    def remover(text: str):
        # 先处理ASCII字符
        result = text.translate(trans_table)
        return result
    
    return remover