# Prompt Info API

获取当前用户的 Prompt 分支元数据

- **`/userdata/prompt/info/{user_id:str}`**
  - **Requset**
    - **method:** `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `branch_id (str)`:  当前分支ID
      - `size (int)`: 当前分支大小
      - `readable_size (str)`: 当前分支大小（可读）
      - `modified_time (int)`: 当前分支最后修改时间

注：`readable_size` 的低位并不会作为高位的小数部分，而是单独显示。
比如：`1572864` 就会是 `1M，512K`