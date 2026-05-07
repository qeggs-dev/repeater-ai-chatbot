# API_INFO 对象结构

API_INFO
- `name` (str): 模型名称
- `url` (str): 该模型所在的 URL
- `id` (str): 该模型在API中的ID
- `parent` (str): 该模型所属的组名称
- `parent_id` (str): 该模型所属的组ID
- `uid` (str): 该模型的唯一标识符
- `limit` (limit): http 连接池的限制
  - `max_connections` (int): 最大连接数
  - `max_keepalive_connections` (int): 最大保持连接数
  - `keepalive_expiry` (float): 保持连接的过期时间，单位为秒
- `timeout` (float | Timeout): 该模型请求的超时时间，单位为秒
  - `connect` (float): 连接超时
  - `read` (float): 读取超时
  - `write` (float): 写入超时
  - `pool` (float): 池超时
