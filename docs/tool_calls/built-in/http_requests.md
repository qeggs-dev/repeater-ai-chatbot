# HTTP Requests Tool

该工具用于发送 HTTP 请求
如需访问内网需要配置 `tool_calls.allow_private_network_requests` 为 `true`

注册名：`http_requests`

接受参数：
``` json
{
  "base_url": "", // The base URL shared by all requests.
  "base_headers": null, // The underlying request header shared by all requests.
  "base_cookies": null, // The base Cookie shared by all requests.
  "base_auth": null, // The base Auth shared by all requests.
  "base_timeout": 5, // Requests timeout in seconds.
  "requests": [ // Sending requests in batches using connection pooling (The outer list executes sequentially, and the inner list executes in parallel.).
    [
      {
        "method": "", // The HTTP method to use for the request.
        "url": "", // The target URL of the request.
        "query_params": null, // Query parameters to include in the request URL.
        "headers": null, // HTTP headers to send with the request.
        "cookies": null, // Cookies to attach to the request.
        "form_data": null, // Form-data to send with the request.
        "json_data": null, // JSON data to send in the request body.
        "auth": null, // Basic authentication credentials as a (username, password) tuple.
        "follow_redirects": true, // Whether to automatically follow HTTP redirects.
        "timeout_seconds": 10, // Request timeout in seconds.
      }
    ]
  ]
}
```

然后拿到响应对象列表

```json
{
  "responses":[
    {
      "status_code": 200, // 状态码
      "reason": "success", // 只要响应了就是 `success` 而超时等情况会是其他内容
      "headers": {}, // 响应头
      "cookies": {}, // 响应 cookie
      "request": {},  // 之前填写的请求体对象
      "data": {} // 响应内容(如果 JSON 解析失败，则将响应文本作为 `data` 返回，解析成功则该字段为任意 JSON 对象)
    }
  ]
}
```