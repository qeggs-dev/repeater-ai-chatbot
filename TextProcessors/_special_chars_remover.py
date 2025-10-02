from typing import Callable

_delete_chars = []
for i in range(32, 127):
    c = chr(i)
    if not (('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('0' <= c <= '9') or c == '_'):
        _delete_chars.append(c)

_delete_str = ''.join(_delete_chars)
_trans_table = str.maketrans('', '', _delete_str)

def remover(text: str):
    # 先处理ASCII字符
    result = text.translate(_trans_table)
    return result

