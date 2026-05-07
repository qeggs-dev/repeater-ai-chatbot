# 管理 API

一组用于高级系统操作的 API。

## Reload API
  - [Reload Configs](./reload/configs.md)
  - [Reload Blacklist](./reload/blacklist.md)
  - [Reload SSL](./reload/ssl.md)

## Debug API
  - [Debug API](./debug/index.md)

## Regenerate API
  - [Regenerate Admin Key API](./regenerate/admin_key.md)

## Clear API
  - [Clear Model Client Pool](./clear/model_client_pool.md)

注：Admin Key 需要保证足够的随机性，
程序会检查 Admin Key 的熵值，
如果 Admin Key 的熵值过低 (`Shannon Entropy` &lt; `3.5`)，
程序会抛出异常以终止启动。

熵值计算公式：

$$H(s) = -\sum_{i=1}^{k} p_i \log_2 p_i$$