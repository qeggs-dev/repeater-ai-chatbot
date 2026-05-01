# Clear Model Client Pool API

清除模型客户端缓存池

- **`/admin/clear/model_client_pool`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key` (str): API 密钥
  - **Response**
    - **type:** `Text`
    - **Content:**
      - "Configs reloaded"

这通常在更新 SSL 时才需要用到