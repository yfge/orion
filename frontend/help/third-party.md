# 第三方集成指南（对接商户/外部系统）

本文面向第三方/商户/外部系统，介绍如何使用 Orion 的公开接口完成消息推送与发送结果查询。

## 1. 基础信息

- 基础地址（本地示例）：`http://localhost:8080`
- 生产环境：以贵方配置的域名为准，建议通过 HTTPS 访问
- 所有公开接口均走同一前缀：`/api/v1`（例如：`/api/v1/notify`）

## 2. 鉴权（API Key）

- 由平台管理员在控制台“API Keys”新建并分发给第三方。
- 推荐在请求头使用 Bearer 方式：`Authorization: Bearer <token>`。
- 兼容：`X-API-Key: <token>` 或 `Authorization: Basic <base64("api:<token>")>`。

> 出于安全考虑：请勿将 API Key 暴露在前端代码或可共享介质中；建议保存在后端安全配置或密钥管理系统。

## 3. 同步发送（简单可靠）

- 接口：`POST /api/v1/notify`
- 请求体（二选一）：
  - `{ "message_name": "<name>", "data": { ... } }`
  - `{ "message_definition_bid": "<bid>", "data": { ... } }`
- 成功响应：`{"results": [{"dispatch_bid","endpoint_bid","status_code","body"}]}`

示例（curl）：

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{
    "message_name": "simple-text",
    "data": { "text": "hello from vendor" }
  }'
```

适用场景：消息量不大、对实时响应有要求；返回中可直接获取第三方渠道响应。

## 4. 异步发送（高并发友好）

- 接口：`POST /api/v1/notify/async`（202 Accepted）
- 请求体同同步发送，可额外携带 `request_id`（字符串，可由业务生成并保证唯一性），系统会在发送记录中以 remark 存储。
- 成功响应：`{"accepted":true, "request_id":"...", "estimated_dispatches": 2}`

示例：

```bash
REQ=$(uuidgen | tr 'A-Z' 'a-z' | tr -d '-')
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify/async \
  -d "{\n  \"message_name\": \"simple-text\",\n  \"data\": { \"text\": \"async hello\" },\n  \"request_id\": \"$REQ\"\n}"
```

注意：当前 `request_id` 用于回查，不做幂等去重。若需严格幂等，可在业务侧保证同一 `request_id` 不重复提交，或后续接入幂等键策略。

## 5. 发送记录查询（API Key）

- 列表：`GET /api/v1/notify/send-records?limit=50&offset=0&message_definition_bid=&notification_api_bid=&status=&start_time=&end_time=&request_id=`
- 单条：`GET /api/v1/notify/send-records/{bid}`
- 明细：`GET /api/v1/notify/send-records/{bid}/details?limit=50&offset=0`

按 `request_id` 回查示例：

```bash
curl -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8080/api/v1/notify/send-records?request_id=$REQ&limit=20&offset=0"
```

返回字段

- 记录：`send_record_bid`、`message_definition_bid`、`notification_api_bid`、`message_name`、`endpoint_name`、`business_system_name`、`send_time`、`result`、`remark`（即 request_id）、`status`、`created_at`
- 明细：`request_payload`、`response_payload`、`error`、`attempt_no`、`sent_at` 等

## 6. 错误码约定

- 401 Unauthorized：API Key 无效/缺失
- 404 Not Found：资源不存在（如消息名错误）
- 5xx：系统异常或第三方渠道错误（建议重试/告警）

## 7. 最佳实践

- 鉴权：统一用 Bearer 方式；API Key 定期轮换
- 异步发送：大流量下建议优先使用 `/notify/async`，并以 `request_id` 回查
- 重试策略：对 5xx 采用指数退避；对 4xx 先排查参数/鉴权
- 可观测性：结合“发送记录”接口与控制台页面，建立告警与看板

## 8. 安全建议

- 仅在服务端存放 API Key；所有调用通过后端转发
- 强制 HTTPS；限制来源 IP；必要时加入签名/时间戳验证
- 及时禁用不再使用的 Key，避免泄露风险
