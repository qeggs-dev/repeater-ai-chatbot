# Config Info API

获取当前用户的 Config 分支元数据

- **`/userdata/config/info/{user_id:str}`**
  - **Requset**
    - **method:** `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `branch_id` (str):  当前分支ID
      - `size` (int): 当前分支大小
      - `modified_time` (int): 当前分支最后修改时间
      - `file_exists` (bool): 当前分支文件是否存在