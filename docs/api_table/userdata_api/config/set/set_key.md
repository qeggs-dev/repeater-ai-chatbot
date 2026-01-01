# Set Config Field API

设置指定用户配置字段

- **`/userdata/config/set/{user_id:str}/{key:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `JSON`
    - **Request Body**:
      - `type (str)`:  配置类型
      - `value (Any)`:  配置字段值
  - **Response**
    - **type:** `Text`
    - **Response Body**:
      - *\*Config 内容*

配置类型列表如下：
- `int` 整形数据
- `float` 浮点数据
- `string` 字符串数据
- `boolean` 布尔数据
- `dict` 字典数据
- `list` 列表数据
- `raw` 使用JSON反序列化得到的数据
- `null` 空数据