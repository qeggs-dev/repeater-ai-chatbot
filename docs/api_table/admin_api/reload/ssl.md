# Reload SSL

热重载 SSL 上下文

- **`/admin/configs/ssl`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key` (str): API 密钥
  - **Response**
    - **type:** `Text`
    - **Content:**
      - "Configs reloaded"

注：我们无法保证所有 SSL 都能被正确重载
有些模块可能会缓存它，重载后它们不会立刻生效
有些已经创建的 Client 可能会继续使用旧的 SSL 上下文