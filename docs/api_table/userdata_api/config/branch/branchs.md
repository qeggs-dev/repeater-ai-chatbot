# Config Branchs API

获取 Config 数据下指定用户的所有分支ID列表

- **`/userdata/config/branchs/{user_id:str}`**
  - **Requset**
    - **method:** `GET`
  - **Response**
    - **type:** `JSON列表`
    - **Response Body**:
      - *\*所有已经保存的`branch_id`*