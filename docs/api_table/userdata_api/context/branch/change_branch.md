# Change Context Branchs API

将指定用户的 Context 活动分支切换到指定分支

- **`/userdata/context/change/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Content:**
      - `new_branch_id` (str):  新的分支ID
  - **Response**
    - **type:** `Text`
    - **Content:**
      - "Context branch changed"