# Change Prompt Branchs API

将指定用户的 Prompt 活动分支切换到指定分支

- **`/userdata/prompt/change/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Content:**
      - `new_branch_id` (str):  新的分支ID
  - **Response**
    - **type:** `Text`
    - **Content:**
      - "Prompt branch changed"