# HTTP GET Function

发送 HTTP GET 请求

- `httpget`: 发送 HTTP GET 请求
  - Params:
    - `url` (str): 
      `params` (dict[str, Any]): 查询参数字典
      `headers` (dict[str, str]): HTTP 请求头字典
      `cookies` (dict[str, str]): HTTP 请求 cookies
      `auth` (BasicAuth | DigestAuth | None): HTTP 认证
      `proxy` (dict[str, str] | None): HTTP 代理
      `follow_redirects` (bool): 是否跟随重定向
      `verify` (str | bool): SSL 证书验证
      `timeout` int | float: 请求超时时间
      `trust_env` bool: 是否信任环境变量中的代理设置
  - Returns:
    - (HTTPResponse): HTTP 响应对象

该函数在主配置 `template.allow_http` 设置为 `true` 才存在