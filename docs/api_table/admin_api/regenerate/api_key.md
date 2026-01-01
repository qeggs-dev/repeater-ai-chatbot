# Regenerate Admin Key

生成新的管理密钥

- **`/admin/admin_key/regenerate`**
  - **method**: POST
  - **Header**
    - `X-Admin-API-Key (str)` API 密钥
  - **Response**
    - **type:** `Text`
    - **Response Body**
      - "Apiinfo reloaded"

注：新生成的管理密钥是临时密钥，
不会自动进行持久化保存，
使用该 API 后如果重启了服务，
则仍然使用环境变量中的管理密钥。