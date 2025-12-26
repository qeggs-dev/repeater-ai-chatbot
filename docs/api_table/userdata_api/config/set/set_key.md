# Set Config Field API

设置指定用户配置字段

- **`/userdata/config/set/{user_id:str}/{key:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `JSON`
    - **Request Body**:
      - `type (str)`:  配置类型(int/float/string/bool/dict/list/raw/null)
      - `value (Any)`:  配置字段值
  - **Response**
    - **type:** `Text`
    - **Response Body**:
      - *\*Config 内容*

