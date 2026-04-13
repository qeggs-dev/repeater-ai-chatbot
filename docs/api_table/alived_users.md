# Alived Users API

用于获取当前活跃用户的数量和列表

- **`/chat/alived_users`**
  - **Request**
    - **method:** `GET`
  - **Response**
    - **type:** `JSON`
    - **Content**: 
      - `message` (str): 用于描述请求结果
      - `count` (int): 当前活跃用户数量
      - `users` (dict[str, UserDetail]): 活跃用户列表，其中key为用户ID，value为用户任务详情
        - *`*user_id`* (str): 用户ID
          - `generated_length` (int): 已生成的字符数
