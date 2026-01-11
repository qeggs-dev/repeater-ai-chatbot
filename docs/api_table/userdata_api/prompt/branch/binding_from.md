# Prompt Branch Binding From API

绑定当前分支到指定分支

- **`/userdata/prompt/binding_from/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Request Body**:
      - `src_branch_id (str)`: 源目标分支ID
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `status (str)`:  "success"

注：绑定功能需要系统支持硬链接