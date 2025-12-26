# Reload Configs

热重载配置文件

- **`/admin/configs/reload`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key (str)` API 密钥
  - **Response**
    - **type:** `Text`
    - **Response Body**
      - "Configs reloaded"

注：有些配置可能无法热重载，
它们被程序缓存到了内存中，
无法被这种方式修改，
只能使用重启服务的方式解决。