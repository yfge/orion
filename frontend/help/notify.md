# Notify API 调用与鉴权

## 接口与鉴权

- 接口：`POST /api/v1/notify`
- 鉴权（三选一，推荐 Bearer）：
  - `Authorization: Bearer <token>`（推荐，最通用）
  - `X-API-Key: <token>`（兼容模式）
  - `Authorization: Basic <base64("api:<token>")>`（兼容 Mailgun 风格）

生成 Key：

- 控制台“API Keys”新建（明文仅显示一次）；或调用 `/api/v1/notify/keys/preview` 生成随机串后配置到后端环境。

## 请求示例

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

## 请求体与响应

- 请求体（两种任选其一）：
  - `{ "message_name": "<name>", "data": { ... } }`
  - `{ "message_definition_bid": "<bid>", "data": { ... } }`
- 响应：
  - `{ "results": [{ "dispatch_bid", "endpoint_bid", "status_code", "body" }] }`
  - `status_code` 为第三方响应码（HTTP 或 SMTP 语义）；`body` 为第三方响应主体（JSON 或文本）。

## 常见错误

- 401 Unauthorized：Key 无效或未配置；检查 Key 是否归属正确、是否启用。
- 404 message not found：消息名/BID 配置错误。
- 第三方渠道 4xx/5xx：查看“发送记录”中的 detail（请求/响应）排障。
