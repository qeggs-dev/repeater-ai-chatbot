# Change Context Branchs API

将指定用户的 Context 活动分支切换到指定分支

- **`/userdata/context/branchs/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Request Body**:
      - `new_branch_id (str)`:  新的分支ID
  - **Response**
    - **type:** `Text`
    - **Response Body**:
      - "Context branch changed"