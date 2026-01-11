# 管理 API

一组用于高级系统操作的 API。

## 重载资源
  - [重载 API INFO](./reload/apiinfo.md)
  - [重载全局配置](./reload/configs.md)
  - [重载黑名单](./reload/blacklist.md)

## Debug API
  - [Debug API](./debug/index.md)

注：Admin Key 需要保证足够的随机性，
程序会检查 Admin Key 的熵值，
如果 Admin Key 的熵值过低 (`Shannon Entropy` &lt; `3.5`)，
程序会抛出异常以终止启动。

熵值计算公式：

$$H(s) = -\sum_{i=1}^{k} p_i \log_2 p_i$$