# Set Context API

设置指定用户的上下文内容

- **`/userdata/context/set/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `JSON`
    - **Content:**
      - *\*Context 内容*
  - **Response**
    - **type:** `Text`
      - **Content:**
        - "Success"