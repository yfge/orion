# Notify API 调用与鉴权

- 接口：`POST /api/v1/notify`
- 鉴权（三选一，推荐 Bearer）：
  - `Authorization: Bearer <token>`
  - `X-API-Key: <token>`
  - `Authorization: Basic <base64("api:<token>")>`

请求示例：

```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{
    "message_name": "simple-text",
    "data": { "text": "hello" }
  }'
```

响应：`{"results": [{"dispatch_bid","endpoint_bid","status_code","body"}]}`

> 通过 `/api/v1/notify/keys/preview` 可生成随机 key，需配置到后端环境变量或在“API Keys”中创建。
