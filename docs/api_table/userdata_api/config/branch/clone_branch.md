# Config Branch Clone API

将当前分支克隆到一个新的指定分支

- **`/userdata/config/clone/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Request Body**:
      - `dst_branch_id (str)`:  目标分支ID
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `status (str)`:  "success"