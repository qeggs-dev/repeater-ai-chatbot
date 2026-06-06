# Ping Provider API

向模型提供方的主机发送 UDP Ping 包，用于检测到模型提供方主机的网络连通性。

- **`/ping_provider/{path}`**
  - **Request**
    - **method:** `POST`
    - **Content:**
      - `model_id` (str): 模型 UID
      - `timeout` (int): 请求超时时间
      - `times` (int): 请求次数
      - `size` (int): 请求包大小
      - `interval` (int): 请求间隔时间
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `sussess_count` (int): 请求成功次数
      - `average_time_spent` (int): 平均请求时间
      - `details` (list): 请求详情
        - *\*list*
          - `host_names` (list[str]): 主机名
          - `ip` (str): IP 地址
          - `time` (list[float]): 请求时间
          - `packet_loss` (list[int]): 丢包率
          - `max_time` (float): 最大请求时间
          - `min_time` (float): 最小请求时间
          - `avg_time` (float): 平均请求时间