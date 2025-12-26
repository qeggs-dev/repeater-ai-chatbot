# Rewrite Context API

向用户 Context 的尾部注入一条上下文信息

- **`/userdata/context/rewrite/{user_id:str}`**
  - **Requset**
    - **method:** `POST`
    - **type:** `JSON`
    - **Request Body**:
      - `index (int)` 上下文索引 (必须存在)
      - `content`
        - `reasoning_content (str)` CoT内容(一般不用填写，除非你需要让它作为前缀使用)
        - `content (str | list[ContentBlock])` 上下文内容
        - `role (str)` 上下文角色(user | assistant | system)
        - `role_name (str)` 上下文角色名称(用于在role上进一步细分多用户，以让模型区分不同角色的user)
        - `prefix (bool)` 该单元是否为前缀（用于前缀续写模式，如果这里rewrite的内容不在尾部，就不建议它为true）
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `status (str)` 状态码，如果 `http code` 为 `200` 则必为`success`
      - `context (Context)` 更新后的Context内容