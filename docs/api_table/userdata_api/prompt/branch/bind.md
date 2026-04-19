# Prompt Branch Bind API

绑定当前分支到指定分支

- **`/userdata/prompt/bind/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Content:**
      - `dst_branch_id` (str): 目标分支ID
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `status` (str):  "success"

注：绑定功能需要系统支持硬链接