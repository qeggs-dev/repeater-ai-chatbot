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

注：我无法保证所有配置都能被正确重载
有些模块可能会缓存配置，重载后它们不会立刻生效
但目前来说，绝大部分的模块都已经可以正确的重载配置了