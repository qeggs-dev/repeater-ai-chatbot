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
        "verify_crawler_permissions": true, // Whether to verify crawler permissions.
        "exclude_crawler_user_agent": false // Whether to not actively add the `User-Agent` in the request header (turn off this option if you need to set 'User-Agent') .
      },
      {
        "sleep_seconds": 10 // Sleep in a batch affects the end time of the batch.
      }
    ],
    {
      "sleep_seconds": 10.0 // Sleep on the outside suspends requests on the back end.
    },
    {
      // If the batch had only one request, it could be written like this.
      "method": "GET",
      "url": "https://example.com"
    }
  ]
}
```

然后拿到响应对象列表

```json
{
  "responses":[
    {
      "status_code": 200, // HTTP Status Code
      "reason": "success", // As long as the response is `success` and timeouts and the like will be something else
      "headers": {}, // Response headers
      "cookies": {}, // Response cookie
      "request": {},  // Request object
      "data": {} // The response content (if the JSON parsing fails, the response text is returned as `data` ; if the parsing succeeds, the field is any JSON object) 
    }
  ]
}
```