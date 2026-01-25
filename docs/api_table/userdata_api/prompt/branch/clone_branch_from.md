# Prompt Branch Clone From API

将指定分支克隆到当前分支

- **`/userdata/prompt/clone_from/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Request Body**:
      - `src_branch_id (str)`: 源目标分支ID
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `status (str)`:  "success"