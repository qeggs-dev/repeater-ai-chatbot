# Reload Api Info

热重载模型定义文件

- **`/admin/apiinfo/reload`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key (str)` API 密钥
  - **Response**
    - **type:** `Text`
    - **Response Body**
      - "Apiinfo reloaded"

注：重载的本质是覆盖，
无法删除多余的模型定义。